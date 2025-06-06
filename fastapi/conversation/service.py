from main import app
from database import get_db

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exception import RequiredColumnMissingException
from .exception import ConversationNotFoundException, ConversationAlreadyExistException, ConversationSavedFailedException
from .model import Conversation
from .schema import ConversationSchema

class ConversationService:
    @staticmethod
    async def get_conversation(db: AsyncSession) -> list[Conversation]:
        """
        Get all conversations.
        """

        sql = select(Conversation).where(Conversation.title.isnot(None))
        result = await db.execute(sql)
        conversations = result.scalars().all()
        return conversations

    @staticmethod
    async def create_conversation(db: AsyncSession, title: str) -> Conversation:
        """
        Create a new conversation.
        """
        if not title:
            message = f"title: {title}"
            exception = RequiredColumnMissingException(message=message)
            raise exception

        if conversation := await ConversationService.get_conversation_by_title(db, title):
            message = f"title: {title}"
            exception = ConversationAlreadyExistException(message=message)
            raise exception

        schema = ConversationSchema()
        data = schema.load({"title": title})

        conversation = Conversation(**data)
        try:
            db.add(conversation)            # 將對象加入 session
            await db.commit()               # 提交到資料庫
            await db.refresh(conversation)  # 更新對象資料（例如拿到自動產生的 ID）

        except Exception as e:
            await db.rollback()             # 回滾事務

            message = f"error: {e}"
            exception = ConversationSavedFailedException(message=message)
            raise exception

        return conversation
    
    @staticmethod
    async def update_conversation(db: AsyncSession, id: int, title: str) -> Conversation:
        """
        Update an existing conversation.
        """
        if not title:
            message = f"title: {title}"
            exception = RequiredColumnMissingException(message=message)
            raise exception

        if conversation := await ConversationService.get_conversation_by_title(db, title):
            message = f"title: {title}"
            exception = ConversationAlreadyExistException(message=message)
            raise exception

        if not(conversation := await ConversationService.get_conversation_by_id(db, id)):
            message = f"id: {id}"
            exception = ConversationNotFoundException(message=message)
            raise exception

        schema = ConversationSchema()
        data = schema.load({"title": title})
        for key, value in data.items():
            setattr(conversation, key, value)

        try:
            await db.commit()
            await db.refresh(conversation)

        except Exception as e:
            await db.rollback()

            message = f"error: {e}"
            exception = ConversationSavedFailedException(message=message)
            raise exception

        return conversation
    
    @staticmethod
    async def delete_conversation(db: AsyncSession, id: int) -> None:
        """
        Delete a conversation.
        """
        if not(conversation := await ConversationService.get_conversation_by_id(db, id)):
            message = f"id: {id}"
            exception = ConversationNotFoundException(message=message)
            raise exception

        try:
            await db.delete(conversation)
            await db.commit()

        except Exception as e:
            await db.rollback()

            message = f"error: {e}"
            exception = ConversationSavedFailedException(message=message)
            raise exception

        return conversation

    @staticmethod
    async def get_conversation_by_id(db: AsyncSession, id: int) -> Conversation:
        """
        Get a conversation by ID.
        """

        sql = select(Conversation).where(Conversation.id == id)
        result = await db.execute(sql)
        conversation = result.scalar_one_or_none()
        return conversation

    @staticmethod
    async def get_conversation_by_title(db: AsyncSession, title: str) -> Conversation:
        """
        Get a conversation by title.
        """

        sql = select(Conversation).where(Conversation.title == title)
        result = await db.execute(sql)
        conversation = result.scalar_one_or_none()
        return conversation