from main import app
from database import get_db

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conversation.service import ConversationService
from conversation.exception import ConversationNotFoundException
from ext.openai.service import OpenaiService
from exception import RequiredColumnMissingException
from .const import prompt_message_1, prompt_message_2, prompt_message_3
from .exception import NodeSavedFailedException, NodeNotFoundException
from .model import Node
from .schema import NodeSchema, CreateNodeSchema

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
    async def create_node(db: AsyncSession, **kwargs) -> Node:
        """
        Create a new node.
        """

        schema = CreateNodeSchema()
        data = schema.load(kwargs)
        conversation_id = data.get("conversation_id")
        prompt = data.get("prompt")
        content = data.get("content")
        last_node_id = data.get("last_node_id")
        next_node_id = data.get("next_node_id")

        if not conversation_id:
            message = f"conversation_id: {conversation_id}"
            exception = RequiredColumnMissingException(message=message)
            raise exception

        if not(conversation := await ConversationService.get_conversation_by_id(db, conversation_id)):
            message = f"conversation_id: {conversation_id}"
            exception = ConversationNotFoundException(message=message)
            raise exception

        last_node = await NodeService.get_node_by_id(db, last_node_id)
        next_node = await NodeService.get_node_by_id(db, next_node_id)
        if not last_node and not next_node:
            order = 1
            prompt_message = prompt_message_1.format(user_prompt=prompt)

        elif last_node and not next_node:
            order = last_node.order + 1
            prompt_message = prompt_message_2.format(user_prompt=prompt, last_content=last_node.content)

        elif last_node and next_node:
            order = (last_node.order + next_node.order) / 2
            prompt_message = prompt_message_3.format(
                user_prompt=prompt,
                last_content=last_node.content,
                next_content=next_node.content
            )

        if not content:
            content = await OpenaiService.get_completion(prompt_message)  # 呼叫 OpenAI API 獲取回應

        data['order'] = order
        data['content'] = str(content)

        schema = NodeSchema()
        data = schema.load(data)
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
    async def update_node(db: AsyncSession, id: int, **kargs) -> Node:
        """
        Update an existing node.
        """
        if not(node := await NodeService.get_node_by_id(db, id)):
            message = f"id: {id}"
            exception = NodeNotFoundException(message=message)
            raise exception

        schema = NodeSchema()
        data = schema.load(kargs)
        for key, value in data.items():
                setattr(node, key, value)

        try:
            await db.commit()       # 提交到資料庫
            await db.refresh(node)  # 更新對象資料（例如拿到自動產生的 ID）

        except Exception as e:
            await db.rollback()

            message = f"error: {e}"
            exception = NodeSavedFailedException(message=message)
            raise exception

        return node
    
    @staticmethod
    async def delete_node(db: AsyncSession, id: int) -> None:
        """
        Delete a conversation.
        """
        if not(node := await NodeService.get_node_by_id(db, id)):
            message = f"id: {id}"
            exception = NodeNotFoundException(message=message)
            raise exception

        try:
            await db.delete(node)
            await db.commit()

        except Exception as e:
            await db.rollback()

            message = f"error: {e}"
            exception = NodeSavedFailedException(message=message)
            raise exception

        return None

    @staticmethod
    async def get_node_by_id(db: AsyncSession, id: int) -> Node:
        """
        Get a node by ID.
        """
        sql = select(Node).where(Node.id == id)
        result = await db.execute(sql)
        node = result.scalar_one_or_none()
        return node