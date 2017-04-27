import os
import re

table = open('num_of_characters_in_plays.csv', 'w', encoding='utf-8')

for file in os.listdir('./ready_TEI/'):
    if file.endswith('.xml'):
        table.write(file.split('.xml')[0] + ',')
        tei = open('./ready_TEI/' + file).read()
        characters = re.findall('<sp who="(.*?)">', tei)
        characters = set(characters)
        table.write(str(len(characters)) + '\n')
table.close()