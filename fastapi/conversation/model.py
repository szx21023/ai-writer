from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Conversation(Base):
    __tablename__ = "conversation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(10), nullable=False)
    create_time = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    update_time = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)