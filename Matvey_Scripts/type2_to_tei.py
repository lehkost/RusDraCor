import re
import os
from transliterate import translit


def get_raws(filename):
    text = open(filename, 'r', encoding='utf-8').read()
    text = re.sub('\n\s+\n', '\n\n', text)
    return text.split('\n\n')


def collect_tags(filename):
    tags = list(set(re.findall('{{.*?}}|<.*?>', open(filename, 'r', encoding='utf-8').read())))
    return list(set([re.sub('\|.*?}}', '}}', i) for i in tags]))


def spot_speakers(raw, status):
    speakers = re.findall('{{[Rr]azr.*?\|(.*?)}}', raw)
    if speakers != []:
        if '{' in raw:
            for speaker in speakers:
                raw = re.sub('{{[Rr]azr.*?\|' + speaker + '}}', '<sp who="#' + translit(speaker, 'ru', reversed=True).replace(' ', '_').replace("'", '') +
                             '"><speaker>' + speaker + '</speaker><l>', raw)
            raw += '</l></sp>'
        else:
            raw += '</l></sp>'
    return raw, status


def spot_stage(raw, status):
    stages = re.findall('{{rem.*?\|(.*)}}', raw)
    if stages == []:
        stages = re.findall('{{smallcenter2}}(.*)', raw)
        if stages != []:
            stage2 = re.sub('{{[Rr]azr.*?\|(.*?)}}', '\\1', stages[0])
            raw = re.sub('{{smallcenter2}}' + re.escape(stages[0]), '<stage type="delivery">' + stage2 + '</stage>', raw)
    else:
        if stages != []:
            stage2 = re.sub('{{[Rr]azr.*?\|(.*?)}}', '\\1', stages[0])
            raw = re.sub('{{rem.*?\|' + re.escape(stages[0]) + '}}', '<stage type="delivery">' + stage2 + '</stage>', raw)
    raw = raw.replace('<small>', '<stage type="delivery">').replace('</small>', '</stage>')
    raw = raw.replace('<center>', '<stage type="delivery">').replace('</center>', '</stage>')
    return raw, status


def divs(raw, status):
    if '==' in raw:
        if status == 0:
            raw = '<div>' + raw
            status = 1
        else:
            raw = '</div><div>' + raw
    return raw, status

    
def collect_meta(raw, status):
    if 'Отексте' in raw:
        author = re.findall('АВТОР=\[\[(.*?)\]\]', raw)
        if author != []:
            author = author[0]
        name = re.findall('НАЗВАНИЕ=(.*)', raw)
        if name != []:
            name = name[0]
        date_c = re.findall('ДАТАСОЗДАНИЯ=(.*)', raw)
        if date_c != []:
            date_c = date_c[0]
        date_p = re.findall('ДАТАПУБЛИКАЦИИ=(.*)', raw)
        if date_p != []:
            date_p = date_p[0]
        source = re.findall('ИСТОЧНИК=(.*)\.?', raw)
        if source != []:
            source = source[0].replace('{', '').replace('}', '')
        quality = re.findall('КАЧЕСТВО=(.*)', raw)
        if quality != []:
            quality = quality[0]
        return {'author': author, 'name': name, 'date_c': date_c, 'date_p': date_p, 'source': source, 'quality': quality}, status
    else:
        return raw, status


def create_header(raws, header):
    meta = [raw for raw in raws if type(raw) == dict][0]
    for key in meta:
        header = re.sub('###' + key + '###', str(meta[key]), header)
    return header.replace('[', '').replace(']', '')
    

def all_func(raw, status):
    if '{{[Rr]azr|Инна}}. Ничего. <small>' in raw:
        raw, status = divs(raw, status)
        print('---', raw, '---')
        raw, status = spot_stage(raw, status)
        print('---', raw, '---')
        raw, status = spot_speakers(raw, status)
        print('---', raw, '---')
        raw, status = collect_meta(raw, status)
        print('---', raw, '---')
    else:
        raw, status = divs(raw, status)
        raw, status = spot_stage(raw, status)
        raw, status = spot_speakers(raw, status)
        raw, status = collect_meta(raw, status)
    return raw, status


