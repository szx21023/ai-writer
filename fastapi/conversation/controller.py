from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import ConversationService

router = APIRouter(prefix=f"/conversation", tags=["conversation"])

@router.get("")
async def get_conversation(
        db: AsyncSession = Depends(get_db)
    ):
    """
    get customer api
    """

    result = await ConversationService.get_conversation(db)
    return result

@router.post("")
async def create_conversation( 
        schema = Body(example={
            'title': 'Sample Conversation',
        }),
        db: AsyncSession = Depends(get_db)
    ):
    """
    post customer api
    """

    title = schema.get('title')
    result = await ConversationService.create_conversation(db, title=title)
    return result

@router.patch("/{conversation_id}")
async def update_conversation(
        conversation_id: int,
        schema = Body(example={
            'title': 'Updated Conversation',
        }),
        db: AsyncSession = Depends(get_db)
    ):
    """
    patch customer api
    """

    title = schema.get('title')
    result = await ConversationService.update_conversation(db, id=conversation_id, title=title)
    return result

@router.delete("/{conversation_id}")
async def delete_conversation(
        conversation_id: int,
        db: AsyncSession = Depends(get_db)
    ):

    """
    delete customer api
    """
    result = await ConversationService.delete_conversation(db, id=conversation_id)
    return result