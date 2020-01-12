import json
import os
import logging
from datetime import date

import pandas as pd
import numpy as np
# Note - not yet used
import dask
import dask.bag as db

from tqdm.auto import tqdm
from library.utils import get_files, save_object, save_objects

#TODO: Config
logging.basicConfig()

def get_mean_var(song_object: pd.core.frame.DataFrame, song_id: str) -> pd.core.frame.DataFrame:
    """Computes the mean and variance of an analysis json object passed
    through
    """
    mean_var = song_object.agg([np.mean, np.var])
    mean_var["song_id"] = song_id
    return mean_var
    

def get_pt_pca(song: pd.core.frame.DataFrame, song_id: str) -> pd.core.frame.DataFrame:
    '''Performs PCA on Pitch and Timbre values in a single song segment
    '''
    pt_pca = pd.DataFrame(
        PCA(song, dims_rescaled_data=10),
        columns=[f"component_{i}" for i in range(1,11)])
    pt_pca["song_id"] = song_id
    return pt_pca

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
def length_check(analysis_objs: dict):
    """Checks the size of analysis objects to determine if they're large
    enough to save and clear
    """
    for key in analysis_objs.keys():
        if len(analysis_objs[key]) > 10000:
            save_object(analysis_objs[key], key)
            analysis_objs[key].clear()
    return    


def analysis_sorter(lst: list, fp: str) -> dict:
    '''Write me pls.
    '''
    sec_mean_vars = []
    pt_mean_vars = []
    pt_pcas = []

    #TODO: Replace with logging
    exceptions_dicts = []

    for record in tqdm(lst):
        song_id = record.replace('.json', '')
        try:
            with open(f'{fp}/{record}', 'r') as f:
                song = json.load(f)
        except Exception as e:
            exceptions_dicts.append({
                "song_id":song_id,
                "error":str(e)})
            continue
        
        # validate json
        validate_analysis_obj(song)

        # retrieve objects for analysis
        for_analysis = get_song_objects(song)

        # Obtaining section mean & variance 
        sec_mean_var = get_mean_var(for_analysis["song_sections"], song_id)
        sec_mean_vars.append(sec_mean_var)

        # pitch and timbre values
        pt_vals = get_mean_var(for_analysis["combined_pitch_timbre"], song_id)
        pt_mean_vars.append(pt_vals)

        pt_pca = get_pt_pca(for_analysis["combined_pitch_timbre"], song_id)
        pt_pcas.append(pt_pca)

        # saving objects
        length_check([sec_mean_vars, pt_mean_vars, pt_pcas])

    save_objects({
        sec_mean_vars:"sec_mean_vars",
        pt_mean_vars:"pt_mean_vars",
        pt_pcas:"pt_pcas"})
    return 

if __name__ == "__main__":
    
    files = db.from_sequence()
    files.map(analysis_sorter)