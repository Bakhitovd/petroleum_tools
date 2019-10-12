from model import db, WellMonthRates, Base, WellWorkDates, WellFormation, WellPad, WellTRPressure, WellBHPPressure
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI
import plotly.graph_objects as go
from graf_examples import gaf_creation, get_well_data_from_merfond, get_field_data_from_merfond,get_form_data
import pandas as pd
from collections import defaultdict
import json
_default_data = lambda: defaultdict(_default_data)

if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = {}
    data = _default_data()
    for row_form in session.query(WellFormation):
        for row_pad in session.query(WellPad).filter_by(well_id=row_form.well_id):
            for row in session.query(WellMonthRates).filter_by(well_id=row_pad.well_id):
                if row.date >= row_form.perf_form_date and row.date < row_form.shut_form_date:
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['oil_day']=round(row.oil/(row.work_time/24), 2)
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['gas_day']=round(row.gas/(row.work_time/24), 2)
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['water_day']=round(row.water/(row.work_time/24), 2)
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['injection_day']=round(row.injection/(row.work_time/24), 2)
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['gor']=row.gor
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['wc']=row.wc
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['oil']=row.oil
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['gas']=row.gas
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['water']=row.water
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['injection']=row.injection
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['oil_cum']=row.oil_cum
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['gas_cum']=row.gas_cum
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['water_cum']=row.water_cum
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['injection_cum']=row.injection_cum
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['work_time']=row.work_time
                    data[str(row_form.form)][str(row_pad.pad)][str(row.name)][str(row.date)]['work_time_cum']=row.work_time_cum
    json.dumps(data)
    with open("data", "w", encoding="utf-8") as file:
        json.dump(data, file)







