import httpx
from sqlalchemy.orm import Session
from app.models.log import ChatLog
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.config import settings

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

async def get_chat_response(db: Session, user_id: int, chat_request: ChatRequest) -> ChatResponse:
    db.add(ChatLog(user_id=user_id, role="user", message=chat_request.message))
    db.commit()

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": chat_request.message}]
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(OPENAI_API_URL, json=payload, headers=headers)
            print("DEBUG: Status code:", response.status_code)
            print("DEBUG: Response JSON:", response.text)
            response.raise_for_status()
            assistant_msg = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("DEBUG: Exception from OpenAI:", e)
        assistant_msg = "Maaf, terjadi kesalahan saat menghubungi AI."

    db.add(ChatLog(user_id=user_id, role="assistant", message=assistant_msg))
    db.commit()
    return ChatResponse(response=assistant_msg)

def get_user_chat_logs(db: Session, user_id: int, limit: int = 100):
    return db.query(ChatLog).filter(ChatLog.user_id == user_id)\
        .order_by(ChatLog.timestamp.desc()).limit(limit).all()

def get_all_chat_logs(db: Session, limit: int = 100):
    return db.query(ChatLog).order_by(ChatLog.timestamp.desc()).limit(limit).all()
