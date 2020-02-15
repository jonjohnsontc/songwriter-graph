import pandas as pd
import numpy as np


def mk_sum_df(summary):
    """
    Make df of summary stats for timbre/pitch values in audio analysis
    """
    sum_df = pd.DataFrame(columns=["dim_" + str(i) for i in range(1, 13)])

    for e in summary:
        sum_df.loc[list(e.keys())[0]] = list(e.values())[0]
    return sum_df
