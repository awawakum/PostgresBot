from utils.db_api.db_gino import db
from utils.db_api.schemes.user import User
from utils.db_api.schemes.product import Product
from utils.db_api.schemes.view import View
from utils.db_api.schemes.category import Category
from asyncpg import UniqueViolationError, UndefinedTableError


async def add_user(user_id: int, first_name: str, last_name: str, username: str, resource: str = 'telegram'):
    try:
        user = User(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            resource=resource)
        await user.create()
    except UniqueViolationError or UndefinedTableError:
        print('Пользователь не добавлен.')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def add_category(category_id: str, category_title: str):
    try:
        category = Category(
            category_id=category_id,
            category_title=category_title
            )
        await category.create()
    except UniqueViolationError or UndefinedTableError:
        print('Категория не добавлена.')


async def select_all_categories():
    categories = await Category.query.gino.all()
    return categories


async def count_categories():
    count = await db.func.count(Category.category_id).gino.scalar()
    return count


async def select_category(category_id):
    category = await Category.query.where(Category.category_id == category_id).gino.first()
    return category


async def delete_category(category_id: str):
    category = await Category.query.where(Category.category_id == category_id).gino.first()
    for product in await Product.query.where(Product.product_tag == category.category_title).gino.all():
        await product.delete()
    await category.delete()


async def add_product(product_id:str, product_title: str, product_body: str, product_photo: str, product_tag: str):
    try:
        product = Product(
            product_id=product_id,
            product_title=product_title,
            product_body=product_body,
            product_photo=product_photo,
            product_tag=product_tag
            )
        await product.create()
    except UniqueViolationError or UndefinedTableError:
        print('Продукт не добавлен.')


async def select_all_products():
    products = await Product.query.gino.all()
    return products


async def select_n_products(n: int):
    products = await Product.query.limit(n).gino.all()
    return products


async def count_products():
    count = await db.func.count(Product.product_id).gino.scalar()
    return count


async def select_product(product_id: str):
    product = await Product.query.where(Product.product_id == product_id).gino.first()
    return product


async def select_products_where():
    products = await Product.query.where().gino.all()
    return products


async def delete_product(product_id: str):
    product = await Product.query.where(Product.product_id == product_id).gino.first()
    await product.delete()


async def delete_product_in_category(category_id: str):
    products = await Product.query.where(Product.product_tag == category_id).gino.all()
    for product in products:
        await product.delete()


async def add_view(data_id: str, user_id: str, resource: str = 'telegram'):
    try:
        view = View(
            data_id=data_id,
            user_id=user_id,
            resource=resource
        )
        await view.create()
    except UniqueViolationError or UndefinedTableError:
        print('Просмотр не добавлен.')


async def select_where_product_tag(category_id: int):
    category = await Category.query.where(Category.category_id==category_id).gino.first()
    if category:
        products = await Product.query.where(Product.product_tag == category.category_title).gino.all()
        return products
    else:
        return None
