import sqlalchemy

metadata = sqlalchemy.MetaData()
items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=200), nullable=False),
    sqlalchemy.Column("price", sqlalchemy.String(length=100), nullable=False),
    sqlalchemy.Column("company", sqlalchemy.String(length=200), nullable=False),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime())
)