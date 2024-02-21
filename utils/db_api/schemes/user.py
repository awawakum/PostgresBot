from utils.db_api.db_gino import TimedBaseModel
import sqlalchemy as sa


class User(TimedBaseModel):
    __tablename__ = 'user'

    cid = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.BigInteger)
    first_name = sa.Column(sa.String(50))
    last_name = sa.Column(sa.String(50))
    username = sa.Column(sa.String(50))
    resource = sa.Column(sa.String(50))

    query: sa.sql.select