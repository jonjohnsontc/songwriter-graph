import pathlib
import pytest
import random

import pandas as pd

from annoy import AnnoyIndex

from songwriter_graph.ann import (
    count_neighbors,
    combine_writer_counts_and_info,
)

TEST_DIR = pathlib.Path().absolute().parent


# @pytest.fixture
# def annoy_index():
#     to_annoy = pd.read_csv(f"{TEST_DIR}/fixtures/whatever.csv")    
    
#     pass


@pytest.fixture
def wid_contribid_mapping():
    """Object mapping of contribution id (`contribid`) to associated wid"""
    wids = [random.randint(1, 999999) for i in range(100)]
    wid_per_song = []
    for _ in range(1000):
        wid_per_song.append(random.choice(wids))

    mapping = dict(zip(list(range(1000)), wid_per_song))
    return mapping


def test_count_neighbors_returns_correct_object_mapping(mapping):
    """We expect that `count_neighbors` returns a dictionary of wid, Counter
    key value pairs
    """

    return


def test_count_neighbors_returns_counts_for_all_neighbors():
    return
