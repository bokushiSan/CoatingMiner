import os
from sqlalchemy.schema import CreateSchema
import logging
from dotenv import load_dotenv
from src.db.database import engine, Base
from src.db.models import Paper

load_dotenv()

SCHEMA = os.getenv('POSTGRES_SCHEMA', 'schema')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """
    Создание схемы и таблиц.
    """
    with engine.connect() as conn:
        if not conn.dialect.has_schema(conn, SCHEMA):
            logger.info(f'Создание схемы {SCHEMA}...')
            conn.execute(CreateSchema(SCHEMA))
            conn.commit()
            logger.info(f'Схема {SCHEMA} создана')
        else:
            logger.info(f'Схема {SCHEMA} уже существует')

    logger.info('Создание всех таблиц...')
    Base.metadata.create_all(bind=engine)
    logger.info('Все таблицы успешно созданы или уже существуют!')

if __name__ == '__main__':
    print(Base.metadata.tables)
    create_tables()
