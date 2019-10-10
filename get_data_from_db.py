from model import db, WellMonthRates, Base, WellWorkDates, WellFormation, WellPad, WellTRPressure, WellBHPPressure
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI
import plotly.graph_objects as go

def gaf_creation(x,y,name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name = name, # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))
    fig.show()
   
def get_month_well_data_from_merfond(bd_session, name):
    well_oil = []
    well_gas = []
    well_water = []
    well_injection = []
    dates = []
    for row in bd_session.query(WellMonthRates.date, 
                                WellMonthRates.oil,
                                WellMonthRates.gas,
                                WellMonthRates.water,
                                WellMonthRates.injection
                                ).filter_by(name=name).order_by(WellMonthRates.date):
        dates.append(row[0])
        well_oil.append(row[1])
        well_gas.append(row[2])
        well_water.append(row[3])
        well_injection.append(row[4])
        
    return (dates, well_oil, well_gas, well_water, well_injection)
'''
def get_well_data_from_merfond(bd_session, name):
    well_oil = []
    well_gas = []
    well_water = []
    well_injection = []
    dates = []
    for row in bd_session.query(WellMonthRates.date, 
                                WellMonthRates.oil,
                                WellMonthRates.gas,
                                WellMonthRates.water,
                                WellMonthRates.injection
                                ).filter_by(name=name).order_by(WellMonthRates.date):
        dates.append(row[0])
        well_oil.append(row[1])
        well_gas.append(row[2])
        well_water.append(row[3])
        well_injection.append(row[4])
        
    return (dates, well_oil, well_gas, well_water, well_injection)
'''
def get_field_data_from_merfond(bd_session):
    field_oil = []
    field_gas = []
    field_water = []
    field_injection = []
    dates = []
    for row in bd_session.query(WellMonthRates.date, 
                                func.sum(WellMonthRates.oil),
                                func.sum(WellMonthRates.gas),
                                func.sum(WellMonthRates.water),
                                func.sum(WellMonthRates.injection),
                                ).group_by(WellMonthRates.date):
        dates.append(row[0])
        field_oil.append(row[1])
        field_gas.append(row[2])
        field_water.append(row[3])
        field_injection.append(row[4])
        
    return (dates, field_oil, field_gas, field_water, field_injection)

if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    #dates, field_oil, field_gas, field_water, field_injection = get_field_data_from_merfond(session)
    dates, field_oil, field_gas, field_water, field_injection = get_month_well_data_from_merfond(session, "8148")
    gaf_creation(dates, field_oil,"Нефть")
    #gaf_creation(dates, field_gas,"Газ")
    gaf_creation(dates, field_water,"Вода")
    gaf_creation(dates, field_injection,"Закачка")    
    











