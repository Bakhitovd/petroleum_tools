from model import db, WellMonthRates, Base, WellWorkDates, WellFormation, WellPad, WellTRPressure, WellBHPPressure
import csv
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI
import plotly.graph_objects as go
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
#Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
field_oil = []
field_gas = []
dates = []

for row in session.query(WellMonthRates.date, func.sum(WellMonthRates.oil)).group_by(WellMonthRates.date):
    field_oil.append(row[1])
    dates.append(row[0])

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=field_oil,
    name = '<b></b> Oil', # Style name/legend entry with html tags
    connectgaps=True # override default to connect the gaps
))
fig.show()
   










