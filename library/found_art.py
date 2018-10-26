def found_art(missing_artists):
    '''
    Iterating through `missing_artists`, and retrieving artist information for each observation.
    '''
    found_artists = []
    for artist in missing_artists:
        artist_list = sp.search(artist[1], type='artist')
        try:
            found_artists.append(artist_list['artists']['items'][0])
        except:
            found_artists.append('no_results')
        time.sleep(0.5)
    return found_artists