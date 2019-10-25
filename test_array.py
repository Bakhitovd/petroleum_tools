from get_data_from_db import get_data
from functions import summm_data
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json
import collections

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)   

with open("data", "r", encoding="utf-8") as file:
    data = json.load(file)

forms = list(data.keys())
label_forms = [{'label': 'Все пласты', 'value': 'Все'}]
for i in forms:
    label_forms.append(
        {'label': i, 'value': i}
    )
dates_list = []

for f in data:
    for p in data[f]: 
        for w in data[f][p]:
            for d in data[f][p][w]:
                if d not in dates_list:
                    dates_list.append(d)
dates_list = sorted(dates_list)                 
 
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Выберете пласт:'),
            dcc.Dropdown(
                id = 'formation-selection',
                options=label_forms,
                value=['Все'],
                multi=True)
        ],style={'width': '33%', 'display': 'inline-block'}),    
        html.Div([    
            html.Label('Выберете куст:'),
            dcc.Dropdown(id = 'pad-selection',
               multi=True)
        ],style={'width': '33%', 'display': 'inline-block'}),  
        html.Div([       
            html.Label('Выберете скважины:'),
            dcc.Dropdown(id = 'wells-selection',
                multi=True)      
        ],style={'width': '33%', 'display': 'inline-block'}),

    ]),
    html.Div([
            html.Label('Отображаемый период:'),    
            dcc.RangeSlider(
                id='date-range-slider',
                min=0,
                max = len(dates_list)-1,
                step=1,
                value = [0, len(dates_list)-1]),
            html.Div(id='output-container-range-slider')
    ]),
    html.Div([

        html.Div([
            html.Label('Добыча нефти'), 
            dcc.Graph(id='chart1')
        ],style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Добыча газа'), 
            dcc.Graph(id='chart2')
        ],style={'width': '49%', 'display': 'inline-block'}),
        
    ]),
    html.Div([

        html.Div([
            html.Label('Закачка'), 
            dcc.Graph(id='chart3')
        ],style={'width': '49%', 'display': 'inline-block'}),

       # html.Div([
       #     html.Label('Фонд'), 
       #     dcc.Graph(id='chart4')
       # ],style={'width': '49%', 'display': 'inline-block'}),
        
    ])

])

@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('date-range-slider', 'value')])
def update_output(value):
    date1=dates_list[value[0]]
    date2=dates_list[value[1]]
    return 'с {} по {}'.format(date1, date2)

@app.callback(
    dash.dependencies.Output('pad-selection', 'options'),
    [dash.dependencies.Input('formation-selection', 'value')])
def update_output(selected_form):
    label_pads = [{'label': 'Все кусты', 'value': 'Все'}]
    if 'Все' not in selected_form and selected_form !='Все':
        for form in selected_form:
            for i in data[form]:
                x = {'label': i, 'value': i}
                if x not in label_pads:
                    label_pads.append(x)
    return label_pads

@app.callback(
    dash.dependencies.Output('wells-selection', 'options'),
    [dash.dependencies.Input('formation-selection', 'value'),
     dash.dependencies.Input('pad-selection', 'value')])
def update_output(selected_form, selected_pad):
    label_wells = [{'label': 'Все скважины', 'value': 'Все'}]
    if 'Все' not in selected_pad and selected_pad != 'Все' and selected_pad !=[]:
        for form in selected_form:
            for pad in selected_pad:
                if pad in data[form]:
                    for well in data[form][pad]:  
                        x = {'label': well, 'value': well}
                        if x not in label_wells :
                            label_wells.append(x)
    return label_wells

@app.callback(
    dash.dependencies.Output('pad-selection', 'value'),
    [dash.dependencies.Input('pad-selection', 'options')])
def set_pads(set_forms):
    return set_forms[0]['value']

@app.callback(
    dash.dependencies.Output('wells-selection', 'value'),
    [dash.dependencies.Input('wells-selection', 'options')])
def set_wells(selected_pads):
    return selected_pads[0]['value']

@app.callback(    
    dash.dependencies.Output('chart1', 'figure'),
    [dash.dependencies.Input('formation-selection', 'value'),
    dash.dependencies.Input('pad-selection', 'value'),
    dash.dependencies.Input('wells-selection', 'value'),
    dash.dependencies.Input('date-range-slider', 'value')])
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = summm_data(data, selected_forms, selected_pads, selected_wells, 'oil')
    if len(list(output_arr.keys())) > 1:    
        date1=dates_list[date_range[0]]
        date2=dates_list[date_range[1]]
    else:
        date1=1
        date2=2  
    return {'data': [go.Scatter(
                    x=list(output_arr.keys()),
                    y=list(output_arr.values()),
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

@app.callback(    
    dash.dependencies.Output('chart2', 'figure'),
    [dash.dependencies.Input('formation-selection', 'value'),
    dash.dependencies.Input('pad-selection', 'value'),
    dash.dependencies.Input('wells-selection', 'value'),
    dash.dependencies.Input('date-range-slider', 'value')])
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = summm_data(data, selected_forms, selected_pads, selected_wells, 'gas')
    if len(list(output_arr.keys())) > 1:    
        date1=dates_list[date_range[0]]
        date2=dates_list[date_range[1]]
    else:
        date1=1
        date2=2  
    return {'data': [go.Scatter(
                    x=list(output_arr.keys()),
                    y=list(output_arr.values()),
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

@app.callback(    
    dash.dependencies.Output('chart3', 'figure'),
    [dash.dependencies.Input('formation-selection', 'value'),
    dash.dependencies.Input('pad-selection', 'value'),
    dash.dependencies.Input('wells-selection', 'value'),
    dash.dependencies.Input('date-range-slider', 'value')])
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = summm_data(data, selected_forms, selected_pads, selected_wells, 'injection')
    if len(list(output_arr.keys())) > 1:    
        date1=dates_list[date_range[0]]
        date2=dates_list[date_range[1]]
    else:
        date1=1
        date2=2  
    return {'data': [go.Scatter(
                    x=list(output_arr.keys()),
                    y=list(output_arr.values()),
                    mode='lines',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                    )],
            'layout': go.Layout(
                    xaxis={'range':[date1, date2]},
                    yaxis={'title': 'Закачка'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    hovermode='closest'
                    
           )}    

if __name__ == '__main__':
    app.run_server(debug=True)