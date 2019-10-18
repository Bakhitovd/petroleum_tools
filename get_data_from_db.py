from model import db, WellMonthRates, Base, WellWorkDates, WellFormation, WellPad, WellTRPressure, WellBHPPressure
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI
import plotly.graph_objects as go
import pandas as pd
from collections import defaultdict
import json
_default_data = lambda: defaultdict(_default_data)



def get_data(db_session):    
    
    data = {}
    data = _default_data()
    for row_form in db_session.query(WellFormation):
        for row_pad in db_session.query(WellPad).filter_by(well_id=row_form.well_id):
            for row in db_session.query(WellMonthRates).filter_by(well_id=row_pad.well_id):
                if row.date >= row_form.perf_form_date and row.date < row_form.shut_form_date:
                    true_date = row.date.date()
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(true_date)]['oil_day']=round(row.oil/(row.work_time/24), 2)
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(true_date)]['gas_day']=round(row.gas/(row.work_time/24), 2)
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(true_date)]['water_day']=round(row.water/(row.work_time/24), 2)
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(true_date)]['injection_day']=round(row.injection/(row.work_time/24), 2)
                    sets = ['oil', 'gas', 'water', 'injection', 'gor', 'wc', 'oil_cum', 'gas_cum', 'water_cum', 'injection_cum', 'work_time', 'work_time_cum']
                    for i in sets:
                        data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(true_date)][i]=getattr(row,i)
           
            for row in db_session.query(WellTRPressure).filter_by(well_id=row_pad.well_id):
                tr_date = row.date.date()
                true_date = datetime(tr_date.year, tr_date.month, 1).date()
                well_name_row = db_session.query(WellFormation).filter_by(well_id=row.well_id).first()
                well_name = str(well_name_row.name).strip()
                data[str(row_form.form)][str(row_pad.pad)][well_name][str(true_date)]['buff_pressure']=row.buff_pressure
                data[str(row_form.form)][str(row_pad.pad)][well_name][str(true_date)]['annular_pressure']=row.annular_pressure
                data[str(row_form.form)][str(row_pad.pad)][well_name][str(true_date)]['line_pressure']=row.line_pressure
           
            for row in db_session.query(WellBHPPressure).filter_by(well_id=row_pad.well_id):
                tr_date = row.date.date()
                true_date = datetime(tr_date.year, tr_date.month, 1).date()
                well_name_row = db_session.query(WellFormation).filter_by(well_id=row.well_id).first()
                well_name = str(well_name_row.name).strip()
                data[str(row_form.form)][str(row_pad.pad)][well_name][str(true_date)]['bhp']=row.bhp
                data[str(row_form.form)][str(row_pad.pad)][well_name][str(true_date)]['form_pressure1']=row.form_pressure1

    return (data) 
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()
data1 = get_data(db_session)


json.dumps(data1)
with open("data", "w", encoding="utf-8") as file:
    json.dump(data1, file)






