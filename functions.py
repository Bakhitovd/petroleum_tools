import collections
import calendar
from datetime import datetime
import plotly.graph_objs as go

def create_figure_bar(output_arr, dates_list, date_range, title, yaxis_title):
    if len(list(output_arr.keys())) > 1:    
        date1=dates_list[date_range[0]]
        date2=dates_list[date_range[1]]
    else:
        date1=1
        date2=2  
    return {'data': [go.Bar(
                    x=list(output_arr.keys()),
                    y=list(output_arr.values()),
                    #mode='bar',
                    #opacity=0.7,
                    #marker={
                    #    'size': 15,
                    #    'line': {'width': 0.5, 'color': 'white'}
                    #}
                    )],
            'layout': go.Layout(
                    title=title,
                    xaxis={'range':[date1, date2]},
                    yaxis={'title': yaxis_title},
                    margin={'l': 60, 'b': 40, 't': 40, 'r': 10},
                    hovermode='closest'
                    
           )} 

def create_figure(output_arr, dates_list, date_range, title, yaxis_title):
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
                    title=title,
                    xaxis={'range':[date1, date2]},
                    yaxis={'title': yaxis_title},
                    margin={'l': 60, 'b': 40, 't': 40, 'r': 10}  
                    #,hovermode='closest'
           )}   

def summm_data(data, selected_forms, selected_pads, selected_wells, measurement):
    output_arr = {}
    if 'Все' in selected_forms or selected_forms =='Все':
        for f in data:
            for p in data[f]: 
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        try:
                            output_arr[d] += data[f][p][w][d][measurement]
                        except:
                            if measurement in list(data[f][p][w][d].keys()):
                                output_arr[d] = data[f][p][w][d][measurement]
    elif 'Все' in selected_pads or selected_pads =='Все':
        for f in selected_forms:
            for p in data[f]: 
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        try:
                            output_arr[d] += data[f][p][w][d][measurement]
                        except:
                            if measurement in list(data[f][p][w][d].keys()):
                                output_arr[d] = data[f][p][w][d][measurement]   
    elif  'Все' in selected_wells or selected_wells =='Все':
        for f in selected_forms:
            for p in selected_pads:
                if p in data[f]:
                    for w in data[f][p]:
                        for d in data[f][p][w]:
                            try:
                                output_arr[d] += data[f][p][w][d][measurement]
                            except:
                                if measurement in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d][measurement]
    else:
         for f in selected_forms:
            for p in selected_pads:
                for w in selected_wells:
                    if p in data[f] and w in data[f][p]:
                        for d in data[f][p][w]:
                            try:
                                output_arr[d] += data[f][p][w][d][measurement]
                            except:
                                if measurement in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d][measurement] 
    return collections.OrderedDict(sorted(output_arr.items()))

def production_fond_data(data, selected_forms, selected_pads, selected_wells, measurement = 'work_time'):
    output_arr = {}
    if 'Все' in selected_forms or selected_forms =='Все':
        for f in data:
            for p in data[f]: 
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        if 'injection' not in list(data[f][p][w][d].keys()) or data[f][p][w][d]['injection'] == 0:
                            date = datetime.strptime(d,'%Y-%m-%d')
                            num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                            try:
                                output_arr[d] += data[f][p][w][d][measurement]/num_hours
                            except:
                                if measurement in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d][measurement]/num_hours
    elif 'Все' in selected_pads or selected_pads =='Все':
        for f in selected_forms:
            for p in data[f]: 
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        if 'injection' not in list(data[f][p][w][d].keys()) or data[f][p][w][d]['injection'] == 0:
                            date = datetime.strptime(d,'%Y-%m-%d') 
                            num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                            try:
                                output_arr[d] += data[f][p][w][d][measurement]/num_hours
                            except:
                                if measurement in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d][measurement]/num_hours
    elif  'Все' in selected_wells or selected_wells =='Все':
        for f in selected_forms:
            for p in selected_pads:
                if p in data[f]:
                    for w in data[f][p]:
                        for d in data[f][p][w]:
                            if 'injection' not in list(data[f][p][w][d].keys()) or data[f][p][w][d]['injection'] == 0:
                                date = datetime.strptime(d,'%Y-%m-%d') 
                                num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                                try:
                                    output_arr[d] += data[f][p][w][d][measurement]/num_hours
                                except:
                                    if measurement in list(data[f][p][w][d].keys()):
                                        output_arr[d] = data[f][p][w][d][measurement]/num_hours
    else:
         for f in selected_forms:
            for p in selected_pads:
                for w in selected_wells:
                    if p in data[f] and w in data[f][p]:
                        for d in data[f][p][w]:
                            if 'injection' not in list(data[f][p][w][d].keys()) or data[f][p][w][d]['injection'] == 0:
                                date = datetime.strptime(d,'%Y-%m-%d') 
                                num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                                try:
                                    output_arr[d] += data[f][p][w][d][measurement]/num_hours
                                except:
                                    if measurement in list(data[f][p][w][d].keys()):
                                        output_arr[d] = data[f][p][w][d][measurement]/num_hours
    for d in output_arr.keys():
        output_arr[d] = round(output_arr[d], 0)

    return collections.OrderedDict(sorted(output_arr.items()))

