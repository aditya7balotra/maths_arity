from sqlalchemy import Column, Integer, String, Table, MetaData, CheckConstraint

reviews_metadata= MetaData()

reviews_table = Table(
    "reviews",
    reviews_metadata,
    Column("id", Integer, primary_key= True),
    Column("name", String(50), nullable= False),
    Column("institute", String(50), nullable= False),
    Column("comment", String(1000), nullable= False),
    Column("rate", Integer, nullable= False),
    # constraints
    CheckConstraint("rate BETWEEN 1 AND 5", name="rate_range_check"),
    CheckConstraint("CHAR_LENGTH(name) <= 50", name="name_max_length"),
    CheckConstraint("CHAR_LENGTH(institute) <= 50", name="institute_max_length"),
    CheckConstraint("CHAR_LENGTH(comment) <= 1000", name="comment_max_length"),

    CheckConstraint("CHAR_LENGTH(name) >= 2", name="name_min_length"),
    CheckConstraint("CHAR_LENGTH(institute) >= 2", name="institute_min_length"),
    CheckConstraint("CHAR_LENGTH(comment) >= 5", name="comment_min_length"),
)

