from model import db, WellMonthRates, Base, WellWorkDates, WellFormation, WellPad, WellTRPressure, WellBHPPressure
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI
import plotly.graph_objects as go
from graf_examples import gaf_creation, get_well_data_from_merfond, get_field_data_from_merfond,get_form_data
import pandas as pd
from collections import defaultdict
_default_data = lambda: defaultdict(_default_data)

if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    oil = []
    gas = []
    water = []
    injection = []
    data={}
    pad={}
    pad = data = _default_data()
    for row in session.query(WellPad.pad, WellPad.well_id):
        pad[row.pad][row.well_id]='true'
    print(pad)
        








