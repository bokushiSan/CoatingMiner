import uuid
from sqlalchemy import Column, Text, DateTime, Enum, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from src.db.database import Base


class Paper(Base):
    """
    Модель таблицы статьи.
    """
    __tablename__ = 'paper'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(
        Enum('pdf', 'doi', 'url', name='source_type_enum'),
        nullable=False
    )
    source_value = Column(Text, nullable=True)
    file_path = Column(Text, nullable=True)
    file_size = Column(Integer, nullable=True)
    status = Column(
        Enum(
            'uploaded',
            'queued',
            'processing',
            'completed',
            'failed',
            name='paper_status_enum'
        ),
        nullable=False,
        default='uploaded'
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
