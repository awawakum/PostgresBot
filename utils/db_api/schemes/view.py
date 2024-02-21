from utils.db_api.db_gino import TimedBaseModel
import sqlalchemy as sa


class View(TimedBaseModel):
    __tablename__ = 'view'
    
    view_id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    data_id = sa.Column(sa.String(50))
    user_id = sa.Column(sa.String(50))
    resource = sa.Column(sa.String(50))

    query: sa.sql.select