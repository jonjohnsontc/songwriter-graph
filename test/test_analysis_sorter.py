import json

from songwriter_graph.analysis_sorter import get_mean_var, get_key_changes, validate_analysis_obj
from songwriter_graph.utils import save_object_np
import pytest

import numpy as np
import pandas as pd


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

# TODO: I'm not quite sure what form this is going to take. But at least one calculation
#       `get_key_changes` is based on the position in the array that a value is assigned to
#       , but I don't know if the order will always stay the same (i.e., `key` is always
#       the sixth field in song sections within an analysis obj)
def test_analysis_sorter_preserves_order():
    pass
