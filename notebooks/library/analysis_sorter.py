def analysis_sorter(lst):
    '''
    Iterate through individual song .json files for sections, and calculate the mean and variance for 
    'confidence', 'duration', 'loudness', 'mode', 'mode_confidence', 'tempo', and 'tempo_confidence' values. 
    
    Returns two lists of dictionaries, one containing each song's section mean values, the other containing 
    each song's section variance values.
    '''
    mean_dicts = []
    var_dicts = []
    count = 0
    for record in lst:
        with open('../data/audio_analysis/{}'.format(record), 'r') as f:
            analysis = json.load(f)
            if isinstance(analysis, dict):
                if 'sections' in analysis:
                    try:
                        mean_dict = {}
                        var_dict = {}
                        df = pd.DataFrame(analysis['sections'])
                        mean = df[['confidence', 'duration', 'loudness', 'mode', 'mode_confidence',
                                   'tempo', 'tempo_confidence']].mean().to_dict()
                        var = df[['confidence', 'duration', 'loudness', 'mode', 'mode_confidence',
                                   'tempo', 'tempo_confidence']].var().to_dict()
                        mean_dict[record.replace('.json', '')] = mean
                        var_dict[record.replace('.json', '')] = var
                        mean_dicts.append(mean_dict)
                        var_dicts.append(var_dict)
                    except:
                        mean_dict = {}
                        var_dict = {}
                        mean_dict[(record.replace('.json',''))] = 'Unable to calculate mean of section features'
                        var_dict[(record.replace('.json',''))] = 'Unable to calculate variance of section features'
                        mean_dicts.append(mean_dict)
                        var_dicts.append(var_dict)
            count += 1
            if count % 5000 == 0:
                print("Completed {} files".format(count))
            if count % 5000 == 0:
                with open('../data/section_var_summary_{}.json'.format(count), 'w') as f:
                    json.dump(var_dicts, f)
                    var_dicts.clear()
                with open('../data/section_mean_summary_{}.json'.format(count), 'w') as f:
                    json.dump(mean_dicts, f)
                    mean_dicts.clear()
    return mean_dicts, var_dicts