from utils.db_api.db_gino import TimedBaseModel
import sqlalchemy as sa


class Category(TimedBaseModel):
    __tablename__ = 'category'

    category_id = sa.Column(sa.String(100), primary_key=True)
    category_title = sa.Column(sa.String(25))

    query: sa.sql.select