import numpy as np 
import pandas as pd 

import dask.dataframe as dd
from dask.distributed import Client 

from sklearn.metrics import jaccard_score

def get_jaccard()