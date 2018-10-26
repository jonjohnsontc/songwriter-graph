def top_10(artist_ids):
    '''
    Retrieves top 10 most popular tracks on Spotify for the artists specified in the `artist_ids` listing. 
    '''
    top_10s = []

    for aid in artist_ids:
        try:
            top_10s.append(sp.artist_top_tracks(aid))
        except:
            top_10s.append('no_results')
        time.sleep(1)
    return top_10s