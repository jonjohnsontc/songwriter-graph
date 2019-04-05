import json
import os
import pandas as pd
import numpy as np
from collections import defaultdict

def analysis_sorter(lst, fp):
    '''
    Iterate through individual song .json files for sections, and calculate the mean and variance for 
    'confidence', 'duration', 'loudness', 'mode', 'mode_confidence', 'tempo', and 'tempo_confidence' values. 
    
    Returns two lists of dictionaries, one containing each song's section mean values, the other containing 
    each song's section variance values.
    '''
    mean_dicts = {}
    var_dicts = {}
    exceptions_dict = {}
    count = 0
    for record in lst:
        try:
            with open(f'{fp}/{record}.json', 'r') as f:
                analysis = json.load(f)
        except Exception as e:
            exceptions_dict[record] = str(e)
            mean_dicts[record] = {
                    'confidence' : np.NaN, 
                    'duration' : np.NaN, 
                    'loudness' : np.NaN, 
                    'mode' : np.NaN, 
                    'mode_confidence': np.NaN,
                    'tempo' : np.NaN, 
                    'tempo_confidence' : np.NaN
            }
            var_dicts[record] = {
                    'confidence' : np.NaN, 
                    'duration' : np.NaN, 
                    'loudness' : np.NaN, 
                    'mode' : np.NaN, 
                    'mode_confidence': np.NaN,
                    'tempo' : np.NaN, 
                    'tempo_confidence' : np.NaN
            }
        if isinstance(analysis, dict) & 'sections' in analysis:
            for section in analysis['sections']:
                try:
                    mean_dicts[count] = section
                except Exception as e:
                    mean_dicts[count] = f'Exception: {e}'

            
            try:
                df = pd.DataFrame.from_dict(mean_dicts, orient='index')    
                mean = df[['confidence', 'duration', 'loudness', 'mode', 'mode_confidence',
                        'tempo', 'tempo_confidence']].mean().to_dict()
                var = df[['confidence', 'duration', 'loudness', 'mode', 'mode_confidence',
                        'tempo', 'tempo_confidence']].var().to_dict()
                mean_dicts[record.replace('.json', '')] = mean
                var_dicts[record.replace('.json', '')] = var
            except:
                mean_dicts[(record.replace('.json',''))] = {
                    'confidence' : np.NaN, 
                    'duration' : np.NaN, 
                    'loudness' : np.NaN, 
                    'mode' : np.NaN, 
                    'mode_confidence': np.NaN,
                    'tempo' : np.NaN, 
                    'tempo_confidence' : np.NaN
                }
                var_dicts[(record.replace('.json',''))] = {
                    'confidence' : np.NaN, 
                    'duration' : np.NaN, 
                    'loudness' : np.NaN, 
                    'mode' : np.NaN, 
                    'mode_confidence': np.NaN,
                    'tempo' : np.NaN, 
                    'tempo_confidence' : np.NaN
                }            
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


def pt_grabber(filepath):
    '''
    Retrieves pitch and timbre summary statistics for every song in audio_analysis folder.
    '''
    # timbre_means = []
    # timbre_var = []
    # pitch_means = []
    # pitch_var = []
    timbre_means = {}
    timbre_var = {}
    pitch_means = {}
    pitch_var = {}
    errors = {}
    count = 0

    aa_directory = os.listdir(filepath)
    audio_analysis_files = list(filter(lambda x: '.json' in str(x), aa_directory))

    for record in audio_analysis_files:
        try: 
            with open(f'{filepath}/{record}', 'r') as f:
                analysis = json.load(f)
        except Exception as e:
            print(f'unable to pull {record}, {str(e)}')
            errors[record] = e
        if isinstance(analysis, dict):
            if 'segments' in analysis:
                try:
                    pm, tm, pv, tv = pt_grabber_sgl(analysis)
                except:
                    response = f"unable to gather summary stats \
                        for song {record.replace('.json', '')} pitch & timbre"
        try:
            timbre_means[record.replace(".json", "")] = {'timbre_means' : tm}
            timbre_var[record.replace(".json", "")] = {'timbre_var' : tv}
            pitch_means[record.replace(".json", "")] = {'pitch_means' : pm}
            pitch_var[record.replace(".json", "")] = {'pitch_var' : pv}
        except Exception as e:
            timbre_means[record.replace(".json", "")] = e
            timbre_var[record.replace(".json", "")] = e
            pitch_means[record.replace(".json", "")] = e
            pitch_var[record.replace(".json", "")] = e 
        # try:
        #     timbre_means.append(dict({record.replace(".json", ""):tm}))
        #     timbre_var.append(dict({record.replace(".json", ""):tv}))
        #     pitch_means.append(dict({record.replace(".json", ""):pm}))
        #     pitch_var.append(dict({record.replace(".json", ""):pv}))
        # except:
        #     [lists.append(response) for lists in [timbre_means, timbre_var, 
        #                                           pitch_means, pitch_var]]
        count += 1
        if count % 10000 == 0:
            print("grabbing {}".format(count + 1))
        if count % 100000 == 0:
            print("Saving results to file")
            with open(f'../data/pitch_timbre_means_vars/timbre_means_{count}.json', 'w') as f:
                json.dump(timbre_means, f)
            with open(f'../data/pitch_timbre_means_vars/timbre_var_{count}.json', 'w') as f:
                json.dump(timbre_var, f)
            with open(f'../data/pitch_timbre_means_vars/pitch_means_{count}.json', 'w') as f:
                json.dump(pitch_means, f)    
            with open(f'../data/pitch_timbre_means_vars/pitch_var_{count}.json', 'w') as f:
                json.dump(pitch_var, f)
            for d in [timbre_means, timbre_var, pitch_means, pitch_var]:
                d.clear()
    with open(f'../data/pitch_timbre_means_vars/timbre_means_{count}.json', 'w') as f:
        json.dump(timbre_means, f)
    with open(f'../data/pitch_timbre_means_vars/timbre_var_{count}.json', 'w') as f:
        json.dump(timbre_var, f)
    with open(f'../data/pitch_timbre_means_vars/pitch_means_{count}.json', 'w') as f:
        json.dump(pitch_means, f)    
    with open(f'../data/pitch_timbre_means_vars/pitch_var_{count}.json', 'w') as f:
        json.dump(pitch_var, f)
    with open(f'../data/pitch_timbre_means_vars/errors_{count}.json', 'w') as f:
        json.dump(errors, f)    
    return 'finished'


def pt_grabber_sgl(song):
    '''
    Retrieve pitch and timbre summary statistics for specified song
    '''
    pitches = np.array(song['segments'][0]['pitches'])
    timbre = np.array(song['segments'][0]['timbre'])
    
    for record in song['segments']:
        new_pitch = np.array(record['pitches'])
        new_timbre = np.array(record['timbre'])
        pitches = np.vstack((pitches, new_pitch))
        timbre = np.vstack((timbre, new_timbre))

    pitch_means = np.mean(pitches, axis = 0)
    timbre_means = np.mean(timbre, axis = 0)
    pitch_var = np.var(pitches, axis = 0)
    timbre_var = np.var(timbre, axis = 0)

    return pitch_means, timbre_means, pitch_var, timbre_var