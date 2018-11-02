import numpy as np
import pandas as pd

# Main Song List - This will be used to help lookup song titles 
main_song_list = pd.read_csv('../data/main_wfeats.csv', index_col='song_id')


def feat_sim(song_id, k=10, cos_sim_mat=cos_sim_mat_g):
    '''
    Returns array of indices for top k songs with greatest similarity to given song, along with 
    their similarity rating, based on precomputed cosine similarity of feature vectors.

    top_songs_feat, top_songs_feat_sim = get_sim.by_feats(ind_song_id, k, cos_sim_mat)

    '''
    top_songs_feat = np.argsort(cos_sim_mat[song_cosine_id[song_id]])[-2:-(k+2):-1]
    top_songs_feat_sim = np.sort(cos_sim_mat[song_cosine_id[song_id]])[-2:-(k+2):-1]

    return top_songs_feat, top_songs_feat_sim


def feat_sim_da(song_id, k=10, song_db=main_song_list, cos_sim_mat=cos_sim_mat_g):
    '''
    Returns array of indices for top k songs with greatest similarity to a given song, but only
    from artists who didn't perform the given song, along with their similarity rating, 
    based on precomputed cosine similarity of feature vectors.

    top_songs_feat, top_songs_feat_sim = get_sim.by_feats(ind_song_id, k, cos_sim_mat)
    '''
    artist_id = song_db.loc[song_id, 'artist_id']
    artist_songs = song_db.index[song_db['artist_id'] == artist_id].drop(song_id)
    top_songs_feat = np.argsort(cos_sim_mat[song_cosine_id[song_id]])[-2:-(k+12):-1]
    top_songs_feat_sim = np.sort(cos_sim_mat[song_cosine_id[song_id]])[-2:-(k+12):-1]
    
    return top_songs_feat, top_songs_feat_sim, artist_songs


def get_recs(song_id, k=10, cos_sim_mat=cos_sim_mat_g):
    '''
    Returns vector of recommended songs with the highest cosign similarity to 
    the song provided.
    '''
    try:
        top_songs_feat, top_songs_feat_sim = feat_sim(song_id, k, cos_sim_mat)
        return pd.DataFrame([[song_id_name[song_cosine_idr[x]] for x in top_songs_feat],
                         [song_id_artist[song_cosine_idr[x]] for x in top_songs_feat],
                         [song_cosine_idr[x] for x in top_songs_feat],
                         list(top_songs_feat_sim)], 
                        index=['Song Name', 'Artist', 'Song ID', 'Similarity']).T
    except:
        print('''No results available for that id. 
                Please refer to the Song Finder for a list of valid ids.''')

def get_recs_da(song_id, k=10, song_db=main_song_list, cos_sim_mat=cos_sim_mat_g):
    try:
        top_songs_feat, top_songs_feat_sim, artist_songs = feat_sim_da(song_id, k, main_song_list, cos_sim_mat)
        recs = [
            [song_id_name[song_cosine_idr[x]] for x in top_songs_feat],
            [song_id_artist[song_cosine_idr[x]] for x in top_songs_feat],
            [song_cosine_idr[x] for x in top_songs_feat],
            list(top_songs_feat_sim)
        ]

        recs = pd.DataFrame(recs, index=['Song Name', 'Artist', 'Song ID', 'Similarity']).T
        recs.set_index('Song ID', inplace=True)

        for song in artist_songs:
            if song in recs.index:
                recs.drop(song, inplace=True)

        recs.reset_index(inplace=True)
        return recs.head(k)
    except:
        print('''No results available for that id. 
                Please refer to the Song Finder for a list of valid ids.''')