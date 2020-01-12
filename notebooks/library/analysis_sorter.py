import json
import os
import logging
from datetime import date

import pandas as pd
import numpy as np
# Note - not yet used
import dask.bag as db

from tqdm.auto import tqdm
from library.utils import save_object, save_objects

#TODO: Config
logging.basicConfig()

def get_mean_var(song_object: pd.core.frame.DataFrame, song_id: str) -> pd.core.frame.DataFrame:
    """Computes the mean and variance of an analysis json object passed
    through
    """
    mean_var = song_object.agg([np.mean, np.var])
    mean_var["song_id"] = song_id
    return mean_var


# def pt_grabber(filepath):
#     '''
#     Retrieves pitch and timbre summary statistics for every song in
#     audio_analysis folder.
#     '''
#     # timbre_means = []
#     # timbre_var = []
#     # pitch_means = []
#     # pitch_var = []
#     timbre_means = {}
#     timbre_var = {}
#     pitch_means = {}
#     pitch_var = {}
#     errors = {}
#     count = 0

#     aa_directory = os.listdir(filepath)
#     audio_analysis_files = list(filter(lambda x: '.json' in str(x), aa_directory))

#     for record in audio_analysis_files:
#         try: 
#             with open(f'{filepath}/{record}', 'r') as f:
#                 analysis = json.load(f)
#         except Exception as e:
#             print(f'unable to pull {record}, {str(e)}')
#             errors[record] = str(e)
#         if isinstance(analysis, dict):
#             if 'segments' in analysis:
#                 try:
#                     pm, tm, pv, tv = get_pt_mean_var(analysis)
#                 except:
#                     response = f"unable to gather summary stats \
#                         for song {record.replace('.json', '')} pitch & timbre"
#         try:
#             timbre_means[record.replace(".json", "")] = {'timbre_means' : tm.tolist()}
#             timbre_var[record.replace(".json", "")] = {'timbre_var' : tv.tolist()}
#             pitch_means[record.replace(".json", "")] = {'pitch_means' : pm.tolist()}
#             pitch_var[record.replace(".json", "")] = {'pitch_var' : pv.tolist()}
#         except Exception as e:
#             timbre_means[record.replace(".json", "")] = str(e)
#             timbre_var[record.replace(".json", "")] = str(e)
#             pitch_means[record.replace(".json", "")] = str(e)
#             pitch_var[record.replace(".json", "")] = str(e) 
#         # try:
#         #     timbre_means.append(dict({record.replace(".json", ""):tm}))
#         #     timbre_var.append(dict({record.replace(".json", ""):tv}))
#         #     pitch_means.append(dict({record.replace(".json", ""):pm}))
#         #     pitch_var.append(dict({record.replace(".json", ""):pv}))
#         # except:
#         #     [lists.append(response) for lists in [timbre_means, timbre_var, 
#         #                                           pitch_means, pitch_var]]
#         count += 1
#         if count % 10000 == 0:
#             print("grabbing {}".format(count + 1))
#         if count % 100000 == 0:
#             print("Saving results to file")
#             with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/timbre_means_{count}.json', 'w') as f:
#                 json.dump(timbre_means, f)
#             with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/timbre_var_{count}.json', 'w') as f:
#                 json.dump(timbre_var, f)
#             with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/pitch_means_{count}.json', 'w') as f:
#                 json.dump(pitch_means, f)    
#             with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/pitch_var_{count}.json', 'w') as f:
#                 json.dump(pitch_var, f)
#             for d in [timbre_means, timbre_var, pitch_means, pitch_var]:
#                 d.clear()
#     with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/timbre_means_{count}.json', 'w') as f:
#         json.dump(timbre_means, f)
#     with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/timbre_var_{count}.json', 'w') as f:
#         json.dump(timbre_var, f)
#     with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/pitch_means_{count}.json', 'w') as f:
#         json.dump(pitch_means, f)    
#     with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/pitch_var_{count}.json', 'w') as f:
#         json.dump(pitch_var, f)
#     with open(f'/home/jovyan/SWI_data/data/interim/pitch_timbre_means_vars/errors_{count}.json', 'w') as f:
#         json.dump(errors, f)    
#     return 'finished'
    

def get_pt_pca(song: pd.core.frame.DataFrame, song_id: str) -> pd.core.frame.DataFrame:
    '''Performs PCA on Pitch and Timbre values in a single song segment
    '''

    return 

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


# def pt_pca_grabber(filepath : str) -> str:
#     '''Retrieves pitch and timbre summary statistics for every song in 
#     audio_analysis folder.
#     '''
#     timbre_dict= {}
#     pitch_dict = {}
#     errors = {}
#     count = 0
#     cd = date.today().strftime('%Y%m%d')

#     aa_directory = os.listdir(filepath)
#     audio_analysis_files = list(filter(lambda x: '.json' in str(x), 
#                                                 aa_directory))

#     for record in audio_analysis_files:
#         try: 
#             with open(f'{filepath}/{record}', 'r') as f:
#                 analysis = json.load(f)
#         except FileNotFoundError as fe:
#             print(f'unable to pull {record}, {str(fe)}')
#             errors[record] = str(fe)

#         if isinstance(analysis, dict):
#             if 'segments' in analysis:
#                 try:
#                     pitch_pca, timbre_pca = get(record)
#                     pitch_dict[record] = pitch_pca
#                     timbre_dict[record] = timbre_pca
#                 except Exception as e:
#                     errors[record] = str(e)
#             else: 
#                 errors[record] = 'Segments not available in aa file'
#         else:
#             errors[record] = 'File is not a dict'
        
#         count += 1

#         if count % 100000 == 0:
#             print('{count} records completed')
#             with open(f'/home/jovyan/SWI_data/data/interim/pitch_pca/pitch_pca_{count}_{cd}.json', 'w') as f:
#                 json.dump(pitch_dict, f)
#             with open(f'/home/jovyan/SWI_data/data/interim/timbre_pca/timbre_pca_{count}_{cd}.json', 'w') as f:
#                 json.dump(timbre_dict, f)
#     with open(f'/home/jovyan/SWI_data/data/interim/pitch_pca/pitch_pca_{count}_{cd}.json', 'w') as f:
#         json.dump(pitch_dict, f)
#     with open(f'/home/jovyan/SWI_data/data/interim/timbre_pca/timbre_pca_{count}_{cd}.json', 'w') as f:
#         json.dump(timbre_dict, f)
#     return "finished"


def length_check(analysis_objs: dict):
    """Checks the size of analysis objects to determine if they're large
    enough to save and clear
    """
    pass

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
        if len(sec_mean_vars) > 10000:
            save_object(sec_mean_vars, object_type="sec_mean_vars")
            sec_mean_vars.clear()

        if len(pt_mean_vars) > 10000:
            save_object(pt_mean_vars, object_type="pt_mean_vars")
            pt_mean_vars.clear()

        if len(pt_pcas) > 10000:
            save_object(pt_pcas, object_type="pt_pcas")
            pt_pcas.clear()

    save_objects([sec_mean_vars, pt_mean_vars, ])
    return 

if __name__ == "__main__":
    pass
        