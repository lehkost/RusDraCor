import os
import csv


for file in os.listdir('./ready_CSV/'):
    if file.endswith('.csv'):
        print(file)
        dict = {}
        degrees = open('./ready_CSV/' + file)
        degrees = csv.DictReader(degrees, delimiter=';')
        for row in degrees:
            source = row['Source']
            target = row['Target']
            if source in dict:
                dict[source].append(target)
            else:
                dict[source] = [target]
            if target in dict:
                dict[target].append(source)
            else:
                dict[target] = [source]
        for el in dict:
            dict[el] = len(set(dict[el]))
        try:
            print(max(dict.values()))
        except:
            print('empty weights')