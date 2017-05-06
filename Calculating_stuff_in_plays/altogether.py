import os
import re
import xml.etree.ElementTree as ET
import csv

csv_path = './ready_CSV/'
tei_path = './ready_TEI/'

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

table = open('calculations.csv', 'w', encoding='utf-8')


def write_filenames(file):
    """This function returns the filename without extension
    = the drama title"""
    return file.split('.xml')[0]


def num_of_char(file, tei_path):
    """This function returns the number of characters in the file"""
    tei = open(tei_path + file).read()
    characters = re.findall('<sp who="(.*?)">', tei)
    characters = set(characters)
    return str(len(characters))


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


def num_of_scenes(path):
    """This function parses the divs and returns the number of scenes.
    If div contains divs,
    the number of these subdivs are added to the number of scenes,
    else number of scenes gets +1.
    If there were no divs in the xml, number of scenes is 1."""
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


def max_degree(file):
    weights = []
    degrees = open('./ready_CSV/' + file)
    degrees = csv.DictReader(degrees, delimiter=';')
    for row in degrees:
        weights.append(row['Weight'])
    try:
        return max(weights)
    except:
        return 'empty weights'







