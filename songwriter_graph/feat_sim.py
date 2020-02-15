def feat_sim(song_id, k=10, cos_sim_mat=cos_sim_mat_g):
    """
    Returns array of indices for top k songs with greatest similarity to given song, along with 
    their similarity rating, based on precomputed cosine similarity of feature vectors.

    top_songs_feat, top_songs_feat_sim = get_sim.by_feats(ind_song_id, k, cos_sim_mat)

    """
    top_songs_feat = np.argsort(cos_sim_mat[song_cosine_id[song_id]])[
        -2 : -(k + 2) : -1
    ]
    top_songs_feat_sim = np.sort(cos_sim_mat[song_cosine_id[song_id]])[
        -2 : -(k + 2) : -1
    ]

    return top_songs_feat, top_songs_feat_sim


def feat_sim_da(
    song_id, k=10, song_db=main_song_list, cos_sim_mat=cos_sim_mat_g
):
    """
    Returns array of indices for top k songs with greatest similarity to a given song, but only
    from artists who didn't perform the given song, along with their similarity rating, 
    based on precomputed cosine similarity of feature vectors.

    top_songs_feat, top_songs_feat_sim = get_sim.by_feats(ind_song_id, k, cos_sim_mat)
    """
    artist_id = song_db.loc[song_id, "artist_id"]
    artist_songs = song_db.index[song_db["artist_id"] == artist_id].drop(
        song_id
    )
    top_songs_feat = np.argsort(cos_sim_mat[song_cosine_id[song_id]])[
        -2 : -(k + 12) : -1
    ]
    top_songs_feat_sim = np.sort(cos_sim_mat[song_cosine_id[song_id]])[
        -2 : -(k + 12) : -1
    ]

    return top_songs_feat, top_songs_feat_sim, artist_songs
