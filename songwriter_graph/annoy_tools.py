from argparse import ArgumentParser
from datetime import datetime

from annoy import AnnoyIndex
import pandas as pd
import numpy as np

from songwriter_graph.utils import drop_non_numeric_feats, load_df

TIME_AT_RUN = datetime.now().strftime("%m%d%Y")

# https://cmry.github.io/notes/euclidean-v-cosine
def l2_normalize(v):
    norm = np.sqrt(np.sum(np.square(v)))
    return v / norm


def create_annoy_index(feat_data, n_trees, distance='euclidean'):
    """Creates an AnnoyIndexed dataset"""
    
    if not isinstance(n_trees, int):
        n_trees = int(n_trees)

    ai = AnnoyIndex(feat_data.shape[1], distance)
    for i in range(len(feat_data)):
        ai.add_item(i, feat_data[i])
    ai.build(n_trees)
    return ai


def create_annoy_indices(feat_data, n_trees_array, distance='euclidean'):
    """Wrapper for `annoy_tools`"""
    for i in range(len(n_trees_array)):
        ai = create_annoy_index(feat_data, n_trees_array[i], distance)
        ai.save(f"Song_Index/data/ai/ai_{n_trees_array[i]}_trees_{TIME_AT_RUN}.ann")
    return 


def get_recommendations(songid, similarity_matrix, mapping):
    """Retrieves recommendations for a given songid"""
    
    # retrieving index for songid in mapping
    idx = list(filter(lambda x: x[1]['song_id'] == songid, mapping.items()))[0][0]
    
    # retrieving recs
    recs = similarity_matrix.get_nns_by_item(idx, 10, include_distances=True)
    
    # recommendation listing
    recs_list = [mapping[index] for index in recs[0]]
    
    # append distances to rec_list
    for i in range(len(recs_list)):
        recs_list[i]['score'] = recs[1][i]
    
    # output to df
    recs_df = pd.DataFrame.from_dict(recs_list)
    
    return recs_df

def parse_args():
    parser = ArgumentParser(
        prog="Create Annoy Indicies",
        usage="Outputs `n` annoy indices based on params passed through"
    )
    parser.add_argument(
        "path",
        default="data/main_wfeats.csv")
    parser.add_argument(
        "trees",
        nargs="+",
        type=int)
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    data = load_df(args['path'])
    just_data = drop_non_numeric_feats(data)
    normalized_data = l2_normalize(just_data.to_numpy()) # convert df to numpy array 
    create_annoy_indices(normalized_data, args['trees'], distance='euclidean')
