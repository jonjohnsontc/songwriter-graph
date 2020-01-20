import json
import os
import logging
from datetime import date

import pandas as pd
import numpy as np
from numba import njit

from tqdm.auto import tqdm
from songwriter_graph.utils import get_files, save_object_np, save_objects_np

#TODO: Config
logging.basicConfig()


def get_mean_var(song_object: np.ndarray) -> np.ndarray:
    """Computes the mean and variance of an analysis json object passed
    through
    """
    mean = np.apply_along_axis(np.mean, 0, song_object)
    var = np.apply_along_axis(np.var, 0, song_object)
    return np.concatenate(mean, var)


def get_key_changes(song_keys: np.ndarray) -> int:
    kc = 0
    for item in np.nditer(song_keys):
        cur_key = item
        if cur_key != start_key:
            start_key = cur_key
            kc += 1
    return kc


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
    
    p = np.array(pitches)
    t = np.array(timbre)
    combined_pitch_timbre = np.concatenate([p, t])
    
    # Retrieve song segments
    song_sections = np.array(
        [list(item.values()) for item in analysis_obj["sections"]])

    return {
        "combined_pitch_timbre": combined_pitch_timbre,
        "song_sections": song_sections}


# Unit test this actually clears the list within the dictionary
def length_check(analysis_objs: dict, song_ids: list):
    """Checks the size of analysis objects to determine if they're large
    enough to save and clear
    """
    for key in analysis_objs.keys():
        if len(analysis_objs[key]) > 10000:
            save_object_np(analysis_objs[key], key, song_ids)
            analysis_objs[key].clear()
    return    


def analysis_sorter_numba(lst: list, fp: str):
    '''Write me pls.
    '''
    song_ids = []
    key_changes = []
    sec_mean_vars = []
    pt_mean_vars = []
    pt_pcas = []

    #TODO: Replacex with logging
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

        song_ids.append(song_id)

        # retrieve objects for analysis
        for_analysis = get_song_objects(song)

        # Obtaining section mean & variance 
        sec_mean_var = get_mean_var(for_analysis["song_sections"])
        sec_mean_vars.append(sec_mean_var)

        # grabbing key changes
        no_of_key_changes = get_key_changes(for_analysis["song_sections"])
        key_changes.append(no_of_key_changes)

        # pitch and timbre values
        pt_vals = get_mean_var(for_analysis["combined_pitch_timbre"])
        pt_mean_vars.append(pt_vals)

        pt_pca = PCA(
            for_analysis["combined_pitch_timbre"],
            dims_rescaled_data=10)
        pt_pcas.append(pt_pca)

        # saving objects
        length_check({
        "sec_mean_vars":sec_mean_vars,
        "pt_mean_vars":pt_mean_vars,
        "pt_pcas":pt_pcas,
        "key_changes":key_changes}, 
        song_ids
        )
    
    to_save = [
        {"object":sec_mean_vars, "object_type":"sec_mean_vars",
         "object_index":song_ids},
        {"object":pt_mean_vars, "object_type":"pt_mean_vars", 
        "object_index":song_ids},
        {"object":pt_pcas, "object_type":"pt_pcas",
        "object_index":song_ids},
        {"object":key_changes, "object_type":"key_changes", 
        "object_index":song_ids}
        ]

    save_objects_np(to_save)

    return


if __name__ == "__main__":
    pass