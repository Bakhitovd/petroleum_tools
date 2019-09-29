import csv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
db = SQLAlchemy()

class WellsStartDates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    pad = db.Column(db.String, nullable=False)
    form = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Cкважина: {self.name}, куст: {self.pad},\
        плаcт: {self.form}, дата запуска по фонду: {self.start_date}'


class WellMonthRates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    well_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    oil = db.Column(db.Float, nullable=True)
    gas = db.Column(db.Float, nullable=True)
    water = db.Column(db.Float, nullable=True)
    injection = db.Column(db.Float, nullable=True)
    work_time = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return (f'Cкважина: {self.name}, дата: {self.date}, нефть т/мес: {self.oil},\
        газ м3/мес: {self.gas}, вода м3/мес: {self.water}, время работы:  {self.work_time}')    


class WellTRPressure(db.Model):
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


