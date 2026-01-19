from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.user import Message
from app.schemas.user import UserResponse
from app.schemas.message import MessageResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all-user", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    return db.query(User).filter(User.id != user_id).all()


@router.get("get-user/{user_id}/messages", response_model=list[MessageResponse])
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    messages = (
        db.query(Message)
        .filter((Message.sender_id == user_id) | (Message.receiver_id == user_id))
        .order_by(Message.created_at.desc())
        .all()
    )
    return messages
