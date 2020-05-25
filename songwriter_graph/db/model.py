# to create OO tables + schemas
from sqlalchemy import (
    MetaData,
    Table,
    Column,
)
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

writers = Table(
    "writers",
    Column("wid", INTEGER),
    Column("writer_name", VARCHAR(length=50)),
    Column("ipi", INTEGER),
    Column("pro", VARCHAR(length=14)),
    )

neighbors = Table(
    "neighbors",
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

