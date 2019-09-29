from model import db, WellMonthRates
import csv
from datetime import datetime, timedelta
from classes import WellsStartDates, WellMonthRates
wells_month = []
with open('merfond.csv', 'r', encoding = 'utf-8') as f:
    mer = csv.DictReader(f, delimiter = ';')
    
    for line in mer:
        wells_month.append({                                #добавление словаря в список словарей
                'date' : line['\ufeffDT_1'],
                'well_id' : line['SK_1'],
                'name' : line['S1_1'],
                'oil' : line['N1_1'],
                'gas' : line['G1_1'],
                'water' : line['V1_1'],
                'injection' : line['Z1_1'],
                'work_time' : line['TEKSR_1']
                        })      

#print(wells_month[1])                          

def save_measurement(well_id, name, date, oil, gas, water, injection, work_time):
  # well_month_exists = WellMonthRates.query.filter(WellMonthRates.well_id == wells_month.well_id and WellMonthRates.name = wells_month.date).count()
   #print(well_month_exists)
  # if not well_month_exists:
    well_date = WellMonthRates(name=wells_month.name, well_id=wells_month.well_id, date=wells_month.date)
    db.session.add(well_date)
    db.session.commit()             