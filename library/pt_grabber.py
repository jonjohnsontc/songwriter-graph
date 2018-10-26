def pt_grabber(lst):
    '''
    Retrieves pitch and timbre summary statistics for every song in audio_analysis folder.
    '''
    timbre_means = []
    timbre_var = []
    pitch_means = []
    pitch_var = []
    count = 0
    for record in lst:
        with open('../data/audio_analysis/{}'.format(record), 'r') as f:
            analysis = json.load(f)
            if isinstance(analysis, dict):
                if 'segments' in analysis:
                    try:
                        pm, tm, pv, tv = pt_grabber_sgl(analysis)
                    except:
                        response = "unable to gather summary stats for song {} pitch & timbre".format(record.replace(".json", ''))
        try:
            timbre_means.append(dict({record.replace(".json", ""):tm}))
            timbre_var.append(dict({record.replace(".json", ""):tv}))
            pitch_means.append(dict({record.replace(".json", ""):pm}))
            pitch_var.append(dict({record.replace(".json", ""):pv}))
        except:
            [lists.append(response) for lists in [timbre_means, timbre_var, 
                                                  pitch_means, pitch_var]]
        count += 1
        if count % 1000 == 0:
            print("grabbing {}".format(count + 1))
    return timbre_means, timbre_var, pitch_means, pitch_var