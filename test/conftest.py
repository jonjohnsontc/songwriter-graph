import pytest
import json
import os

from typing import List
from numpy.random import choice, normal, randint, random
from secrets import token_hex

from songwriter_graph.config import section_mean_var_cols

filepath = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture
def test_sec_means_vars():
    means_vars = [randint(-300, 500, size=25) for i in range(10000)]
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
        "columns": section_mean_var_cols,
    }
    return song_object_means_vars


@pytest.fixture(scope="function")
def test_song() -> dict:
    with open(f"{filepath}/fixtures/example_song_analysis.json", "r") as f:
        song = json.load(f)
    return song