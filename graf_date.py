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
print(min(dates))
print(len(dates))

app.layout = html.Div([
    dcc.Graph(
        id='Oil Field',
        figure={
            'data': [
                go.Scatter(
                    x=dates,
                    y=field_oil,
                    mode='lines',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                ) 
            ]
            }),
    dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=len(dates),
        step=1,
        value=[0, len(dates)]
    ),
    html.Div(id='output-container-range-slider')
])

@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'с {} по {}'.format(dates[value[0]].strftime('%d.%m.%y'), dates[value[1]].strftime('%d.%m.%y'))
  

@app.callback(    
    dash.dependencies.Output('Oil Field', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_figure(value):

    return {'layout': go.Layout(
            xaxis={'range': [dates[value[0]], dates[value[1]]]},
            yaxis={'title': 'Добыча нефти'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )}    



if __name__ == '__main__':
    app.run_server(debug=True)

