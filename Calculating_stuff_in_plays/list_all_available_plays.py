import os

ilibrary_tei_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                    'github desktop/RusDraCor/TEI/ilibrary/'
wikisource_tei_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                      'github desktop/RusDraCor/TEI/wikisource/'

files = []

for file in os.listdir(ilibrary_tei_path):
    if file.endswith('.xml'):
        files.append(file)

for file in os.listdir(wikisource_tei_path):
    if file.endswith('.xml'):
        files.append(file)

for el in sorted(files):
    print(el)