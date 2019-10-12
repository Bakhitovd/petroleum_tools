from model import db, WellMonthRates, Base, WellWorkDates, WellFormation, WellPad, WellTRPressure, WellBHPPressure
import csv
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_work_dates(well_id, name, start_date, stop_date):
    well_start_date = session.query(WellWorkDates).filter_by(well_id = well_id, start_date=start_date).count()
    if not well_start_date:
        well_date = WellWorkDates(well_id=well_id, name=name, start_date=start_date, stop_date=stop_date)
        session.add(well_date)
"""
Функция для записи в локальную БД информацию о периодах работы скважин. Это необхродимо для 
корректного отображения информации  
"""
def save_form_dates(well_id, name, form, perf_form_date, shut_form_date):
    well_perf_date = session.query(WellFormation).filter_by(well_id = well_id, perf_form_date=perf_form_date).count()
    if not well_perf_date:
        well_date = WellFormation(well_id=well_id, name=name, form = form,
        perf_form_date=perf_form_date, shut_form_date=shut_form_date)
        session.add(well_date)
"""
Функция для записи в локальную БД информацию о том когда и на какой пласт работа та или инная скважина. 
Необходмо для корректного учета добытых углеводородов. 
"""

def save_well_pads(well_id, pad):
    well_pad = session.query(WellPad).filter_by(well_id = well_id).count()
    if not well_pad:
        well_date = WellPad(well_id=well_id, pad = pad)
        session.add(well_date)
"""
Функция для записи в локальную БД информацию о том с какого куста пробуренны скважины
"""

def save_tr_pressures(well_id, date, buff_pressure, annular_pressure, line_pressure):
    well_tr = session.query(WellTRPressure).filter_by(well_id = well_id, date=date).count()
    if not well_tr:
        well_date = WellTRPressure(well_id=well_id, date=date, buff_pressure=buff_pressure, 
        annular_pressure=annular_pressure, line_pressure=line_pressure)
        session.add(well_date)
"""
Функция для записи в локальную БД информацию о технологических режимах скважин, а именно буферное, затрубное
и линейное давление
"""

def save_bhp_pressures(well_id, date, bhp, form_pressure1, form_pressure2):
    well_bhp = session.query(WellBHPPressure).filter_by(well_id = well_id, date=date).count()
    if not well_bhp:
        well_date = WellBHPPressure(well_id=well_id, date=date, bhp=bhp, form_pressure1=form_pressure1, 
        form_pressure2=form_pressure2)
        session.add(well_date)
"""
Функция для записи в локальную БД информацию о технологических режимах скважин, а именно забойное давление
и пластовое даление 
"""
def save_month_rate(well_id, name, date, oil_day, gas_day, water_day, injection_day, gor, wc,
    oil, gas, water, injection, oil_cum, gas_cum, water_cum, injection_cum, work_time, work_time_cum):
    well_month_exists = session.query(WellMonthRates).filter_by(well_id = well_id, date = datetime.strptime(date, '%Y%m%d')).count()
    if not well_month_exists:
        well_date = WellMonthRates(
        well_id=well_id, 
        name=name,
        date=date, 
        oil_day=oil_day, 
        gas_day=gas_day,
        water_day=water_day,
        injection_day=injection_day,
        gor=gor,
        wc=wc,
        oil=oil,
        gas=gas,
        water=water,
        injection=injection,
        oil_cum=oil_cum,
        gas_cum=gas_cum,
        water_cum=water_cum,
        injection_cum=injection_cum,
        work_time=work_time, 
        work_time_cum=work_time_cum)
        session.add(well_date)
"""
Функция для записи в локальную БД месячных показателей работы скважин. Добыча нефти, газа, воды, закачка 
и время работы за месяц в часах.
"""
with open('ois\merfond.csv', 'r', encoding = 'utf-8-sig') as f:
    mer = csv.DictReader(f, delimiter = ';')   
    for line in mer:
        well_id = line['SK_1']
        if float(well_id) >= 500000000 and float(well_id) <= 500999900:
            save_month_rate(               
            well_id = well_id,
            name=line['S1_1'],
            date=line['DT_1'],
            oil_day=(float(line['N1_1'])+float(line['K1_1']))/(float(line['TR_1'])/24),
            gas_day=(float(line['G1_1'])+float(line['H1_1']))/(float(line['TR_1'])/24),
            water_day=float(line['V1_1'])/(float(line['TR_1'])/24),
            injection_day=float(line['Z1_1'])/(float(line['TR_1'])/24),
            gor=line['GF_1'],
            wc=line['SW_1'],
            oil=(float(line['N1_1'])+float(line['K1_1'])),
            gas=(float(line['G1_1'])+float(line['H1_1'])),
            water=line['V1_1'],
            injection=line['Z1_1'],
            oil_cum=(float(line['N3_1'])+float(line['K3_1'])),
            gas_cum=(float(line['G3_1'])+float(line['H3_1'])),
            water_cum=line['V3_1'],
            injection_cum=line['Z3_1'],
            work_time=line['TR_1'],
            work_time_cum=line['TEKSR_1']
                   )      
"""
Чтение файла с месячными показателями работы скважин. Добыча нефти, газа, воды, закачка 
и время работы за месяц в часах
"""
with open('ois\well_op.csv', 'r', encoding = 'utf-8-sig') as w:
    tr = csv.DictReader(w, delimiter = ';')   
    for line in tr:
        well_id = line['WELL_ID']
        if float(well_id) >= 500000000 and float(well_id) <= 500999900:
            save_tr_pressures(               
            well_id = well_id,
            date=line['CALC_DATE'],
            buff_pressure=line['BUFFER_PRESSURE'],
            annular_pressure=line['CASING_PRESSURE'],
            line_pressure=line['INLINE_PRESSURE']
            ) 
"""
Чтение файла с ТехРежимами
"""

with open('ois\well_layer_op.csv', 'r', encoding = 'utf-8-sig') as w:
    tr = csv.DictReader(w, delimiter = ';')   
    for line in tr:
        well_id = line['WELL_ID']
        if float(well_id) >= 500000000 and float(well_id) <= 500999900:
            save_bhp_pressures(  
            well_id = well_id,
            date=line['CALC_DATE'],
            bhp=line['LAYER_FLOW_PRESSURE_CALC'],
            form_pressure1=line['VDP_PRESSURE'],
            form_pressure2=line['INIT_SHUT_PRESSURE']
            )
"""
Чтение файла с забойным и пластовым давлением
"""

with open('ois\wellop.v_well_ful.csv', 'r', encoding = 'utf-8-sig') as p:  
    pads = csv.DictReader(p, delimiter = ';')
    for line in pads: 
        save_well_pads(
        well_id = line['WELL_ID'],
        pad = line['KS_1']
        )
"""
Чтение файла с кустами
"""

with open('ois\db70.rabpl.csv', 'r', encoding = 'utf-8-sig') as f:
    form = csv.DictReader(f, delimiter = ';')
    for line in form:
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
"""
Чтение файла с информацией о пластах на которые работали скважины
"""

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
"""
Чтение файла с периодами работы
"""


session.commit()       