from get_data_from_db import get_data
from functions import summm_data, production_fond_data,injection_fond_data, summ_inj_data, create_figure, create_figure_bar, compensation
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

chart_deps = [dash.dependencies.Input('formation-selection', 'value'),
              dash.dependencies.Input('pad-selection', 'value'),
              dash.dependencies.Input('wells-selection', 'value'),
              dash.dependencies.Input('date-range-slider', 'value')]

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

    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Div([
            html.Label('Отображаемый период:'),    
            dcc.RangeSlider(
                id='date-range-slider',
                min=0,
                max = len(dates_list)-1,
                step=1,
                value = [0, len(dates_list)-1]),
            html.Div(id='output-container-range-slider')
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 15px'
    }),
    html.Div([

        html.Div([
            dcc.Graph(id='chart1')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '0px 5px 5px 5px' }),

        html.Div([
            dcc.Graph(id='chart2')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '5px 5px 5px 5px' }),
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(211, 217, 224)'
    }),
    html.Div([

        html.Div([
            dcc.Graph(id='chart4')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '5px 5px 0px 5px' }),

        html.Div([
            dcc.Graph(id='chart3')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '5px 5px 0px 5px' }),    
    ]),
    html.Div([

        html.Div([
            dcc.Graph(id='chart5')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '5px 5px 0px 5px' }),

        html.Div([
            dcc.Graph(id='chart6')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '5px 5px 0px 5px' }),    
    ]),
    html.Div([

        html.Div([
            dcc.Graph(id='chart7')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '5px 5px 0px 5px' }),

        html.Div([
            dcc.Graph(id='chart8')
        ],style={'width': '49%', 'display': 'inline-block', 'padding': '5px 5px 0px 5px' }),    
    ])
], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(211, 217, 224)'
})

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
    dash.dependencies.Output('chart1', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = summm_data(data, selected_forms, selected_pads, selected_wells, 'oil')
    return create_figure(output_arr, dates_list, date_range, 'Добыча нефти', 'Добыча нефти, т/мес.')
 
@app.callback(    
    dash.dependencies.Output('chart2', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = summm_data(data, selected_forms, selected_pads, selected_wells, 'gas')
    return create_figure(output_arr, dates_list, date_range, 'Добыча газа', 'Добыча газа, м3/мес.')
    
@app.callback(    
    dash.dependencies.Output('chart3', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = summ_inj_data(data, selected_forms, selected_pads, selected_wells, 'gas_inj')
    return create_figure(output_arr, dates_list, date_range, 'Закачка газа', 'Закачка газа, м3/мес.')

@app.callback(    
    dash.dependencies.Output('chart4', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = summ_inj_data(data, selected_forms, selected_pads, selected_wells, 'water_inj')
    return create_figure(output_arr, dates_list, date_range, 'Закачка воды', 'Закачка воды, м3/мес.')

@app.callback(    
    dash.dependencies.Output('chart5', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = production_fond_data(data, selected_forms, selected_pads, selected_wells)
    return create_figure_bar(output_arr, dates_list, date_range, 'Работающий фонт добывающих скважин', 'Добывающий фонд, шт.')
 
@app.callback(    
    dash.dependencies.Output('chart6', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    output_arr = injection_fond_data(data, selected_forms, selected_pads, selected_wells)
    return create_figure_bar(output_arr, dates_list, date_range, 'Работающий нагнетательный фонд', 'Нагнетательный фонд, шт.')

@app.callback(    
    dash.dependencies.Output('chart7', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    gas_summ_form = summm_data(data, selected_forms, selected_pads, selected_wells, 'gas_form')
    liquid_summ_form = summm_data(data, selected_forms, selected_pads, selected_wells, 'liquid_form')
    injection_summ_water = summ_inj_data(data, selected_forms, selected_pads, selected_wells, 'water_inj')
    injection_summ_gas = summ_inj_data(data, selected_forms, selected_pads, selected_wells, 'gas_inj')
    output_arr = compensation(dates_list, gas_summ_form, liquid_summ_form, injection_summ_water, injection_summ_gas)
    return create_figure_bar(output_arr, dates_list, date_range, 'Текущая компенсация', 'Текущая компенсация, %')

@app.callback(    
    dash.dependencies.Output('chart8', 'figure'), chart_deps)
def update_figure(selected_forms, selected_pads, selected_wells, date_range):
    gas_summ_form = summm_data(data, selected_forms, selected_pads, selected_wells, 'gas_form')
    liquid_summ_form = summm_data(data, selected_forms, selected_pads, selected_wells, 'liquid_form')
    injection_summ_water = summ_inj_data(data, selected_forms, selected_pads, selected_wells, 'water_inj')
    injection_summ_gas = summ_inj_data(data, selected_forms, selected_pads, selected_wells, 'gas_inj')
    output_arr = compensation(dates_list, gas_summ_form, liquid_summ_form, injection_summ_water, injection_summ_gas)
    return create_figure_bar(output_arr, dates_list, date_range, 'Текущая компенсация', 'Текущая компенсация, %')
               
if __name__ == '__main__':
    app.run_server(debug=True)