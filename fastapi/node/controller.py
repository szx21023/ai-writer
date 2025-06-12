from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import NodeService

router = APIRouter(prefix=f"/node", tags=["node"])

@router.get("")
async def get_node(
        db: AsyncSession = Depends(get_db)
    ):
    """
    get node api
    """

    result = await NodeService.get_node(db)
    return result

@router.post("")
async def create_node( 
        schema = Body(example={
            'conversation_id': 1,
            'prompt': 'it should be a story',
            'content': 'this is a content',
            'order': 1,
            'last_node_id': None,
            'next_node_id': None
        }),
        db: AsyncSession = Depends(get_db)
    ):
    """
    post node api
    """

    result = await NodeService.create_node(db, **schema)
    return result

@router.patch("/{node_id}")
async def update_node(
        node_id: int,
        schema = Body(example={
            'conversation_id': 1,
            'prompt': 'it should be a story',
            'content': 'this is a content',
            'order': 1
        }),
        db: AsyncSession = Depends(get_db)
    ):
    """
    patch node api
    """

    conversation_id = schema.get('conversation_id')
    prompt = schema.get('prompt')
    content = schema.get('content')
    order = schema.get('order')
    result = await NodeService.update_node(db, id=node_id, conversation_id=conversation_id, prompt=prompt, content=content, order=order)
    return result

@router.delete("/{node_id}")
async def delete_node(
        node_id: int,
        db: AsyncSession = Depends(get_db)
    ):

    """
    delete node api
    """
    result = await NodeService.delete_node(db, id=node_id)
    return result