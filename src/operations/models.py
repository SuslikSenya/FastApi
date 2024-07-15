from sqlalchemy import Table, Column, Integer, String, TIMESTAMP

from database import metadata
operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String(150)),
    Column("figi", String(150)),
    Column("instrument_type", String(150), nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String(150)),
)
