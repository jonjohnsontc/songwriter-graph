def genre_p_artist(genres):
    '''
    Make artist to genre listing
    '''
    gdict_list = []
    
    for g_list, a_id  in genres.values:
        for genre in g_list:
            gdict_list.append((genre, a_id))
    return gdict_list