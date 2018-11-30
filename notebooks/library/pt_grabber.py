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