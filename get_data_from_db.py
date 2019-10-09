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
   
def get_oil_from_merfond(bd_session, array_y, date_array):
    for row in bd_session.query(WellMonthRates.date, func.sum(WellMonthRates.oil)).group_by(WellMonthRates.date):
        array_y.append(row[1])
        date_array.append(row[0])
    return (date_array, array_y)

if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    field_oil = []
    dates = []
    dates, field_oil = get_oil_from_merfond(session, field_oil, dates)
    gaf_creation(dates, field_oil,"Нефть")    
    











