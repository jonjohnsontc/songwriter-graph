# a script to migrate my data from csv + annoy index to sql
import json
import pandas as pd
import sqlalchemy
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from .utils import connect



# might just do this through pandas in ipython
def writers_to_db(connection, writers_df):
    """Uploads writers dataframe to SQL table"""
    writers_df.to_sql(
        "writers",
        connection,
        if_exists="replace",
        index=False,
        dtype={
            "wid": INTEGER,
            "writer_name": VARCHAR(50),
            "ipi": INTEGER,
            "pro": VARCHAR(14),
        }
    )
    return

def convert_results_dict_to_all_ints(results, writers):
    """Converts the `writers_and_counts` styled dictionaries I had created
    through nbs to a dictionary which represents every feature as an integer
    to hopefully save on some space + redundancy
    """
    int_results = []
    for i in results.keys():
        top_matches = {}
        top_matches["wid"] = i

        # starts at index 1 because the 0th indexed item is always the
        # same writer as the writer themselves
        for j in range(1, len(results[i]["top_matches"])): 
            top_matches[f"top_match_{j}"] = results[i]["top_matches"][j][0]
            top_matches[f"top_match_{j}_count"] = results[i]["top_matches"][j][1] 
        int_results.append(top_matches)
    return int_results


def jsonify_and_dump(int_results, filepath):
    with open(filepath, "w") as f:
        json.dump(int_results, f)
    return