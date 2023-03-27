import sqlalchemy

metadata = sqlalchemy.MetaData()
settings = sqlalchemy.Table(
    "settings",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=200), nullable=False),
    sqlalchemy.Column("value", sqlalchemy.String(length=500), nullable=False),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime())
)