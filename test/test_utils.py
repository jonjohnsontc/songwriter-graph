import pytest

from secrets import token_hex
from numpy.random import randint
from numpy import array
import pandas as pd

from songwriter_graph.utils import save_object_np
from songwriter_graph.config import section_mean_var_cols

@pytest.fixture
def test_sec_means_vars():
    means_vars = [randint(-300,500,size=25) for i in range(10000)]
    return means_vars


@pytest.fixture
def test_song_ids():
    song_ids = [token_hex(nbytes=6) for i in range(10000)] 
    return song_ids

@pytest.fixture
def test_song_object_means_vars(test_sec_means_vars, test_song_ids):
    song_object_means_vars = {
                    "object": test_sec_means_vars,
                    "object_type": "sec_mean_vars",
                    "object_index": test_song_ids,
                    "columns": section_mean_var_cols}
    return song_object_means_vars

def test_save_object_np_correctly_applies_rows_and_columns(test_song_object_means_vars):
    nc = test_song_object_means_vars
    df = pd.DataFrame(data=nc["object"],
                      index=nc["object_index"],
                      columns=nc["columns"])
    return

