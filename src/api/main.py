import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.routes import paper
from sqlalchemy.schema import CreateSchema
from src.db.database import engine, Base
from src.db.models import Paper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCHEMA = os.getenv('POSTGRES_SCHEMA', 'schema')

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    yield

app = FastAPI(
    title='CoatingMiner API',
    version='0.1',
    lifespan=lifespan
)

app.include_router(paper.router)