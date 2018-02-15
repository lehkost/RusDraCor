import re
import glob
import csv
import xml.etree.ElementTree as ET
import networkx as nx


def write_filename(file): # folder
    """This function returns the filename without extension
    = the drama title"""
    file_name0 = file.split('/')[-1]
    return file_name0.split('.xml')[0]


def write_year(years_data, play_title): # new CSV
    """Uses new CSV."""
    for row in years_data:
        if row['Play'] == play_title:
            return row['Year_of_creation']


def get_date(file): # TEI
    """This function extracts the date of the drama."""
    tei = open(file, 'r', encoding='utf-8').read()
    try:
        date_print = int(re.search('<date type="print" when="(.*?)"', tei).group(1))
    except:
        try:
            date_print = int(re.search('<date type="print" .*?notAfter="(.*?)"', tei).group(1))
        except:
            date_print = None
    try:
        date_premiere = int(re.search('<date type="premiere" when="(.*?)"', tei).group(1))
    except:
        try:
            date_premiere = int(re.search('<date type="premiere" .*?notAfter="(.*?)">', tei).group(1))
        except:
            date_premiere = None
    try:
        date_written = int(re.search('<date type="written" when="(.*?)"', tei).group(1))
    except:
        try:
            date_written = int(re.search('<date type="written" .*?notAfter="(.*?)">', tei).group(1))
        except:
            date_written = None

    if date_print and date_premiere:
        date_definite = min(date_print, date_premiere)
    elif date_premiere:
        date_definite = date_premiere
    else:
        date_definite = date_print
    if date_written and date_definite:
        if date_definite - date_written > 10:
            date_definite = date_written
    elif date_written and not date_definite:
        date_definite = date_written

    return date_definite


def get_body(file): # TEI
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


def get_divs(file): # TEI
    """This function gets all the divs of the play
    with their contents"""
    body = get_body(file)
    if body is not None:
        divs = body.findall('tei:div', ns)
        return divs
    else:
        return None


def num_of_segments(file): # TEI
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


def num_of_acts(file): # TEI
    tei = open(file, 'r', encoding='utf-8').read()
    num_of_acts = len(re.findall('<div type="act">', tei))
    return num_of_acts


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


def max_degree(file): # CSV
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


def genre(file): # TEI
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


def parse_graph(file): # CSV
    graph = list()
    table = open(file)
    table = csv.DictReader(table, delimiter=';')
    for row in table:
        line = row['Source'] + ' ' + row['Target'] + ' ' + "{'weight':" + row['Weight'] + "}"
        graph.append(line)
    return graph


def graph_metrics(file): # CSV
    graph = parse_graph(file)
    parsed_graph = nx.parse_edgelist(graph, nodetype=str)
    density = nx.density(parsed_graph)
    num_of_char = nx.number_of_nodes(parsed_graph)
    degrees = nx.degree(parsed_graph)
    if len(set(degrees.values())) != 1:
        max_degree_chars = [k for k, v in degrees.items() if v == max(degrees.values())]
        max_degree_chars_str = '|'.join(max_degree_chars)
    else:
        max_degree_chars_str = None
    try:
        avg_clust_coeff = round(nx.average_clustering(parsed_graph), 2)
    except:
        avg_clust_coeff = None
    return density, num_of_char, max_degree_chars_str, avg_clust_coeff


def gender_proportion(file): # TEI
    tei = open(file, 'r', encoding='utf-8').read()
    text = re.search('<text>(.*?)</text>', tei, re.DOTALL).group(1)
    gender_dict = {}
    participants = re.findall('<person xml:id="(.*?)" sex="(.*?)">', tei)
    for participant in participants:
        gender_dict[participant[0]] = participant[1]
    female = 0
    male = 0
    for participant in gender_dict:
        gender = gender_dict[participant]
        num_of_speech_acts = len(re.findall('#' + participant, text))
        if gender == 'FEMALE':
            female += num_of_speech_acts
        if gender == 'MALE':
            male += num_of_speech_acts
    try:
        return female, male, round(female/(female+male), 2), round(male/(female+male), 2)
    except:
        return female, male, "None", "None"


def gender_words(file): # TEI
    tei = open(file, 'r', encoding='utf-8').read()
    text = re.search('<text>(.*?)</text>', tei, re.DOTALL).group(1)
    gender_dict = {}
    ch_words_dict = {}
    female = 0
    male = 0
    participants = re.findall('<person xml:id="(.*?)" sex="(.*?)">', tei)
    for participant in participants:
        gender_dict[participant[0]] = participant[1]
    for char in gender_dict:
        ch_words_dict[char] = 0
        tag = '<sp who="#' + char
        spacts = re.findall(tag + '.*?>(.*?)</sp>', tei, re.DOTALL)
        for spact in spacts:
            #print(spact)
            spact = re.sub('<speaker>.*?</speaker>', '', spact, re.DOTALL)
            spact = re.sub('<stage.*?>.*?</stage>', '', spact, re.DOTALL)
            spact = re.sub('<p>', '', spact, re.DOTALL)
            spact = re.sub('</p>', '', spact, re.DOTALL)
            spact = re.sub('[-\.,\?!:;\(\)–]', '', spact, re.DOTALL)
            #print(spact.split(), len(spact.split()))
            ch_words_dict[char] += len(spact.split())
    for ch in ch_words_dict:
        if gender_dict[ch] == 'FEMALE':
            female += ch_words_dict[ch]
        if gender_dict[ch] == 'MALE':
            male += ch_words_dict[ch]
    female_repls = gender_proportion(file)[0]
    male_repls = gender_proportion(file)[1]
    if female_repls != 0 and male_repls != 0:
        return round(female/gender_proportion(file)[0], 2),round(male/gender_proportion(file)[1], 2),\
            round(female/(female+male), 2), round(male/(female+male), 2)
    else:
        if female_repls == 0:
            try:
                return 0, round(male/gender_proportion(file)[1], 2),\
                    round(female/(female+male), 2), round(male/(female+male), 2)
            except:
                return 0, 'None', 'None', 'None'
        if male_repls == 0:
            try:
                return round(female/gender_proportion(file)[0], 2), 0,\
                    round(female/(female+male), 2), round(male/(female+male), 2)
            except:
                return 'None', 0, 'None', 'None'


