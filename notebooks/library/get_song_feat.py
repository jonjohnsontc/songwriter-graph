def get_song_feat(song_list):
    '''
    Retrieve audio features for every song in `song_list`.
    '''
    song_feat = []
    for i in song_list:
        if isinstance(i, dict):
            id_list = []
            for k in i['tracks']:
                id_list.append(k['id'])
        else:
            continue
        try:
            song_feat.append(sp.audio_features(id_list))
            time.sleep(1)
        except:
            time.sleep(5)
            song_feat.append(sp.audio_features(id_list))
    return song_feat