import os
import re
import xml.etree.ElementTree as ET

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


def get_body(path):
    """This function parse the file at initial phase
    and gets its xml body or returns None if the file is invalid"""
    try:
        tree = ET.parse(path)
        tei = tree.getroot()
        text = tei[1]
        body = text.find('tei:body', ns)
        return body
    except:
        print('ERROR while parsing', path)
        return None


def get_divs(path):
    """This function gets all the divs of the play
    with their contents"""
    body = get_body(path)
    if body is not None:
        divs = body.findall('tei:div', ns)
        return divs
    else:
        return None


def parse_divs(path):
    """This function parses the divs, if div contains divs,
    the number of these subdivs are added to the number of scenes,
    else number of scenes gets +1. If there were no divs in the xml, number of scenes is 1."""
    scenes_num = 0
    divs = get_divs(path)
    if divs is not None:
        for div in divs:
            subdivs = div.findall('tei:div', ns)
            if len(subdivs) == 0:
                scenes_num += 1
            else:
                scenes_num += len(subdivs)
    if scenes_num == 0:
        scenes_num = 1
    return scenes_num


for file in os.listdir('./ready_TEI/'):
    if file.endswith('.xml'):
        print(parse_divs('./ready_TEI/' + file))
