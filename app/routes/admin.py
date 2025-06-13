from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat_schema import ChatLog, SummaryLog
from app.services.auth_service import get_admin_user
from app.services.chat_service import get_all_chat_logs
from app.services.summary_service import get_user_summaries, generate_summary
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/logs", response_model=list[ChatLog])
def get_all_chat_logs_admin(
    limit: int = 100,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    return get_all_chat_logs(db, limit)

@router.get("/summaries/{user_id}", response_model=list[SummaryLog])
def get_user_summaries_admin(
    user_id: int,
    summary_type: str | None = None,
    limit: int = 10,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    if summary_type and summary_type not in ("daily", "weekly"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid summary_type")
    return get_user_summaries(db, user_id, summary_type, limit)

@router.post("/summaries/{user_id}/{summary_type}", response_model=SummaryLog)
def generate_summary_admin(
    user_id: int,
    summary_type: str,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    if summary_type not in ("daily", "weekly"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid summary_type")
    summary = generate_summary(db, user_id, summary_type)
    if not summary:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No chat logs to summarize")
    return summary
