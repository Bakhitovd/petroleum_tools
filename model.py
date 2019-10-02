import csv
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
#db = SQLAlchemy()
#from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Boolean, Numeric, ForeignKey
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WellsStartDates(Base):
    __tablename__ = 'WellsStartDates'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    pad = db.Column(db.String, nullable=False)
    form = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Cкважина: {self.name}, куст: {self.pad},\
        плаcт: {self.form}, дата запуска по фонду: {self.start_date}'


class WellMonthRates(Base):  #Добавить 
    __tablename__ = 'WellMonthRates'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    oil = db.Column(db.Float, nullable=True)
    gas = db.Column(db.Float, nullable=True)
    water = db.Column(db.Float, nullable=True)
    injection = db.Column(db.Float, nullable=True)
    work_time = db.Column(db.Float, nullable=True)
    
    def __init__(self,well_id, name, date, oil, gas, water, injection, work_time):
        self.well_id = well_id.strip()
        self.name = name.strip()
        try:
            self.date = date.strip()
            self.date = datetime.strptime(date, '%Y%m%d')
        except:
            self.date=date          
        self.oil = float(oil)
        self.gas = float(gas)
        self.water = float(water)
        self.injection = float(injection)
        self.work_time = float(work_time)

    def __repr__(self):
        return (f'Cкважина: {self.name}, дата: {self.date}, нефть т/мес: {self.oil},\
        газ м3/мес: {self.gas}, вода м3/мес: {self.water}, время работы:  {self.work_time}')    


class WellTRPressure(Base):
    __tablename__ = 'WellTRPressure'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    bhp = db.Column(db.Float, nullable=True)
    buff_pressure = db.Column(db.Float, nullable=True)
    annular_pressure = db.Column(db.Float, nullable=True)
    line_pressure = db.Column(db.Float, nullable=True)
    form_pressure = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'Cкважина: {self.name}, дата: {self.date}, нефть т/мес: {self.bhp}, \
        буферное давление: {self.buff_pressure}, затрубное давление: {self.annular_pressure}, \
        линейное давление:  {self.line_pressure}, пластовое давление {self.form_pressure}'    


