from model import db, WellMonthRates, Base
import csv
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
  
def save_month_rate(well_id, name, date, oil, gas, water, injection, work_time):
    well_month_exists = session.query(WellMonthRates).filter_by(well_id = well_id, date = datetime.strptime(date, '%Y%m%d')).count()
    print(well_month_exists)
    if not well_month_exists:
        well_date = WellMonthRates(well_id=well_id, name=name, date=date, oil=oil, gas=gas,
        water=water, injection=injection, work_time=work_time)
        session.add(well_date)
    

with open('merfond.csv', 'r', encoding = 'utf-8') as f:
    mer = csv.DictReader(f, delimiter = ';')   
    for line in mer:
        save_month_rate(               
        well_id = line['SK_1'],
        name=line['S1_1'],
        date=line['\ufeffDT_1'],
        oil=line['N1_1'],
        gas=line['G1_1'],
        water=line['V1_1'],
        injection=line['Z1_1'],
        work_time=line['TEKSR_1']
               )      
    

session.commit()       