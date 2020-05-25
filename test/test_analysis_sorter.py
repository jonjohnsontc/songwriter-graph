import json

from songwriter_graph.analysis_sorter import get_mean_var
from songwriter_graph.utils import save_object_np
import pytest

import numpy as np
import pandas as pd

@pytest.fixture



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


def get_key_changes_produces_accurate_no():
    pass


def validate_analysis_obj_properly_throws_exception():
    pass


def length_check_properly_clears_analysis_obj_dict():
    pass


def length_check_properly_checks_object_lenghts():
    pass

# Need:
# list of song ids
# a fake song fixture,
# monkeypatched functions (or do i?):
# - get_song_objects
# - get_mean_var
# - get_key_changes
# - On second thought, i'll say no for now


def test_analysis_sorter_preserves_order():
    pass
