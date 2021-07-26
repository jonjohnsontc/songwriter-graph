import json

from songwriter_graph.analysis_sorter import get_mean_var, get_key_changes, validate_analysis_obj
from songwriter_graph.utils import save_object_np
import pytest

import numpy as np
import pandas as pd


# TODO: Don't think this is worth testing -- just concats np.mean + np.var
def test_get_mean_var_returns_mean_and_variance():
    pass


# TODO: Should I be doing this? Do I need to test PCA? Can I test it?
def test_get_pt_pca_produces_accurate_pca():
    pass


# TODO: Hasn't been implemented yet
def test_PCA_result_can_map_back_to_original_data():
    pass


def test_get_key_changes_produces_accurate_no():
    # Should change 7 times
    keys = np.array([0, 3, 4, 8, 0, 7, 9, 4, 4])
    expected = 7
    actual = get_key_changes(keys)
    assert actual == expected


def test_validate_analysis_obj_throws_exceptions_for_bad_data(test_song):
    song_no_sections = test_song.copy()
    song_no_sections.pop('sections')
    with pytest.raises(ValueError):
        validate_analysis_obj(song_no_sections)


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
