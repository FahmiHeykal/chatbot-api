import openai
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.log import ChatLog, SummaryLog
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_summary(db: Session, user_id: int, summary_type: str) -> SummaryLog | None:
    end = datetime.utcnow()
    start = end - timedelta(days=1 if summary_type == "daily" else 7)

    logs = db.query(ChatLog).filter(
        ChatLog.user_id == user_id,
        ChatLog.timestamp >= start,
        ChatLog.timestamp <= end
    ).order_by(ChatLog.timestamp).all()

    if not logs:
        return None

    convo = "\n".join(f"{l.role}: {l.message}" for l in logs)
    prompt = f"Ringkas percakapan berikut dalam 3-5 poin:\n\n{convo}"

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful summarizer."},
                {"role": "user", "content": prompt}
            ]
        )
        summary_text = resp.choices[0].message.content
    except Exception:
        summary_text = "Tidak dapat menghasilkan ringkasan saat ini."

    db.add(SummaryLog(user_id=user_id, summary_type=summary_type,
                      content=summary_text, start_date=start, end_date=end))
    db.commit()
    return db.query(SummaryLog).order_by(SummaryLog.created_at.desc()).first()

def get_user_summaries(db: Session, user_id: int, summary_type: str | None, limit: int = 10):
    q = db.query(SummaryLog).filter(SummaryLog.user_id == user_id)
    if summary_type:
        q = q.filter(SummaryLog.summary_type == summary_type)
    return q.order_by(SummaryLog.created_at.desc()).limit(limit).all()
