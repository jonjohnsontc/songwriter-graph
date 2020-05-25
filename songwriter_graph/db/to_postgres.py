# coding: utf-8
import pandas as pd
writers = pd.read_csv("data/writers.csv", index_col=0)
writers.head()
max(writers.WID.values())
max(writers.WID.values)
import pickle
with open("data/ai/swg_model/writers_and_counts_20200503.pkl", "rb") as f:
    results = pickle.load(f)
    
results[3]
writers_dict = writers.to_dict(orient="index")
writers_dict[0]
len(results[3]["top_matches"])
max(results.keys())
def convert_results_dict_to_all_ints(results, writers):
    """Converts the `writers_and_counts` styled dictionaries I had created
    through nbs to a dictionary which represents every feature as an integer
    to hopefully save on some space + redundancy
    """
    int_results = []
    for i in results.keys():
        int_results.append(
            {
                "wid": i,
                "top_match_1": results[i]["top_matches"][1][0],
                "top_match_1_count": results[i]["top_matches"][1][1],
                "top_match_2": results[i]["top_matches"][2][0],
                "top_match_2_count": results[i]["top_matches"][2][1],
                "top_match_3": results[i]["top_matches"][3][0],
                "top_match_3_count": results[i]["top_matches"][3][1],
                "top_match_4": results[i]["top_matches"][4][0],
                "top_match_4_count": results[i]["top_matches"][4][1],
                "top_match_5": results[i]["top_matches"][5][0],
                "top_match_5_count": results[i]["top_matches"][5][1],
                "top_match_6": results[i]["top_matches"][6][0],
                "top_match_6_count": results[i]["top_matches"][6][1],
                "top_match_7": results[i]["top_matches"][7][0],
                "top_match_7_count": results[i]["top_matches"][7][1],
                "top_match_8": results[i]["top_matches"][8][0],
                "top_match_8_count": results[i]["top_matches"][8][1],
                "top_match_9": results[i]["top_matches"][9][0],
                "top_match_9_count": results[i]["top_matches"][9][1],
                "top_match_10": results[i]["top_matches"][10][0],
                "top_match_10_count": results[i]["top_matches"][10][1],
            }
        )
    return int_results
    
get_ipython().run_line_magic('who', '')
int_results = convert_results_dict_to_all_ints(results, writers_dict)
len(results[3]["top_matches"])
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
    
int_results = convert_results_dict_to_all_ints(results, writers_dict)
int_results[0]
def jsonify_and_dump(int_results, filepath):
    enc_results = json.JSONEncoder().encode(int_results)
    with open(filepath, "w") as f:
        json.dump(enc_results, f)
    return
    
path = "data/ai/swg_model/writers_counts_just_ints.json"
jsonify_and_dump(int_results, path)
import json
jsonify_and_dump(int_results, path)
def jsonify_and_dump(int_results, filepath):
    # enc_results = json.JSONEncoder().encode(int_results)
    with open(filepath, "w") as f:
        json.dump(int_results, f)
    return
    
jsonify_and_dump(int_results, path)
get_ipython().run_line_magic('pinfo', 'writers.to_sql')
writers.columns
PG_PASSWORD = "4NB9h68eRDch4K2fj7tkRwGw"
DRIVER = "postgresql+psycopg2"
def connect():
    """Generates connection to postgres db
    
    Returns:
        connection object
    """
    engine = create_engine(f"{DRIVER}://postgres:{PG_PASSWORD}@localhost:5432/postgres")
    return engine.connect()
    
conn = connect()
from sqlalchemy.engine import create_engine
conn = connect()
writers_df.to_sql(
        "writers",
        conn,
        if_exists="replace",
        index=False,
        dtype={
            "wid": INTEGER,
            "writer_name": VARCHAR(50),
            "ipi": INTEGER,
            "pro": VARCHAR(14),
        }
    )
writers.to_sql(
        "writers",
        conn,
        if_exists="replace",
        index=False,
        dtype={
            "wid": INTEGER,
            "writer_name": VARCHAR(50),
            "ipi": INTEGER,
            "pro": VARCHAR(14),
        }
    )
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
writers.to_sql(
        "writers",
        conn,
        if_exists="replace",
        index=False,
        dtype={
            "wid": INTEGER,
            "writer_name": VARCHAR(50),
            "ipi": INTEGER,
            "pro": VARCHAR(14),
        }
    )
type(int_results)
df = pd.DataFrame(int_results)
df.head()
df = pd.DataFrame(int_results, dtype=int)
df.head()
df.to_sql("neighbors", conn, if_exists="replace", index=False)
