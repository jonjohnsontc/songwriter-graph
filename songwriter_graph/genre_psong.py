def genre_psong(genres, songs):
    gs_list = []
    count = 1
    for song, artist in songs[["s_song_id", "artist_id"]].values:
        for genre in genres:
            if artist == genre[1]:
                gs_list.append((count, song, genre[0], genre[1]))
                count += 1
    return gs_list
