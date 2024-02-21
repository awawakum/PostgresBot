from utils.db_api.db_gino import TimedBaseModel
import sqlalchemy as sa


class Product(TimedBaseModel):
    __tablename__ = 'product'

    product_id = sa.Column(sa.String(100), primary_key=True)
    product_title = sa.Column(sa.String(50))
    product_body = sa.Column(sa.String(50))
    product_photo = sa.Column(sa.LargeBinary)
    product_tag = sa.Column(sa.String(50))

    query: sa.sql.select