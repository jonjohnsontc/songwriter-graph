import json
import os
import logging
from datetime import date

import pandas as pd
import numpy as np
from numba import jit, njit

from tqdm.auto import tqdm
from songwriter_graph.utils import get_files, save_object_np, save_objects_np
from songwriter_graph.config import key_changes_cols, pt_mean_var_cols, pt_pca_cols, section_mean_var_cols

#TODO: Config
logging.basicConfig()

def get_mean_var(song_object: np.ndarray) -> np.ndarray:
    """Computes the mean and variance of an analysis json object passed
    through
    """
    mean = np.mean(song_object, axis=0)
    var = np.var(song_object, axis=0)
    return np.concatenate([mean, var])


def get_key_changes(song_keys: np.ndarray) -> int:
    if len(song_keys)==1:
        return 0
    else:
        start_key = song_keys[0]

    kc = 0
    for item in np.nditer(song_keys):
        cur_key = item
        if cur_key != start_key:
            start_key = cur_key
            kc += 1
    return kc


# https://stackoverflow.com/a/13224592
def PCA(data: np.ndarray, dims_rescaled_data: int = 10) -> np.ndarray:
    """
    returns: data transformed in 2 dims/columns + regenerated original data
    pass in: data as 2D NumPy array
    """
    # transpose the data
    data = data.T
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


# TODO: Refactor this to take in dict like `save_objects`
# Unit test this actually clears the list within the dictionary
def length_check(analysis_objs: list):
    """Checks the size of analysis objects to determine if they're large
    enough to save and clear
    """
    for i in range(len(analysis_objs)):
        if len(analysis_objs[i]["object"]) > 10000:
            save_object_np(
                analysis_objs[i]["object"], 
                analysis_objs[i]["object_type"], 
                analysis_objs[i]["columns"], 
                analysis_objs[i]["object_index"])
            analysis_objs[i]["object"].clear()
            analysis_objs[i]["object_index"].clear()
    return    


def _append_key_change_to_section(
    song_section: np.ndarray, key_change: int) -> np.ndarray:
    return np.append(song_section, key_change)


def analysis_sorter_numba(lst: list, fp: str):
    '''Write me pls.
    '''
    song_ids = []
    sec_mean_vars_kc = []
    pt_mean_vars = []
    # pt_pcas = []


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

        # grabbing key changes & adding to section
        no_of_key_changes = get_key_changes(for_analysis["song_sections"][:, 6])        
        sec_mean_var_kc = _append_key_change_to_section(sec_mean_var, no_of_key_changes)
        sec_mean_vars_kc.append(sec_mean_var_kc)

        # pitch and timbre values
        pt_vals = get_mean_var(for_analysis["combined_pitch_timbre"])
        pt_mean_vars.append(pt_vals)

        # pt_pca = PCA(
        #     for_analysis["combined_pitch_timbre"],
        #     dims_rescaled_data=10)
        # pt_pcas.append(pt_pca)

        # saving objects
        # TODO: refactor dictionary being passed through
        length_check([
            {"object":sec_mean_vars_kc, "object_type":"sec_mean_vars",
            "object_index":song_ids, "columns":section_mean_var_cols},
            {"object":pt_mean_vars, "object_type":"pt_mean_vars", 
            "object_index":song_ids, "columns":pt_mean_var_cols},
            # {"object":pt_pcas, "object_type":"pt_pcas",
            # "object_index":song_ids, "columns":pt_pca_cols},
            ]
        )
    
    
    ###### ALSO PART OF KEY CHANGE SECTION ######
    to_save = [
        {"object":sec_mean_vars_kc, "object_type":"sec_mean_vars",
         "object_index":song_ids, "columns":section_mean_var_cols},
        {"object":pt_mean_vars, "object_type":"pt_mean_vars", 
        "object_index":song_ids, "columns":pt_mean_var_cols},
        # {"object":pt_pcas, "object_type":"pt_pcas",
        # "object_index":song_ids, "columns":pt_pca_cols},
        ]

    save_objects_np(to_save)

    return


if __name__ == "__main__":
    pass