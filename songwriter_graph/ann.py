"""This was initially written to build the AnnoyIndex which underlies at least
a couple of SWG models. However, I ended up doing all of the actual work in
building in indices via notebooks and iPython. The functions can still be
referenced, but no main script was ever completed"""
from collections import Counter
from argparse import ArgumentParser
from datetime import datetime

from annoy import AnnoyIndex
import pandas as pd
from tqdm import tqdm

from .config import metadata_cols
from .utils import drop_non_numeric_feats, load_df

TIME_AT_RUN = datetime.now().strftime("%m%d%Y")


def create_annoy_index(df, non_numeric_cols=None):
    """Creates an annoy index out of a passed in dataframe.
    
    Args:
        df: pandas dataframe
        non_numeric_cols: iterable, a listing of non-numeric columns to drop
    
    Returns:
        The annoy index object all nice and populated
    """
    df = df.drop(columns=non_numeric_cols)
    df_numeric = df.to_numpy()
    
    ai = AnnoyIndex(df_numeric.shape[1], 'euclidean')
    for i in range(len(df_numeric)):
        ai.add_item(i, df_numeric[i])
    return ai


def build_annoy_indices(ai, n_trees=500):
    """Builds and saves annoy indices"""
    return ai.build(n_trees)
    

def count_neighbors(ai: AnnoyIndex, wid_mapping: dict, num_votes: int=10) -> dict: 
    """Groups annoy index (`ai`) by writer and determines the most
    frequently occuring neighbors for each writer, based on the songs
    within their `wid_mapping`
    
    Args:
        ai: AnnoyIndex, the AnnoyIndex which was trained on the dataset
            in question
        wid_mapping: dict, a dictionary with contribid (or similar) as
            keys, and WID as values
        votes: int=10, the number of eligible votes to count for each
            song
            
    Returns:
        Dictionary of neighbor counts per `WID`
    """
    
    # establishing a dictionary to house the number of votes that each
    # writer recieves. `Counter` tallies 
    neighbor_counts = {wid : Counter() for wid in set(wid_mapping.values())}
    for i in tqdm(list(wid_mapping.keys())):
        
        # grab songs, aka votes
        votes = ai.get_nns_by_item(i, num_votes, include_distances=False)
        
        # retrieving writer id's belonging to songs, aka the neighbors
        neighbors = list(map(lambda x: wid_mapping[x], votes))
        
        wid = wid_mapping[i]
        neighbor_counts[wid].update(neighbors)
        
    return neighbor_counts


def combine_writer_counts_and_info(count_dict, writer_df):
    top_match_dict = {wid : {'writer_name' : '',
                          'ipi' : '',
                          'top_matches' : ''}\
                   for wid in count_dict.keys()}
    
    # Retreive Top 11 Results for each Songwriter
    for entry in count_dict:
        top_match_dict[entry]['top_matches'] = count_dict[entry].most_common(11)
    
    # add writer name and info to dictionary
    for wid in top_match_dict:
        if wid in writer_df['WID']:
            top_match_dict[wid]['writer_name'] = writer_df['Writer Name']\
                                                [writer_df['WID'] == wid].values[0]
            top_match_dict[wid]['ipi'] = writer_df['IPI']\
                                        [writer_df['WID'] == wid].values[0]
    
    return top_match_dict


def main(paths):
    """Wrapper for `ann`"""
    dfs = [load_df(path) for path in paths]

    pass


# TODO: revamp
def parse_args():
    parser = ArgumentParser(
        prog="Create Annoy Indicies",
        usage="Outputs `n` annoy indices based on params passed through",
    )
    parser.add_argument("path", default="data/main_wfeats.csv")
    parser.add_argument("trees", nargs="+", type=int)
    return vars(parser.parse_args())


if __name__ == "__main__":
    pass