def no_sp_in_stage(raw):
    stage = re.findall('<stage type="delivery">(.*?)</stage>', raw)[0]
    stage = re.sub('<.*?>', '', stage)
    return '<stage type="delivery">' + stage + '</stage>'


def Run(filename):
    from header import header, closer
    raws = get_raws(filename)
    status = 0
    out = []
    for raw in raws:
        raw, status = all_func(raw, status)
        out.append(raw)
    header = create_header(out, header)
    text = header + '\n'
    for raw in out:
        if type(raw) == str:
            if raw.startswith('<stage type="delivery">'):
                raw = no_sp_in_stage(raw)
            text += raw.replace('</div><div>', '</div>\n<div>') + '\n'
    text += closer
    text = text.replace('&nbsp;', '').replace('<div>==', '<div><head>==').replace(' ==', ' ==</head>')
    x = open(filename[:-4] + '_out.xml', 'w', encoding='utf-8')
    x.write(text)
    x.close()


def cast_list(name_of_text):
    head = '''<profileDesc>
      <particDesc>
        <listPerson>'''
    end = '''</listPerson>
      </particDesc>
      <textClass>
        <keywords>
          <term type="genreTitle">Драма</term>
        </keywords>
      </textClass>
    </profileDesc>
    <revisionDesc>
      <listChange>
        <change who="#MatveyKolbasov" when="2017-05-20">Converted from Source</change>
      </listChange>
    </revisionDesc>
  </teiHeader>
  <text>
    <front>
      <div type="front">
        <head>''' + name_of_text + '''</head>
      </div>
    </front>
    <body>
      <p>ДЕЙСТВУЮЩИЕ ЛИЦА</p>
      <castList>'''
    name = input('Input name of cast_item: ')
    while True:
        if name != 'end':
            name, other = name.split('}}')
            pattern1 = '<person xml:id="' + translit(name, 'ru', reversed=True).replace(' ', '_').replace("'", '') + '''">
                <persName>''' + name + '''</persName>
              </person>'''
            pattern2 = '<castItem>' + name + other + '</castItem>\n'
            head += pattern1
            end += pattern2
            name = input('Input name of cast_item: ')
        else:
            print(head + end + '</castList>')
            break

def corrections(path):
    text = open(path, 'r', encoding='utf-8').read().replace('__', '_')
    title = translit(re.findall('<title type="main">(.*?)</title>', text)[0].replace(' ', '_'), 'ru', reversed=True)
    author = translit(re.findall('<author.*?>(.*?)</author>', text)[0].split()[-1], 'ru', reversed=True)
    text = text.replace("''", '')
    text = text.replace('<stage type="delivery">', '<stage type="delivery">(').replace('</stage>', ')</stage>').replace('((', '(').replace('))', ')')
    ids1 = re.findall('sp who="(.*?)"', text)
    ids = {i: i.replace('.', '').split('_') for i in ids1}
    for i in ids:
        new_id = ''
        for ii in ids[i]:
            new_id += ii[0].upper() + ii[1:]
        ids[i] = new_id
    for idd in ids:
        text = text.replace(idd, ids[idd])
    idds = ''
    ids = set(re.findall('<sp who=.*?</speaker>', text))
    for i in ids:
        print(i)
        i = i.replace('<sp who="#', '',).replace('"><speaker>', '$$').replace('</speaker>', '').split('$$')
        idds += '<person xml:id="' + i[0] + '">\n<persName>' + i[1] + '</persName></person>\n'
    text = re.sub('<particDesc>(.*?)</particDesc>', '<particDesc><listPerson>\n' + idds + '</listPerson></particDesc>', text, flags=re.S)
    text = text.replace('</speaker><l>', '</speaker><p>').replace('</l></sp>', '</p></sp>')
    x = open('DONE\\' + author + '_-_' + title + '.xml', 'w', encoding='utf-8')
    x.write(text)
    x.close()

    
#corrections("D:/ДрамКр/Type2/pre_done/Chehov_-_Jubilej.xml")
