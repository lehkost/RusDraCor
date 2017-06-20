import os
import re
import glob
import csv
import xml.etree.ElementTree as ET
import networkx as nx


csv_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                      'github desktop/RusDraCor/TEI/current_CSV_files_extracted_from_TEI/ilibrary/Chehov_Medved.csv'

def parse_graph(file):
    graph = list()
    table = open(file)
    table = csv.DictReader(table, delimiter=';')
    for row in table:
        line = row['Source'] + ' ' + row['Target'] + ' ' + "{'weight':" + row['Weight'] + "}"
        graph.append(line)
    return graph


def density(file):
    graph = parse_graph(file)
    parsed_graph = nx.parse_edgelist(graph, nodetype = str)
    density = nx.density(parsed_graph)
    print(nx.node_connectivity(parsed_graph))
    return density


print(density(csv_path))

def write_filename(file):
    """This function returns the filename without extension
    = the drama title"""
    file_name0 = file.split('/')[-1]
    return file_name0.split('.xml')[0]


def get_genre(file):
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

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

play_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/' \
                      'github desktop/RusDraCor/TEI/ilibrary/Chehov_Vishnevyi_sad.xml'
