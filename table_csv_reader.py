import csv
from datetime import datetime, timedelta, date
from classes import WellsStartDates
wells_month = []
with open('merfond.csv', 'r', encoding = 'utf-8') as f:
    mer = csv.DictReader(f, delimiter = ';')
    for line in mer:
        wells_month.append({                                #добавление словаря в список словарей
                'well_id' : line['SK_1'],
                'well_name' : line['S1_1']
            })

print (wells_month)
