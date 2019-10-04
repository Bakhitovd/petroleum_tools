from model import db, WellMonthRates, Base, WellWorkDates, WellFormation, WellPad
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
    if not well_month_exists:
        well_date = WellMonthRates(well_id=well_id, name=name, date=date, oil=oil, gas=gas,
        water=water, injection=injection, work_time=work_time)
        session.add(well_date)

def save_work_dates(well_id, name, start_date, stop_date):
    well_start_date = session.query(WellWorkDates).filter_by(well_id = well_id, start_date=start_date).count()
    if not well_start_date:
        well_date = WellWorkDates(well_id=well_id, name=name, start_date=start_date, stop_date=stop_date)
        session.add(well_date)

def save_form_dates(well_id, name, form, perf_form_date, shut_form_date):
    well_perf_date = session.query(WellFormation).filter_by(well_id = well_id, perf_form_date=perf_form_date).count()
    if not well_perf_date:
        well_date = WellFormation(well_id=well_id, name=name, form = form,
        perf_form_date=perf_form_date, shut_form_date=shut_form_date)
        session.add(well_date)

def save_well_pads(well_id, pad):
    well_pad = session.query(WellPad).filter_by(well_id = well_id).count()
    if not well_pad:
        well_date = WellPad(well_id=well_id, pad = pad)
        session.add(well_date)


with open('ois\wellop.v_well_ful.csv', 'r', encoding = 'utf-8-sig') as p:  
    pads = csv.DictReader(p, delimiter = ';')
    for line in pads: 
        save_well_pads(
        well_id = line['WELL_ID\t'],
        pad = line['\tKS_1']
        )

with open('ois\db70.rabpl.csv', 'r', encoding = 'utf-8-sig') as f:
    form = csv.DictReader(f, delimiter = ';')
    for line in form:
        print(line)
        well_id = line['SK_1']
        if float(well_id) >= 500000000 and float(well_id) <= 500999900:
            if line['D2_1'] == '99999999':
                shut_form_date =  datetime.strptime('00010101', '%Y%m%d')
            else:
                shut_form_date = datetime.strptime(line['D2_1'], '%Y%m%d')
            save_form_dates(               
            well_id = well_id,
            form =line['PL_1'],
            name=line['S1_1'],
            perf_form_date = datetime.strptime(line['DZ_1'], '%Y%m%d'),   
            shut_form_date = shut_form_date
            )

with open('ois\db70.sost.csv', 'r', encoding = 'utf-8-sig') as f:
    sost = csv.DictReader(f, delimiter = ';')   
    for line in sost:
        well_id = line['SK_1']
        if float(well_id) >= 500000000 and float(well_id) <= 500999900 and line['SS_1'] == 'SS0001':
            if line['D2_1'] == '99999999':
                stop_date =  datetime.strptime('00010101', '%Y%m%d')
            else:
                stop_date = datetime.strptime(line['D2_1'], '%Y%m%d')
            save_work_dates(               
            well_id = well_id,
            name=line['S1_1'],
            start_date = datetime.strptime(line['DZ_1'], '%Y%m%d'),   
            stop_date = stop_date
            )      

with open('ois\merfond.csv', 'r', encoding = 'utf-8-sig') as f:
    mer = csv.DictReader(f, delimiter = ';')   
    for line in mer:
        well_id = line['SK_1']
        if float(well_id) >= 500000000 and float(well_id) <= 500999900:
            save_month_rate(               
            well_id = well_id,
            name=line['S1_1'],
            date=line['DT_1'],
            oil=line['N1_1'],
            gas=line['G1_1'],
            water=line['V1_1'],
            injection=line['Z1_1'],
            work_time=line['TEKSR_1']
                   )      


session.commit()       