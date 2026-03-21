import uuid
from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
from src.db.database import Base


source_type_enum = ENUM(
    'pdf', 'doi', 'url',
    name='source_type_enum',
    create_type=True
)

paper_status_enum = ENUM(
    'uploaded',
    'queued',
    'processing',
    'text_extracted',
    'extracted',
    'completed',
    'failed',
    name='paper_status_enum',
    create_type=True
)


class Paper(Base):
    """
    Модель таблицы статьи.
    """
    __tablename__ = 'paper'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(source_type_enum, nullable=False, comment='Тип источника: pdf - загруженный файл, doi - '
                                                                   'цифровой идентификатор, url - ссылка')
    source_value = Column(Text, nullable=True)
    file_path = Column(Text, nullable=True)
    file_size = Column(Integer, nullable=True)
    status = Column(paper_status_enum, nullable=False, default='uploaded', comment='Статус обработки статьи: uploaded '
                                                                                   '- загружен, processing - в '
                                                                                   'обработке, completed - завершен '
                                                                                   'успешно, failed - завершен '
                                                                                   'неуспешно')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    extracted_data = relationship(argument='ExtractedData', back_populates='paper', uselist=False)


class ExtractedData(Base):
    __tablename__ = 'extracted_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(UUID(as_uuid=True), ForeignKey('paper.id'), nullable=False, unique=True)
    title = Column(Text, nullable=True)
    authors = Column(JSONB, nullable=True)
    year = Column(Integer, nullable=True)
    coating_material = Column(Text, nullable=True)
    # TODO: здесь нужно добавить новые колонки (тип нанесения, материал, микротвердость, толщина, класс адгезии и пр.)
    raw_json = Column(JSONB, nullable=True)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())

    paper = relationship(argument='Paper', back_populates='extracted_data')
