import os
import re
import glob
import csv
import xml.etree.ElementTree as ET
import networkx


def write_filename(file):
    """This function returns the filename without extension
    = the drama title"""
    file_name0 = file.split('/')[-1]
    return file_name0.split('.xml')[0]


def write_year(years_data, play_title):
    for row in years_data:
        if row['Play'] == play_title:
            return row['Year_of_creation']


def get_body(file):
    """This function parse the file at initial phase
    and gets its xml body or returns None if the file is invalid"""
    try:
        tree = ET.parse(file)
        tei = tree.getroot()
        text = tei[1]
        body = text.find('tei:body', ns)
        return body
    except:
        print('ERROR while parsing', file)
        return None


def get_divs(file):
    """This function gets all the divs of the play
    with their contents"""
    body = get_body(file)
    if body is not None:
        divs = body.findall('tei:div', ns)
        return divs
    else:
        return None


def num_of_scenes(file):
    """This function parses the divs and returns the number of scenes.
    If div contains divs,
    the number of these subdivs are added to the number of scenes,
    else number of scenes gets +1.
    If there were no divs in the xml, number of scenes is 1."""
    scenes_num = 0
    divs = get_divs(file)
    if divs is not None:
        for div in divs:
            subdivs = div.findall('tei:div', ns)
            if len(subdivs) == 0:
                scenes_num += 1
            else:
                scenes_num += len(subdivs)
    else:
        scenes_num = 'ERROR while parsing'
    if scenes_num == 0:
        scenes_num = 1
    return scenes_num


def num_of_char(file):
    """This function returns the number of characters in the file"""
    tei = open(file).read()
    characters = re.findall('<sp who="(.*?)">', tei)
    characters = set(characters)
    return str(len(characters))


def max_weight(file):
    """This function returns the max weight of characters connection in the play"""
    weights = []
    table = open(file)
    table = csv.DictReader(table, delimiter=';')
    for row in table:
        weights.append(int(row['Weight']))
    try:
        return max(weights)
    except:
        return 'empty weights'


def max_degree(file):
    """This function returns the max degree of some character in the play =
    how many of the other characters does a character
    ‘meet’/’speak to’ throughout the whole play"""
    degrees = dict()
    table = open(file)
    table = csv.DictReader(table, delimiter=';')
    for row in table:
        source = row['Source']
        target = row['Target']
        if source in degrees:
            degrees[source].append(target)
        else:
            degrees[source] = [target]
        if target in degrees:
            degrees[target].append(source)
        else:
            degrees[target] = [source]
    for el in degrees:
        degrees[el] = len(set(degrees[el]))
    try:
        return max(degrees.values())
    except:
        return 'empty weights'


def genre(file):
    try:
        tree = ET.parse(file)
        tei = tree.getroot()
        header = tei[0]
        profiledesc = header.find('tei:profileDesc', ns)
        textclass = profiledesc.find('tei:textClass', ns)
        if textclass is not None:
            keywords = textclass.find('tei:keywords', ns)
            if keywords is not None:
                genre = keywords.find('tei:term', ns)
                if genre is not None:
                    if 'subtype' in genre.attrib:
                        return genre.attrib['subtype']
                    else:
                        return 'other'
                else:
                    return 'no genre tag in file'
    except:
        print('ERROR while parsing', file)
        return None


years = open('./years_of_creation.csv')
years = csv.DictReader(years, delimiter=',')

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

table = open('calculations.csv', 'w', encoding='utf-8')
table.write('Play,Year_of_creation,Num_of_scenes,Num_of_char,Max_weight,Max_degree,Genre,\n')


ilibrary_tei_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                      'github desktop/RusDraCor/TEI/ilibrary/'
ilibrary_csv_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                    'github desktop/RusDraCor/TEI/current_CSV_files_extracted_from_TEI/ilibrary/'
wikisource_csv_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                     'github desktop/RusDraCor/TEI/current_CSV_files_extracted_from_TEI/wikisource/'
wikisource_tei_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                      'github desktop/RusDraCor/TEI/wikisource/'

all_tei = glob.glob(ilibrary_tei_path+'*.xml') + glob.glob(wikisource_tei_path+'*.xml')
all_csv = glob.glob(ilibrary_csv_path+'*.csv') + glob.glob(wikisource_csv_path+'*.csv')


data = list()
for file in all_tei:
    years = open('./years_of_creation.csv')
    years = csv.DictReader(years, delimiter=',')
    data_f = list()
    file_name = write_filename(file)
    print(file_name)
    data_f.append(file_name)
    data_f.append(write_year(years, file_name))
    data_f.append(num_of_scenes(file))
    data_f.append(num_of_char(file))
    for el in all_csv:
        if file_name in el:
            data_f.append(max_weight(el))
            data_f.append(max_degree(el))
    data_f.append(genre(file))
    data.append(data_f)

for d in data:
    for el in d:
        table.write(str(el) + ',')
    table.write('\n')


