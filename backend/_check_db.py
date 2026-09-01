from app.database.session import engine
from app.models.product import Product
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print('Tabelas no banco:', tables)

if 'products' in tables:
    columns = inspector.get_columns('products')
    print('\nColunas da tabela products:')
    for col in columns:
        print(f'  - {col["name"]}: {col["type"]}')
else:
    print('\nTabela products NÃO existe. Criando...')
    Product.metadata.create_all(engine)
    print('Tabela products criada com sucesso!')
