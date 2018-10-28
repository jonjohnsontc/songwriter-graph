def song_feat_pull(song_list):
    '''
    Pulls modeling features of songs and outputs them into a separate list.
    '''
    master_song_list = []

    for entry in song_list:
        if isinstance(entry, dict):
            for track in entry['tracks']:
                master_song_list.append({'song_id':track['id'], 'song_title':track['name'],
                                         'artist_id':track['artists'][0]['id'], 'artist_name':track['artists'][0]['name'],
                                         'linked_album':track['album']['name'], 
                                         'album_release_date':track['album']['release_date'],
                                         'duration_ms':track['duration_ms'], 'explicit':track['explicit']})
    return master_song_list