from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from transliterate import translit


# some magic write nice xml's
def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


def dotfix(name):
    if name[-1] == ".":
        return name[:-1]
    else:
        return name


# prepare bs
work_file = open('test2.htm', 'r')
text = work_file.read()
soup = BeautifulSoup(text, 'html.parser')

target_tag_list = ["h2", "h3", "p", "div"]
init_tag = soup.find(["h2", "h3"])
current_tag = init_tag


# some consts to parse
new_act_dict = {"type": "act"}
new_scene_dict = {"type": "scene"}
new_speech_dict = {"who": "$$Undefined"}
new_speech_stage_delivery = {"type": "delivery"}

now_cast_list = False
previous_speaker_name = None


# init xml result
xml_text = ET.Element("text")
xml_body = ET.SubElement(xml_text, "body")
xml_current_tag = xml_body

xml_current_act_tag = ET.SubElement(xml_body, "div", attrib=new_act_dict)
xml_add_head = ET.SubElement(xml_current_act_tag, "head")
xml_add_head.text = init_tag.string


# going through the text
while current_tag.find_next(target_tag_list):
    speaker_name = None
    current_tag = current_tag.find_next(target_tag_list)

    # second type of castlists
    if now_cast_list and current_tag.name == "div":
        if len(current_tag["align"]) > 1:
            xml_cast_item = ET.SubElement(xml_cast_list_tag, "castItem")
            xml_cast_item.text = list(current_tag.children)[0].string

    # speech tag
    if current_tag.name == "p":
        if len(current_tag["class"]) == 0:
            raise RuntimeError("no class atrr for an <p> tag..")

        if len(current_tag["class"]) > 1:
            raise RuntimeWarning("hmm more than one class atr")

        # stage action
        if current_tag["class"][0] in {"stage", "remark"}:
            if current_tag.string is not None and current_tag.string.strip() != "":
                if now_cast_list:
                    xml_current_phrase = ET.SubElement(xml_current_act_tag, "stage")
                else:
                    xml_current_phrase = ET.SubElement(xml_current_scene_tag, "stage")

                xml_current_phrase.text = current_tag.string.strip()
            now_cast_list = False

        # for the first type of castlists
        if now_cast_list:
            person_desc = list(current_tag.children)[0].string + list(current_tag.children)[1].string
            xml_cast_item = ET.SubElement(xml_cast_list_tag, "castItem")
            xml_cast_item.text = person_desc
            continue

        # regular speech
        if current_tag["class"][0] == "text-regular" or current_tag["class"][0] == "text-continuation":

            # check about speech continuation to guess who
            if current_tag["class"][0] == "text-regular":
                speaker_name = None
            else:
                speaker_name = previous_speaker_name

            # add speech tag
            xml_current_speech_tag = ET.SubElement(xml_current_scene_tag,
                                                   "sp", attrib=new_speech_dict)

            # parsing items
            for child_tag in current_tag.children:
                if child_tag.name is None:
                    # it is a text

                    if child_tag.string is not None and child_tag.string.strip() != "":
                        xml_current_phrase = ET.SubElement(xml_current_speech_tag, "p")
                        xml_current_phrase.text = child_tag.string.strip()

                if child_tag.name == "span":
                    # here we parse some remarks and speakers
                    if len(child_tag["class"]) == 0:
                        raise RuntimeError("no class atrr for an <span> tag..")

                    if len(child_tag["class"]) > 1:
                        raise RuntimeWarning("hmm more than one class atr")

                    if child_tag["class"][0] == "speaker":
                        speaker_name = dotfix(child_tag.string)

                        xml_current_phrase = ET.SubElement(xml_current_speech_tag, "speaker")
                        xml_current_phrase.text = child_tag.string.strip()

                    if child_tag["class"][0] == "remark":
                        xml_current_phrase = ET.SubElement(xml_current_speech_tag, "stage",
                                                           attrib=new_speech_stage_delivery)
                        xml_current_phrase.text = child_tag.string.strip()

            # set who attribute
            if speaker_name is not None:
                res_speaker = translit(speaker_name, "ru", reversed=True)
                xml_current_speech_tag.set("who", "#" + res_speaker)
            else:
                print(previous_speaker_name)
                print("Warning: fix who for:")
                print(current_tag)

            # update info about prev speaker
            previous_speaker_name = speaker_name

    # new yavlenie ?
    if current_tag.name == "h3":
        # magic to detect castlists
        tech_current_tag_text = current_tag.string
        tmp_words = tech_current_tag_text.split()
        if tmp_words[0] == "ЛИЦА":
            now_cast_list = True

            xml_cast_list_tag = ET.SubElement(xml_current_act_tag, "castList")
            xml_add_head = ET.SubElement(xml_cast_list_tag, "head")
            xml_add_head.text = tech_current_tag_text
        else:
            now_cast_list = False

            xml_current_scene_tag = ET.SubElement(xml_current_act_tag,
                                                  "div", attrib=new_scene_dict)
            xml_add_head = ET.SubElement(xml_current_scene_tag, "head")
            xml_add_head.text = current_tag.string.strip()

    # new deistvie ?
    if current_tag.name == "h2":
        now_cast_list = False

        xml_current_act_tag = ET.SubElement(xml_body,
                                            "div", attrib=new_act_dict)
        xml_add_head = ET.SubElement(xml_current_act_tag, "head")
        xml_add_head.text = current_tag.string.strip()


# write results
resulting_xml = ET.ElementTree(element=xml_text)
indent(resulting_xml.getroot())
resulting_xml.write("sample.xml", encoding="utf-8")
