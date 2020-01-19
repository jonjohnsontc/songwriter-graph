import json
import logging
from pathlib import Path
from datetime import date

import pandas as pd
import numpy as np
import dask

from tqdm.auto import tqdm
from songwriter_graph.utils import get_files, save_object, save_objects, load_json

#TODO: Config
logging.basicConfig()

dask.config.set(scheduler='threads')

@dask.delayed
def get_mean_var(song_object: pd.core.frame.DataFrame, song_id: str) -> pd.core.frame.DataFrame:
    """Computes the mean and variance of an analysis json object passed
    through
    """
    mean_var = song_object.agg([np.mean, np.var])
    mean_var["song_id"] = song_id
    return mean_var


@dask.delayed
def get_pt_pca(song: pd.core.frame.DataFrame, song_id: str) -> pd.core.frame.DataFrame:
    '''Performs PCA on Pitch and Timbre values in a single song segment
    '''
    pt_pca = pd.DataFrame(
        PCA(song, dims_rescaled_data=10),
        columns=[f"component_{i}" for i in range(1,11)])
    pt_pca["song_id"] = song_id
    return pt_pca


@dask.delayed
def get_key_changes(song_sections: pd.core.frame.DataFrame, song_id: str) -> int:
    song_secs = song_sections.to_dict(orient="list")
    start_key = song_secs['key'][0]
    kc = 0 
    for item in song_secs['key']:
        cur_key = item
        if cur_key != start_key:
            start_key = cur_key
            kc += 1
    return pd.DataFrame.from_dict([{"song_id":song_id, "key_changes": kc}])


# https://stackoverflow.com/a/13224592
def PCA(data, dims_rescaled_data=2):
    """
    returns: data transformed in 2 dims/columns + regenerated original data
    pass in: data as 2D NumPy array
    """
    # mean center the data
    data -= data.mean(axis=0)
    # calculate the covariance matrix
    R = np.cov(data, rowvar=False)
    # calculate eigenvectors & eigenvalues of the covariance matrix
    # use 'eigh' rather than 'eig' since R is symmetric, 
    # the performance gain is substantial
    evals, evecs = np.linalg.eigh(R)
    # sort eigenvalue in decreasing order
    idx = np.argsort(evals)[::-1]
    evecs = evecs[:,idx]
    # sort eigenvectors according to same index
    evals = evals[idx]
    # select the first n eigenvectors (n is desired dimension
    # of rescaled data array, or dims_rescaled_data)
    evecs = evecs[:, :dims_rescaled_data]
    # carry out the transformation on the data using eigenvectors
    # and return the re-scaled data, eigenvalues, and eigenvectors
    return np.dot(evecs.T, data.T).T


@dask.delayed
def validate_analysis_obj(analysis_obj: dict):
    """Validates that analysis object passed through can be correctly
    parsed.
    """
    if isinstance(analysis_obj, dict)\
        & ("sections" in analysis_obj)\
        & ("segments" in analysis_obj)\
        & (len(analysis_obj["segments"])>0)\
        & (len(analysis_obj["sections"])>0):
        pass
    else:
        raise ValueError("Analysis object not valid")
    
    return


@dask.delayed
def get_song_objects(analysis_obj: dict) -> dict:
    """Retrieves objects necessary to compute analysis for"""
   
    # Instantiate containers for objects
    pitches = []
    timbre = []

    # Retrieve pitches and timbre 
    for i in analysis_obj["segments"]:
        pitches.append(i["pitches"])
        timbre.append(i["timbre"])
    
    p = pd.DataFrame(pitches, columns=[f"p_{i}" for i in range(1, 13)])
    t = pd.DataFrame(timbre, columns=[f"t_{i}" for i in range(1, 13)])
    combined_pitch_timbre = pd.concat([p, t], axis = 1)
    
    # Retrieve song segments
    song_sections = pd.DataFrame.from_dict(analysis_obj['sections'])

    return {
        "combined_pitch_timbre": combined_pitch_timbre,
        "song_sections": song_sections}


# Unit test this actually clears the list within the dictionary
@dask.delayed
def length_check(analysis_objs: dict):
    """Checks the size of analysis objects to determine if they're large
    enough to save and clear
    """
    for key in analysis_objs.keys():
        if len(analysis_objs[key]) > 10000:
            save_object(analysis_objs[key], key)
            analysis_objs[key].clear()
    return    


def analysis_sorter_delayed(lst: list, fp: str):
    '''Write me pls.
    '''
    key_changes = []
    sec_mean_vars = []
    pt_mean_vars = []
    pt_pcas = []

    for record in tqdm(lst):
        path = Path(fp, record)
        song_id = record.replace('.json', '')
        song = load_json(path)

        # validate json
        validate_analysis_obj(song)

        # retrieve objects for analysis
        for_analysis = get_song_objects(song)

        # Obtaining section mean & variance 
        sec_mean_var = get_mean_var(for_analysis["song_sections"], song_id)
        sec_mean_vars.append(sec_mean_var)

        # grabbing key changes
        no_of_key_changes = get_key_changes(for_analysis["song_sections"], song_id)
        key_changes.append(no_of_key_changes)

        # pitch and timbre values
        pt_vals = get_mean_var(for_analysis["combined_pitch_timbre"], song_id)
        pt_mean_vars.append(pt_vals)

        pt_pca = get_pt_pca(for_analysis["combined_pitch_timbre"], song_id)
        pt_pcas.append(pt_pca)

    key_changes = dask.compute(*key_changes)
    sec_mean_vars = dask.compute(*sec_mean_vars)
    pt_mean_vars = dask.compute(*pt_mean_vars)
    pt_pcas = dask.compute(*pt_pcas)

    save_objects([
        {"object": sec_mean_vars, "object_type":"sec_mean_vars"},
        {"object": pt_mean_vars, "object_type": "pt_mean_vars"},
        {"object":pt_pcas, "object_type":"pt_pcas"},
        {"object":key_changes, "object_type":"key_changes"}])
    return


if __name__ == "__main__":
    pass