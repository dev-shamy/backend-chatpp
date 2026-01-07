from datetime import datetime
from app.schemas.message import PersonalMessage


class MessageService:
    async def create_message(self, data: dict) -> PersonalMessage:
        return PersonalMessage(
            sender_id=data["sender_id"],
            receiver_id=data["receiver_id"],
            content=data["content"],
            timestamp=datetime.utcnow(),
        )
