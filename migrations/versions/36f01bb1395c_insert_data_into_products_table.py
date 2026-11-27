"""Insert data into products table

Revision ID: 36f01bb1395c
Revises: ae7540f9c384
Create Date: 2026-11-26 13:01:35.410377

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '36f01bb1395c'
down_revision = 'ae7540f9c384'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = table('categories', column('id', sa.Integer), column('name', sa.String))

    products_table = table('products',
        column('name', sa.String),
        column('price', sa.Float),
        column('active', sa.Boolean),
        column('category_id', sa.Integer),
    )

    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'},
    ])

    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': 1},
        {'name': 'Smartphone LG', 'price': 800.0, 'active': True, 'category_id': 1},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': 2},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': 3},
    ])

def downgrade():
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Ultrabook', 'Laptop', 'Smartphone LG', 'Novel', 'T-Shirt');
    """)

    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)
