import os
import csv


for file in os.listdir('./ready_CSV/'):
    if file.endswith('.csv'):
        weights = []
        degrees = open('./ready_CSV/' + file)
        degrees = csv.DictReader(degrees, delimiter=';')
        for row in degrees:
            weights.append(row['Weight'])
        try:
            print(max(weights))
        except:
            print('empty weights')