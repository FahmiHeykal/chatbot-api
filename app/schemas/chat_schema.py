from datetime import datetime
from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str 

class ChatResponse(BaseModel):
    response: str

class ChatLog(BaseModel):
    id: int
    user_id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True

class SummaryLog(BaseModel):
    id: int
    user_id: int
    summary_type: str
    content: str
    start_date: datetime
    end_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