def injection_fond_data(data, selected_forms, selected_pads, selected_wells, measurement = 'work_time'):
    output_arr = {}
    if 'Все' in selected_forms or selected_forms =='Все':
        for f in data:
            for p in data[f]: 
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        if 'injection' in list(data[f][p][w][d].keys()) and data[f][p][w][d]['injection'] != 0:
                            date = datetime.strptime(d,'%Y-%m-%d') 
                            num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                            try:
                                output_arr[d] += data[f][p][w][d][measurement]/num_hours
                            except:
                                if measurement in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d][measurement]/num_hours
    elif 'Все' in selected_pads or selected_pads =='Все':
        for f in selected_forms:
            for p in data[f]: 
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        if 'injection' in list(data[f][p][w][d].keys()) and data[f][p][w][d]['injection'] != 0:
                            date = datetime.strptime(d,'%Y-%m-%d') 
                            num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                            try:
                                output_arr[d] += data[f][p][w][d][measurement]/num_hours
                            except:
                                if measurement in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d][measurement]/num_hours
    elif  'Все' in selected_wells or selected_wells =='Все':
        for f in selected_forms:
            for p in selected_pads:
                if p in data[f]:
                    for w in data[f][p]:
                        for d in data[f][p][w]:
                            if 'injection' in list(data[f][p][w][d].keys()) and data[f][p][w][d]['injection'] != 0:
                                date = datetime.strptime(d,'%Y-%m-%d') 
                                num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                                try:
                                    output_arr[d] += data[f][p][w][d][measurement]/num_hours
                                except:
                                    if measurement in list(data[f][p][w][d].keys()):
                                        output_arr[d] = data[f][p][w][d][measurement]/num_hours
    else:
         for f in selected_forms:
            for p in selected_pads:
                for w in selected_wells:
                    if p in data[f] and w in data[f][p]:
                        for d in data[f][p][w]:
                            if 'injection' in list(data[f][p][w][d].keys()) and data[f][p][w][d]['injection'] != 0:
                                date = datetime.strptime(d,'%Y-%m-%d') 
                                num_hours = 24*calendar.monthrange(date.year, date.month)[1]
                                try:
                                    output_arr[d] += data[f][p][w][d][measurement]/num_hours
                                except:
                                    if measurement in list(data[f][p][w][d].keys()):
                                        output_arr[d] = data[f][p][w][d][measurement]/num_hours
    for d in output_arr.keys():
        output_arr[d] = round(output_arr[d], 0)

    return collections.OrderedDict(sorted(output_arr.items()))

def gas_water_inj(measurement, selected_pads):
    if measurement == 'gas_inj':
        gas_pads = ['101', '102', '103', '102_1', '103_1', '104']
        selected_pads = list(set(gas_pads) & set(selected_pads))
    elif measurement == 'water_inj':
        gas_pads = ['101', '102', '103', '102_1', '103_1', '104']
        selected_pads = list(set(selected_pads)-set(gas_pads))
    print(selected_pads)
    return selected_pads

def summ_inj_data(data, selected_forms, selected_pads, selected_wells, measurement):
    output_arr = {}
    if 'Все' in selected_forms or selected_forms =='Все':
        for f in data:
            data[f].keys()
            pad_list = []
            pad_list = gas_water_inj(measurement, list(data[f].keys()))
            for p in pad_list:
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        try:
                            output_arr[d] += data[f][p][w][d]['injection']
                        except:
                            if 'injection' in list(data[f][p][w][d].keys()):
                                output_arr[d] = data[f][p][w][d]['injection']
    elif 'Все' in selected_pads or selected_pads =='Все':
        for f in selected_forms:
            for p in data[f]: 
                for w in data[f][p]:
                    for d in data[f][p][w]:
                        try:
                            output_arr[d] += data[f][p][w][d]['injection']
                        except:
                            if 'injection' in list(data[f][p][w][d].keys()):
                                output_arr[d] = data[f][p][w][d]['injection']   
    elif  'Все' in selected_wells or selected_wells =='Все':
        for f in selected_forms:
            for p in selected_pads:
                if p in data[f]:
                    for w in data[f][p]:
                        for d in data[f][p][w]:
                            try:
                                output_arr[d] += data[f][p][w][d]['injection']
                            except:
                                if 'injection' in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d]['injection']
    else:
         for f in selected_forms:
            for p in selected_pads:
                for w in selected_wells:
                    if p in data[f] and w in data[f][p]:
                        for d in data[f][p][w]:
                            try:
                                output_arr[d] += data[f][p][w][d]['injection']
                            except:
                                if 'injection' in list(data[f][p][w][d].keys()):
                                    output_arr[d] = data[f][p][w][d]['injection'] 
    return collections.OrderedDict(sorted(output_arr.items()))
