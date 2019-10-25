import collections

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
