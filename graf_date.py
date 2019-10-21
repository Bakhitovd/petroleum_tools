from model import db, WellMonthRates, Base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime as dt
from get_data_from_db import get_data

def get_field_data_from_merfond(bd_session):
    field_oil = []
    dates = []
    for row in bd_session.query(WellMonthRates.date, 
                                func.sum(WellMonthRates.oil)
                                ).group_by(WellMonthRates.date):
        dates.append(row[0])
        field_oil.append(row[1])
    return (dates, field_oil)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
dates, field_oil= get_field_data_from_merfond(session)


data1 = get_data(session)
forms = list(data1.keys())
label_forms = []


for i in forms:
    label_forms.append(
        {'label': i, 'value': i}
    )

app.layout = html.Div([
    dcc.Graph(
        id='Oil Field'),
    dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=len(dates)-1,
        step=1,
        value=[0, len(dates)-1]
    ),
    html.Div(id='output-container-range-slider'),

    html.Label('Выберете пласт:'),
    dcc.Dropdown(
        id = 'formation-selection',
        options=label_forms,
        value=[],
        multi=True
    ),

    html.Label('Выберете куст:'),
    dcc.Dropdown(id = 'pad-selection',
        multi=True
    )
])

@app.callback(
    dash.dependencies.Output('pad-selection', 'options'),
    [dash.dependencies.Input('formation-selection', 'value')])
def update_output(value):
    label_pads = [{'label': 'Все', 'value': 'Все'}]
    for i in list(value):
        label_pads.append(
        {'label': data1[i], 'value': data1[i]}
    )
    options = label_pads
    return options

@app.callback(
    dash.dependencies.Output('pad-selection', 'value'),
    [dash.dependencies.Input('pad-selection', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    date1=dates[value[0]].strftime('%d.%m.%y')
    date2=dates[value[1]].strftime('%d.%m.%y')
    return 'с {} по {}'.format(date1, date2)
  

@app.callback(    
    dash.dependencies.Output('Oil Field', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_figure(value):
    date1=dates[value[0]].date()
    date2=dates[value[1]].date()
    return {'data': [go.Scatter(
                    x=dates,
                    y=field_oil,
                    mode='lines',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                    )],
            'layout': go.Layout(
                    xaxis={'range':[date1, date2]},
                    yaxis={'title': 'Добыча нефти'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest'
           )}    

if __name__ == '__main__':
    app.run_server(debug=True)