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