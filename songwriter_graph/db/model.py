from sqlalchemy import (
    MetaData,
    Table,
    Column,
)
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from songwriter_graph.api import db

class Writers(db.Model):
    wid = db.Column(db.Integer, primary_key=True)
    writer_name = db.Column(db.String(50))
    ipi = db.Column(db.Integer)
    pro = db.Column(db.String(14))

class Neighbors(db.Model):
    wid = db.Column(db.Integer, primary_key=True)
    top_match_1 = db.Column(db.Integer)
    top_match_1_count = db.Column(db.Integer)
    top_match_2 = db.Column(db.Integer)
    top_match_2_count = db.Column(db.Integer)
    top_match_3 = db.Column(db.Integer)
    top_match_3_count = db.Column(db.Integer)
    top_match_4 = db.Column(db.Integer)
    top_match_4_count = db.Column(db.Integer)
    top_match_5 = db.Column(db.Integer)
    top_match_5_count = db.Column(db.Integer)
    top_match_6 = db.Column(db.Integer)
    top_match_6_count = db.Column(db.Integer)
    top_match_7 = db.Column(db.Integer)
    top_match_7_count = db.Column(db.Integer)
    top_match_8 = db.Column(db.Integer)
    top_match_8_count = db.Column(db.Integer)
    top_match_9 = db.Column(db.Integer)
    top_match_9_count = db.Column(db.Integer)
    top_match_10 = db.Column(db.Integer)
    top_match_10_count = db.Column(db.Integer)


writers = Table(
    "writers",
    MetaData(),
    Column("wid", INTEGER),
    Column("writer_name", VARCHAR(length=50)),
    Column("ipi", INTEGER),
    Column("pro", VARCHAR(length=14)),
    )

neighbors = Table(
    "neighbors",
    MetaData(),
    Column("wid", INTEGER),
    Column("top_match_1", INTEGER),
    Column("top_match_1_count", INTEGER),
    Column("top_match_2", INTEGER),
    Column("top_match_2_count", INTEGER),
    Column("top_match_3", INTEGER),
    Column("top_match_3_count", INTEGER),
    Column("top_match_4", INTEGER),
    Column("top_match_4_count", INTEGER),
    Column("top_match_5", INTEGER),
    Column("top_match_5_count", INTEGER),
    Column("top_match_6", INTEGER),
    Column("top_match_6_count", INTEGER),
    Column("top_match_7", INTEGER),
    Column("top_match_7_count", INTEGER),
    Column("top_match_8", INTEGER),
    Column("top_match_8_count", INTEGER),
    Column("top_match_9", INTEGER),
    Column("top_match_9_count", INTEGER),
    Column("top_match_10", INTEGER),
    Column("top_match_10_count", INTEGER),
)

