from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatLog
from app.services.auth_service import get_current_active_user
from app.services.chat_service import get_chat_response, get_user_chat_logs
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return await get_chat_response(db, current_user.id, chat_request)

@router.get("/logs", response_model=list[ChatLog])
def get_chat_logs(
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_user_chat_logs(db, current_user.id, limit)

@router.get("/me")
def get_me(current_user: User = Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin
    }