import os
import csv
import glob


def write_filename(file):
    """This function returns the filename without extension
    = the drama title"""
    file_name0 = file.split('/')[-1]
    return file_name0.split('.xml')[0]

years = open('./years_of_creation.csv')
years = csv.DictReader(years, delimiter=',')

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


for file in all_tei:
    file = write_filename(file)
    print(file)
    for row in years:
        if row['Play'] == file:
            print(row['Year_of_creation'])

for row in years:
        if row['Play'] == 'Chehov_Chaika':
            print('YES')
            print(row['Year_of_creation'])