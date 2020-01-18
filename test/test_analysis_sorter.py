import json

from songwriter_graph.analysis_sorter import get_mean_var
import pytest

import numpy as np 
import pandas as pd 

#TODO: Add some actual test here
# currently takes an assload of time to run
# def test_get_mean_var_returns_mean_and_variance():
#     test_file = glob.glob("/home/jovyan/SWI_data/data/audio_analysis/*.json")
#     with open(file_listing[0], 'r') as f:
#         test_json_obj = json.load(f)
#     test_mean_var = get_mean_var(test_json_obj)
#     assert len(test_mean_var) > 5


def test_get_pt_pca_produces_accurate_pca():
    pass


def test_PCA_result_can_map_back_to_original_data():
    pass

