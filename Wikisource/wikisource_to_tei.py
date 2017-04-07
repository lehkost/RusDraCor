import re
import transliterate

text = open('./wikisource_raws/41. Don-Zhuan v Egipte.txt', 'r', encoding='utf-8')
text_read = text.read()
text.close()
title = re.findall('НАЗВАНИЕ = (.*?)\n', text_read)[0]
author = re.findall('АВТОР = (.*?)\n', text_read)[0]
text = open('./wikisource_raws/41. Don-Zhuan v Egipte.txt', 'r', encoding='utf-8')

tei_header = open('tei_header.xml', 'r', encoding='utf-8').read()
text_tei = open('/wikisource_tei/Don-Zhuan v Egipte_v2.xml', 'w', encoding='utf-8')
text_tei.write(tei_header)

poem = False
cast = False
castList = []
for line in text:
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
    if line == '<poem>\n':
        poem = True
    if line.startswith('</poem>'):
        poem = False
    if poem:
        if line.startswith('{{Re|') or line.startswith('{{re|'):
            speaker = re.findall('\{\{[Rr]e\|(.*?)\|', line)[0]
            speaker_id = transliterate.translit(speaker, 'ru', reversed=True)
            stage_del = re.findall('\{\{[Rr]e\|' + speaker + '\|\((.*?)\)\}\}', line)
            if len(stage_del) != 0 and len(speaker) != 0:
                print(stage_del)
                stage_del = stage_del[0]
                text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>'
                               + '<stage type="delivery">' + stage_del
                               + '</stage>\n')
            if len(stage_del) == 0 and len(speaker) != 0:
                text_tei.write('<sp who="#' + speaker_id + '">\n<speaker>' + speaker + '</speaker>\n')
            if len(stage_del) != 0 and len(speaker) == 0:
                stage_del = stage_del[0]
                text_tei.write('<stage>' + stage_del + '</stage>\n')
        else:
            if line == '\n' or line == '----\n' or line == '<poem>\n':
                pass
            else:
                if 'indent' in line:
                    line = line.split('}} ')[1]
                    text_tei.write('<l part="F">' + line.split('\n')[0] + '</l>\n')
                else:
                    text_tei.write('<l>' + line.split('\n')[0] + '</l>\n')

text_tei.write('</body>\n</text>\n</TEI>')

text_tei.close()
text_tei = open('41. Don-Zhuan v Egipte.xml', 'r', encoding='utf-8')
text_tei_read = text_tei.read()
text_tei.close()
text_tei_read = re.sub('<sp>', '</sp>\n<sp>', text_tei_read)
text_tei_read = re.sub('<sp who', '</sp>\n<sp who', text_tei_read)
text_tei_read = re.sub('<author></author>', '<author>' + author + '</author>', text_tei_read)
text_tei_read = re.sub('<title type="main"></title>', '<title type="main">' + title + '</title>', text_tei_read)
text_tei = open('41. Don-Zhuan v Egipte.xml', 'w', encoding='utf-8')
text_tei.write(text_tei_read)

castListLine = ''
for person in castList:
    castListLine += '<castItem>' + person + '</castItem>\n'