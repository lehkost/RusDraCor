import re
import os

for root, dirs, files in os.walk('./wikisource_raws/1/'):
    for file in files:
        if file.endswith('.txt'):
            print(file)
            text = open('./wikisource_raws/1/' + file, 'r', encoding='utf-8')
            text_read = text.read()
            text.close()
            text_read = text_read.split('</div>')[0]
            text_read = re.sub('<poem', '\n<poem', text_read)
            text_read = re.sub('</poem', '\n</poem', text_read)
            text = open('./wikisource_raws/1_preprocessed/' + file, 'w', encoding='utf-8')
            text.write(text_read)
            text.close()
            text = open('./wikisource_raws/1_preprocessed/' + file, 'r', encoding='utf-8')
            text_read = text.readlines()
            text.close()
            text = open('./wikisource_raws/1_preprocessed/' + file, 'w', encoding='utf-8')
            for line in text_read:
                if line.lower().startswith('{{реплика') or line.lower().startswith('{{rem'):
                    # print(line)
                    razrs = re.findall('\{\{[Rr]azr2?\|.*?\}\}', line)
                    # print(razrs)
                    if len(razrs) != 0:
                        for el in razrs:
                            e = re.findall('\{\{[Rr]azr2?\|(.*?)\}\}', el)[0]
                            # print(el, e, '\n')
                            line = re.sub('\{\{[Rr]azr2?\|' + e + '\}\}', '<actor>' + e + '</actor>', line)
                    text.write(line)
                else:
                    text.write(line)