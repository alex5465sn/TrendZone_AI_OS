from app.database.session import engine
from app.models.user import User
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

if 'users' in tables:
    columns = inspector.get_columns('users')
    print('Tabela users já existe com colunas:')
    for col in columns:
        print(f'  - {col["name"]}: {col["type"]}')
else:
    print('Tabela users não existe. Criando...')
    User.metadata.create_all(engine)
    print('Tabela users criada!')
