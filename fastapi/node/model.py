from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Node(Base):
    __tablename__ = "Node"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    order: Mapped[float] = mapped_column(Float, nullable=False)
    create_time = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    update_time = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)