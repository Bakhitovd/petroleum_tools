import csv
from datetime import datetime, timedelta, date
from classes import WellsStartDates
wells = {}
with open('merfond.csv', 'r', encoding = 'utf-8') as f:
    mer = csv.reader(f, delimiter = ';')
    for line in mer:
        print(' ', line)
    #    well_id = line.SK_1
     #   well_name = line.S1_1
     #   wells.append({                                #добавление словаря в список словарей
     #           'well_id' : well_id,
     #           'well_name' : well_name
     #       })