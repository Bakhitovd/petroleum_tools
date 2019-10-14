import csv
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
#db = SQLAlchemy()
#from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Boolean, Numeric, ForeignKey
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WellWorkDates(Base):
    __tablename__ = 'WellWorkDates'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)# id скважины необходим потому что в названии скважн часто еть буквы
    name = db.Column(db.String, nullable=False)#геологическое имя скважины
    start_date = db.Column(db.DateTime, nullable=False)# дата запука скажины 
    stop_date = db.Column(db.DateTime, nullable=False)#дата остановки
    def __repr__(self):
        return f'Cкважина: {self.name}, дата запуска : {self.start_date}, дата остановки : {self.stop_date}'
"""
Описание таблицы с датами работы скважин. Иногда скважины останавливаются, иногда надолго.
"""
class WellPad(Base):
    __tablename__ = 'WellPad'   
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)# id скважины
    pad = db.Column(db.String, nullable=True)#номер куста с которого пробурена скважина
"""
    Важная информация.Номер куста,хранится в отдельной таблице. 
"""
class WellFormation(Base):
    __tablename__ = 'WellFormation'   
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False) #id скважины
    name = db.Column(db.String, nullable=False)#геологическое имя скважины
    form = db.Column(db.String, nullable=False)#Идентификатор пласта на который пробурена скважина
    perf_form_date = db.Column(db.DateTime, nullable=False)#Дата перфорации на пласт
    shut_form_date = db.Column(db.DateTime, nullable=False)#дата отсечения
"""
Таблица с датами работы скважин на тот или инной пласт. Обычно скважина пробурена на конкретный пласт
и работает на этот пласт всю жизнь. Но бывает такое что скважину перебуривают или перестреливают на 
другой пласт и тогда возникают неудобства с учетом и анализом. Поэтому лучше иметь такую таблицу. 
"""
class WellMonthRates(Base):  
    __tablename__ = 'WellMonthRates'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)#месяц за который приведена добыча  
    gor = db.Column(db.Float, nullable=True)# Средний газовый фактор
    wc = db.Column(db.Float, nullable=True)#Средняя обводненность 
    oil = db.Column(db.Float, nullable=True)#число тонн нефти добытой за этот месяц
    gas = db.Column(db.Float, nullable=True)#число кубометров добытого попутного нефтянного газа
    water = db.Column(db.Float, nullable=True)#число кубометров добытой пластовой воды
    injection = db.Column(db.Float, nullable=True)#число закачанной воды за месяц  
    oil_cum = db.Column(db.Float, nullable=True)#накопленное число тонн нефти добытой за этот месяц
    gas_cum = db.Column(db.Float, nullable=True)#накопленное число кубометров добытого попутного нефтянного газа
    water_cum = db.Column(db.Float, nullable=True)#накопленное число кубометров добытой пластовой воды
    injection_cum = db.Column(db.Float, nullable=True)#накопленное число закачанной воды за месяц 
    work_time = db.Column(db.Float, nullable=True)#время работы за месяц
    work_time_cum = db.Column(db.Float, nullable=True)#накопленное время работы

    def __init__(self,well_id, name, date, gor, wc,
    oil, gas, water, injection, oil_cum, gas_cum, water_cum, injection_cum, work_time, work_time_cum):
        self.well_id = well_id.strip()
        self.name = name.strip()
        try:
            self.date = date.strip()
            self.date = datetime.strptime(date, '%Y%m%d')
        except:
            self.date=date           
        self.gor = float(gor)
        self.wc = float(wc)
        self.oil = float(oil)
        self.gas = float(gas)
        self.water = float(water)
        self.injection = float(injection) 
        self.oil_cum = float(oil_cum)
        self.gas_cum = float(gas_cum)
        self.water_cum = float(water_cum)
        self.injection_cum = float(injection_cum)
        self.work_time = float(work_time)
        self.work_time_cum = float(work_time_cum)
    def __repr__(self):
        return (f'Cкважина: {self.name}, дата: {self.date}, нефть т/мес: {self.oil},\
        газ м3/мес: {self.gas}, вода м3/мес: {self.water}, время работы:  {self.work_time}')    
"""
Таблица с информацией о том сколько чего добыла(если это добываюшая) либо закачала(если это нагнетательная)
скважина за месяц.
"""

class WellTRPressure(Base):
    __tablename__ = 'WellTRPressure'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)#месяц за который приведены ТехРежимы
    annular_pressure = db.Column(db.Float, nullable=True)# затрубное давление
    buff_pressure = db.Column(db.Float, nullable=True)#буферное давление
    line_pressure = db.Column(db.Float, nullable=True)#линейное давление

    def __init__(self,well_id, date, buff_pressure, annular_pressure, line_pressure):
        self.well_id = well_id.strip()
        try:
            self.date = date.strip()
            self.date = datetime.strptime(date, '%d.%m.%Y')
        except:
            self.date=date
        try:
            self.annular_pressure = float(annular_pressure)
        except:
            self.annular_pressure = 0 
        try:        
            self.buff_pressure = float(buff_pressure)
        except:
            self.buff_pressure = 0
        
        try:
            self.line_pressure = float(buff_pressure)      
        except:
            self.line_pressure = 0


class WellBHPPressure(Base):
    __tablename__ = 'WellBHPPressure'
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)#месяц за который приведены ТехРежимы
    bhp = db.Column(db.Float, nullable=True)#забойное давление 
    form_pressure1 = db.Column(db.Float, nullable=True)#Пластовое давление, приводится справочно
    form_pressure2 = db.Column(db.Float, nullable=True)#пластовое давление из другого источника

    def __init__(self,well_id, date, bhp, form_pressure1, form_pressure2):
        self.well_id = well_id.strip()
        try:
            self.date = date.strip()
            self.date = datetime.strptime(date, '%d.%m.%Y')
        except:
            self.date=date     
        try:
            self.bhp = float(bhp)
        except:
            self.bhp = 0
        try:        
            self.form_pressure1 = float(form_pressure1)
        except:
            self.form_pressure1 = 0

        try:        
            self.form_pressure2 = float(form_pressure2)
        except:
            self.form_pressure2 = 0    

"""
В этих двух таблицах представленна информация о технологических режимах работы скважин.
ТехРежимы это набор параметров на которых данная скважина эксплуатировалась в данный месяц.
Мы используем именно их потому что так удобнее чем брать замеры за весь месяц и усреднять.
"""