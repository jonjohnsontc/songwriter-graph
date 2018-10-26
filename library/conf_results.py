def conf_results(artist_list):
    '''
    Parses through spotify search results to retrieve the `artist_id` of the first 
    result of each search.
    '''
    confident_list = []
    for artist in artist_list:
        results = sp.search(artist, type='artist')
        try:
            confident_list.append(results['artists']['items'][0])
        except:
            confident_list.append('no_results')
        time.sleep(1)
    return confident_list