# Paths for final dataset creation

songwriter_df_path = "data/interim/tracks_w_writers/*"
song_features_path = "data/interim/song_features/*"
modeling_path = "data/modeling/*"
segment_path = "data/interim/analysis_segments/*"
modeling_labels_path = "data/modeling/"

paths = {
    "songwriter_df_path": "data/interim/tracks_w_writers/*",
    "compressed_genre_path": "data/interim/genres/compressed_genres/*",
    "segment_path": "data/interim/analysis_segments/*",
    "song_features_path": "data/interim/song_features/*",
}


# The following are column names that are used in the various data shaping
# functions within `analysis_sorter`

metadata_cols = [
    'WID',
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
    'contribid'
]


non_normalized_cols = [
    "track_id",
    "Song Title",
    "Artist",
    "artist_id",
    "name",
    "popularity",
    "followers",
    "artist_name",
    "song_id",
    "song_title",
    "CID",
    "PID",
    "Title",
    "Performer Name",
    "Writer Name",
    "IPI",
    "PRO",
]

feature_cols = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature",
    "key_changes",
    "mean_song_conf",
    "mean_loudness",
    "mean_mode",
    "mean_mode_conf",
    "mean_tempo",
    "mean_tempo_conf",
    "var_song_conf",
    "var_loudness",
    "var_mode",
    "var_mode_conf",
    "var_tempo",
    "var_tempo_conf",
    "tm_dim_1",
    "tm_dim_2",
    "tm_dim_3",
    "tm_dim_4",
    "tm_dim_5",
    "tm_dim_6",
    "tm_dim_7",
    "tm_dim_8",
    "tm_dim_9",
    "tm_dim_10",
    "tm_dim_11",
    "tm_dim_12",
    "tv_dim_1",
    "tv_dim_2",
    "tv_dim_3",
    "tv_dim_4",
    "tv_dim_5",
    "tv_dim_6",
    "tv_dim_7",
    "tv_dim_8",
    "tv_dim_9",
    "tv_dim_10",
    "tv_dim_11",
    "tv_dim_12",
    "pm_dim_1",
    "pm_dim_2",
    "pm_dim_3",
    "pm_dim_4",
    "pm_dim_5",
    "pm_dim_6",
    "pm_dim_7",
    "pm_dim_8",
    "pm_dim_9",
    "pm_dim_10",
    "pm_dim_11",
    "pm_dim_12",
    "pv_dim_1",
    "pv_dim_2",
    "pv_dim_3",
    "pv_dim_4",
    "pv_dim_5",
    "pv_dim_6",
    "pv_dim_7",
    "pv_dim_8",
    "pv_dim_9",
    "pv_dim_10",
    "pv_dim_11",
    "pv_dim_12",
]

pt_cols = [f"p_{i}" for i in range(1, 13)]
pt_cols.extend([f"t_{i}" for i in range(1, 13)])

section_cols = [
    "start",
    "duration",
    "confidence",
    "loudness",
    "tempo",
    "tempo_confidence",
    "key",
    "key_confidence",
    "mode",
    "mode_confidence",
    "time_signature",
    "time_signature_confidence",
]

section_mean_var_cols = [f"mean_{sec}" for sec in section_cols]
section_mean_var_cols.extend([f"var_{sec}" for sec in section_cols])
section_mean_var_cols.append("key_changes")

key_changes_cols = ["key_changes"]

pt_mean_var_cols = [f"mean_{pt}" for pt in pt_cols]
pt_mean_var_cols.extend([f"var_{pt}" for pt in pt_cols])

pt_pca_cols = [f"pt_{i}_component_{x}" for i in range(12) for x in range(10)]
