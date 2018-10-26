def mk_msong_list(song_list):
    '''
    Retrieve `track_name` and `track_id` for each song and add to separate listing.
    '''
    master_song_list = []

    for entry in song_list:
        if isinstance(entry, dict):
            for track in entry['tracks']:
                master_song_list.append(dict({track['name'] : track['id']}))
    return master_song_list