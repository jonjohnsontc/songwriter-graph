def miss_art(conf_list):
    '''
    Iterate through `confident_list` for any artists that weren't retrieved during the lists' creation
    '''
    missing_artists = []
    for i in list(enumerate(confident_list)):
        if i[1] == 'no_results':
            missing_artists.append((i[0], artist_list_td[i[0]]))
    return missing_artists