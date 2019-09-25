import csv
from datetime import datetime, timedelta, date
class WellsStartDates:
    def __init__(self, id, name, pad, form, start_date):
        self.id = id.strip()
        if not len(self.id) == 9:
              raise ValueError('Некорректный id скважины')
        self.name = name.strip()
        self.pad = pad.strip()
        if str(self.pad) == '0':
            self.pad = 'б/к'
        self.form = form.strip()
        if isinstance(start_date, str):
            self.start_date = start_date.strip()
            self.start_date = datetime.strptime(start_date, '%d%m%Y') #добавить обработку даты!!!!!!!!!!!!!!!!!!!!!!

    def __repr__(self):
        return f'Cкважина: {self.name}, куст: {self.pad},\
        плаcт: {self.form}, дата запуска по фонду: {self.start_date}'


class WellMonthRates:
    def __init__(self,id, name, date, oil, gas, water, injection, work_time):
        self.id = id.strip()
        if not len(self.id) == 9:
              raise ValueError('Некорректный id скважины')
        self.name = name.strip()
        if isinstance(date, str):
            self.date = date.strip()
            self.date = datetime.strptime(date, '%d%m%Y')        
        self.oil = float(oil)
        self.gas = float(gas)
        self.water = float(water)
        self.injection = float(injection)
        self.work_time = float(work_time)

    def __repr__(self):
        return (f'Cкважина: {self.name}, дата: {self.date}, нефть т/мес: {self.oil},\
        газ м3/мес: {self.gas}, вода м3/мес: {self.water}, время работы:  {self.work_time}')    


class WellTRPressure:
    def __init__(self,id, name, date, bhp, buff_pressure, annular_pressure, line_pressure, form_pressure):
        self.id = id.strip()
        if not len(self.id) == 9:
              raise ValueError('Некорректный id скважины')
        self.name = name.strip()
        if isinstance(date, str):
            self.date = date.strip()
            self.date = datetime.strptime(date, '%d%m%Y')
        self.bhp = float(bhp)
        self.buff_pressure = float(buff_pressure)
        self.annular_pressure = float(annular_pressure)
        self.line_pressure = float(line_pressure)
        self.form_pressure = float(form_pressure)

    def __repr__(self):
        return f'Cкважина: {self.name}, дата: {self.date}, нефть т/мес: {self.bhp}, \
        буферное давление: {self.buff_pressure}, затрубное давление: {self.annular_pressure}, \
        линейное давление:  {self.line_pressure}, пластовое давление {self.form_pressure}'    

if __name__ == '__main__':
    well1 = WellsStartDates('500408500', '4058', '6', 'НП 4', '01012017')
    well2 = WellMonthRates('500408500', '4058', '01012018', '100', '100000', '10', '0', '700')
    well3 = WellTRPressure('500408500', '4058', '01012019', '100', '10', '10', '50', '180') 


    print(well1)
    print(well2)
    print(well3)        