def gender_words_fail(file): # TEI
    gender_words_dict0 = {}
    gender_words_dict1 = {}
    divs = get_divs(file)
    if divs is not None:
        for div in divs:
            sps = div.findall('tei:sp', ns)
            if sps is not None:
                for sp in sps:
                    speaker = re.sub('#', '', sp.attrib['who'])
                    #print(speaker)
                    gender_words_dict0[speaker] = 0
                    text = sp.findall('tei:l', ns)
                    if len(text) != 0:
                        for t in text:
                            gender_words_dict0[speaker] += len(t.text.split())
                    else:
                        text = sp.findall('tei:lg:l', ns)
                        if len(text) != 0:
                            for t in text:
                                gender_words_dict0[speaker] += len(t.text.split())
                        else:
                            text = sp.findall('tei:p', ns)
                            if len(text) != 0:
                                for t in text:
                                    gender_words_dict0[speaker] += len(t.text.split())
                    for ch in gender_words_dict0:
                        if ch in gender_words_dict1:
                            gender_words_dict1[ch] += gender_words_dict0[ch]
                        else:
                            gender_words_dict1[ch] = gender_words_dict0[ch]
            else:
                subdivs = div.findall('tei:div', ns)
                for subdiv in subdivs:
                    sps = subdiv.findall('tei:sp', ns)
                    if sps is not None:
                        for sp in sps:
                            speaker = re.sub('#', '', sp.attrib['who'])
                            #print(speaker)
                            gender_words_dict0[speaker] = 0
                            text = sp.findall('tei:l', ns)
                            if len(text) != 0:
                                for t in text:
                                    gender_words_dict0[speaker] += len(t.text.split())
                            else:
                                text = sp.findall('tei:lg:l', ns)
                                if len(text) != 0:
                                    for t in text:
                                        gender_words_dict0[speaker] += len(t.text.split())
                                else:
                                    text = sp.findall('tei:p', ns)
                                    if len(text) != 0:
                                        for t in text:
                                            gender_words_dict0[speaker] += len(t.text.split())
                            for ch in gender_words_dict0:
                                if ch in gender_words_dict1:
                                    gender_words_dict1[ch] += gender_words_dict0[ch]
                                else:
                                    gender_words_dict1[ch] = gender_words_dict0[ch]

                #for t in text:
                    #print(t.text)
    print(gender_words_dict1)



ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

tei_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/github desktop/dracor-rusdracor/tei/'
csv_path = '/Users/IrinaPavlova/Desktop/Uni/Бакалавриат/2015-2016/Programming/github desktop/RusDraCor/Ira_Scripts/CSV/'

all_tei = glob.glob(tei_path+'*.xml')
all_csv = glob.glob(csv_path+'*.csv')

table = open('NEW_calculations.csv', 'w', encoding='utf-8')
table.write('Play,Year_of_creation,Num_of_segments,Num_of_acts,Female_part,Male_part,Female_words,Male_words,'
            'Mean_len_fem_re,Mean_len_male_re,'
            'Max_weight,Max_degree,Density,Num_of_char,'
            'Chars_with_max_degree,Average_clust_coef,Genre,\n')

data = list()
for file in all_tei:
    data_f = list()
    file_name = write_filename(file)
    print(file_name)
    data_f.append(file_name)
    data_f.append(get_date(file))
    data_f.append(num_of_segments(file))
    data_f.append(num_of_acts(file))
    data_f.append(gender_proportion(file)[2])
    data_f.append(gender_proportion(file)[3])
    data_f.append(gender_words(file)[2])
    data_f.append(gender_words(file)[3])
    data_f.append(gender_words(file)[0])
    data_f.append(gender_words(file)[1])
    #if gender_words(file)[0] > gender_words(file)[1]:
        #print('fem words are longer!', gender_words(file)[0], gender_words(file)[1])
    for el in all_csv:
        if file_name in el:
            data_f.append(max_weight(el))
            data_f.append(max_degree(el))
            data_f.append(round(graph_metrics(el)[0], 2))
            data_f.append(graph_metrics(el)[1])
            data_f.append(graph_metrics(el)[2])
            data_f.append(graph_metrics(el)[3])
    print('\n\n')
    data_f.append(genre(file))
    data.append(data_f)

for d in data:
    for el in d:
        table.write(str(el) + ',')
    table.write('\n')

table.close()
table = open('NEW_calculations.csv', 'r', encoding='utf-8')
table_new = re.sub(',\n', '\n', table.read())
table.close()

table = open('NEW_calculations.csv', 'w', encoding='utf-8')
table.write(table_new)
table.close()