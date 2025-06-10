from main import app
from database import get_db

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conversation.service import ConversationService
from conversation.exception import ConversationNotFoundException
from exception import RequiredColumnMissingException
from .exception import NodeSavedFailedException
from .model import Node
from .schema import NodeSchema

class NodeService:
    @staticmethod
    async def get_node(db: AsyncSession) -> list[Node]:
        """
        Get all nodes.
        """

        sql = select(Node)
        result = await db.execute(sql)
        nodes = result.scalars().all()
        return nodes

    @staticmethod
    async def create_node(db: AsyncSession, conversation_id, prompt, content, order) -> Node:
        """
        Create a new node.
        """
        if not conversation_id or order is None:
            message = f"conversation_id: {conversation_id}, order: {order}"
            exception = RequiredColumnMissingException(message=message)
            raise exception

        if not(conversation := await ConversationService.get_conversation_by_id(db, conversation_id)):
            message = f"conversation_id: {conversation_id}"
            exception = ConversationNotFoundException(message=message)
            raise exception

        schema = NodeSchema()
        data = schema.load({
            "conversation_id": conversation_id,
            "prompt": prompt,
            "content": content,
            "order": order
        })

        node = Node(**data)
        try:
            db.add(node)            # 將對象加入 session
            await db.commit()       # 提交到資料庫
            await db.refresh(node)  # 更新對象資料（例如拿到自動產生的 ID）

        except Exception as e:
            await db.rollback()     # 回滾事務

            message = f"error: {e}"
            exception = NodeSavedFailedException(message=message)
            raise exception

        return node
    
    @staticmethod
    async def update_node(db: AsyncSession, id: int, conversation_id, prompt, content, order) -> Node:
        """
        Update an existing node.
        """
        sql = select(Node).where(Node.id == id)
        result = await db.execute(sql)
        node = result.scalar_one_or_none()

        if node is None:
            raise ValueError("Node not found")

        node.conversation_id = conversation_id
        node.prompt = prompt
        node.content = content
        node.order = order
        await db.commit()
        await db.refresh(node)
        return node
    
    @staticmethod
    async def delete_node(db: AsyncSession, id: int) -> None:
        """
        Delete a conversation.
        """
        sql = select(Node).where(Node.id == id)
        result = await db.execute(sql)
        node = result.scalar_one_or_none()

        if node is None:
            raise ValueError("Node not found")

        await db.delete(node)
        await db.commit()
        return None