from pydantic import BaseModel
from datetime import datetime


class PersonalMessage(BaseModel):
    sender_id: str
    receiver_id: str
    content: str
    timestamp: datetime
