from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    receiver_id: int | None
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

