import numpy as np
import pandas as pd

def get_sec_ss(dicts):
    '''
    Create df out of section summary stats in `mean_dicts` and `var_dicts`.
    '''
    sum_stats_df = pd.DataFrame(columns=['confidence', 'duration', 'loudness', 'mode',
                                        'mode_confidence', 'tempo', 'tempo_confidence'])

    for e in dicts:
        sum_stats_df.loc[list(e.keys())[0]] = list(e.values())[0]
    return sum_stats_df