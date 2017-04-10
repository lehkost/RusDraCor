import re
import transliterate
import os

for root, dirs, files in os.walk('./wikisource_raws/1/'):
    for file in files:
        if file.endswith('.txt'):
            print(file)
            text = open('./wikisource_raws/1/' + file, 'r', encoding='utf-8')
            text_read = text.read()
            text.close()
            title = re.findall('НАЗВАНИЕ *?= ?(.*?)\n', text_read)[0]
            author = re.findall('АВТОР *?= ?\[?\[?(.*?)\]?\]?', text_read)[0]
            '''
            razrs = re.findall('\{\{Razr\|.*?\}\}', text_read)
            for el in razrs:
                e = re.findall('\{\{Razr\|(.*?)\}\}', el)[0]
                text_read = re.sub(el, '<actor>' + e + '</actor>', text_read)
            text = open('./wikisource_raws/1/' + file, 'w', encoding='utf-8')
            text.write(text_read)
            text.close()
            '''
            text = open('./wikisource_raws/1/' + file, 'r', encoding='utf-8')
            tei_header = open('tei_header.xml', 'r', encoding='utf-8').read()
            text_tei = open('./wikisource_tei/1/' + file.split('.txt')[0] + '.xml', 'w', encoding='utf-8')
            text_tei.write(tei_header)

            poem = False
            cast = False
            castList = []
            start = False
            sp = False
            for line in text:
                if line == "<div class='drama text'>\n":
                    start = True
                if start:
                    if 'действующие лица' in line.lower():
                        cast = True
                    if cast:
                        if len(re.findall('\{\{razr2?\|(.*?)\}\}', line)) != 0:
                            castList.append(re.findall('\{\{razr2?\|(.*?)\}\}', line)[0])

                    if line.startswith('{{rem|') or line.startswith('{{Rem|'):
                        stage = re.findall('\{\{[Rr]em\|(.*?)\}\}', line)[0]
                        text_tei.write('<stage>' + stage + '</stage>\n')
                    if line == '\n' or line == '----\n':
                        pass
                    if line.startswith('<poem'):
                        poem = True
                    if line.startswith('</poem>'):
                        poem = False
                    if line.lower().startswith('{{re|'):
                        speaker = re.findall('\{\{[Rr]e\|(.*?)\|', line)
                        if len(speaker) == 0:
                            speaker = re.findall('\{\{[Rr]e\|(.*?)\}\}', line)
                            speaker = speaker[0]
                        else:
                            speaker = re.findall('\{\{[Rr]e\|(.*?)\|', line)[0]
                        speaker_id = transliterate.translit(speaker, 'ru', reversed=True)
                        stage_del = re.findall('\{\{[Rr]e\|' + speaker + '\|\((.*?)\)\}\}', line)
                        if len(stage_del) != 0 and len(speaker) != 0:
                            stage_del = stage_del[0]
                            text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>'
                                            + '<stage type="delivery">' + stage_del
                                            + '</stage>\n')
                        if len(stage_del) == 0 and len(speaker) != 0:
                            text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>\n')
                        if len(stage_del) != 0 and len(speaker) == 0:
                            stage_del = stage_del[0]
                            text_tei.write('<stage>' + stage_del + '</stage>\n')
                    #if line == '\n':
                        #text_tei.write('</sp>\n')
                    if line.startswith('<h4>'):
                        scene_title = re.findall('<h4>(.*?)</h4>', line)[0]
                        text_tei.write('<div type="scene">\n<head>' + scene_title + '</head>\n')
                    if line.startswith('<center>'):
                        stage_text = re.findall('<center>(.*?)</center>', line)[0]
                        text_tei.write('<stage>' + stage_text + '</stage>\n')
                    else:
                        if poem:
                            if not line.startswith('{{Re|') and not line.startswith('{{re|')\
                                    and not line.startswith('{{rem|') and not line.startswith('{{Rem|')\
                                    and not line.startswith('<h4>') and not line == '<poem>\n':
                                if line == '----\n' or line == '<poem>\n':
                                    pass
                                if line == '\n':
                                    pass
                                else:
                                    if 'indent' in line:
                                        line = line.split('}}')[1]
                                        text_tei.write('<l part="F">' + line.split('\n')[0] + '</l>\n')
                                    else:
                                        text_tei.write('<l>' + line.split('\n')[0] + '</l>\n')
                        if not poem:
                            if not line.startswith('{{Re|') and not line.startswith('{{re|')\
                                    and not line.startswith('{{rem|') and not line.startswith('{{Rem|')\
                                    and not line.startswith('<h4>') and not line.startswith('|')\
                                    and not line == '</poem>\n':
                                '''
                                if line.lower().startswith('{{реплика|'):
                                    print(line)
                                    speaker = re.findall('\{\{Реплика\|(.*?)\|', line)
                                    if len(speaker) == 0:
                                        speaker = re.findall('\{\{Реплика\|(.*?)\}\}', line)[0]
                                    else:
                                        speaker = speaker[0]
                                    speaker_id = transliterate.translit(speaker, 'ru', reversed=True)
                                    stage_del = re.findall('\{\{Реплика\|' + speaker + '\|(.*?)\}\}', line)
                                    if len(stage_del) != 0 and len(speaker) != 0:
                                        stage_del = stage_del[0]
                                        text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>'
                                                        + '<stage type="delivery">' + stage_del
                                                        + '</stage>\n')
                                    if len(stage_del) == 0 and len(speaker) != 0:
                                        text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>\n')
                                '''

                                if line == '\n':
                                    pass
                                if line == "<div class='drama text'>\n":
                                    pass
                                else:
                                    text_tei.write('<p>' + line.split('\n')[0] + '</p>\n')



            text_tei.write('</body>\n</text>\n</TEI>')

            text_tei.close()
            text_tei = open('./wikisource_tei/1/' + file.split('.txt')[0] + '.xml', 'r', encoding='utf-8')
            text_tei_read = text_tei.read()
            text_tei.close()
            text_tei_read = re.sub('<l></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<p></p>\n', '', text_tei_read)
            text_tei_read = re.sub('<sp>', '</sp>\n<sp>', text_tei_read)
            text_tei_read = re.sub('<sp who', '</sp>\n<sp who', text_tei_read)
            text_tei_read = re.sub('<l></l>\n', '', text_tei_read)
            text_tei_read = re.sub('<p></p>\n', '', text_tei_read)
            text_tei_read = re.sub('</l>\n<div', '</l>\n</sp>\n<div', text_tei_read)
            text_tei_read = re.sub('</sp>\n<div', '</sp>\n</div>\n<div', text_tei_read)
            text_tei_read = re.sub('<ref.*?>.*?</ref>', '', text_tei_read)
            text_tei_read = re.sub('<author></author>', '<author>' + author + '</author>', text_tei_read)
            text_tei_read = re.sub('<title type="main"></title>', '<title type="main">' + title + '</title>', text_tei_read)
            text_tei = open('./wikisource_tei/1/' + file.split('.txt')[0] + '.xml', 'w', encoding='utf-8')
            text_tei.write(text_tei_read)

            castListLine = ''
            for person in castList:
                castListLine += '<castItem>' + person + '</castItem>\n'