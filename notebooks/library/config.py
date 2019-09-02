
# Paths for final dataset creation
songwriter_df_path="data/interim/tracks_w_writers/*"
song_features_path="data/interim/song_features/*"
modeling_path="data/modeling/*"
segment_path="data/interim/analysis_segments/*"
modeling_labels_path="data/modeling/"

paths = {
    "songwriter_df_path" : "data/interim/tracks_w_writers/*",
    "compressed_genre_path" : "data/interim/genres/compressed_genres/*",
    "segment_path" : "data/interim/analysis_segments/*",
    "song_features_path" : "data/interim/song_features/*",
   
        }


non_normalized_cols = [
    'track_id',
    'Song Title',
    'Artist',
    'artist_id',
    'name',
    'popularity',
    'followers',
    'artist_name',
    'song_id',
    'song_title',
    'CID',
    'PID',
    'Title',
    'Performer Name',
    'Writer Name',
    'IPI',
    'PRO',
    ]