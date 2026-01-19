from socketio import AsyncServer
import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import Chat, Message

logger = logging.getLogger(__name__)


def register(sio: AsyncServer):
    @sio.event
    async def send_message(sid, data):
        db: Session = SessionLocal()
        logger.info(f"Message from {sid}: {data}")
        try:
            chat_id = data.get("chat_id")
            sender_id = data.get("sender_id")
            receiver_id = data.get("receiver_id")
            content = data.get("content")

            if chat_id:
                chat = db.query(Chat).filter(Chat.id == chat_id).first()

            if not chat:
                chat = Chat(id=chat_id, is_group=bool(receiver_id is None))
                db.add(chat)
                db.commit()
                db.refresh(chat)
            message = Message(
                chat_id=chat.id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=content,
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            payload = {
                "id": message.id,
                "chat_id": chat.id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "content": content,
                "created_at": message.created_at.isoformat(),
            }
            await sio.emit("new_message", payload, room=f"user:{receiver_id}")
            await sio.emit("new_message", payload, room=f"user:{sender_id}")
        except Exception as e:
            logger.exception(f"send_message failed {str(e)}")

    @sio.event
    async def typing(sid, data):
        user_id = data.get("user_id")
        is_typing = data.get("is_typing", False)
        to_user_id = data.get("to_user_id")
        logger.info(f"User {user_id} typing status: {is_typing}")
        if to_user_id is None:
            await sio.emit(
                "typing_status",
                {"user_id": user_id, "is_typing": is_typing},
                skip_sid=sid,
            )
        else:
            await sio.emit(
                "typing_status",
                {"user_id": user_id, "is_typing": is_typing},
                room=f"user:{to_user_id}",
            )


    @sio.event
    async def call_request(sid, data):
        await sio.emit("incoming_call", data, room=f"user:{data['receiver_id']}")

    @sio.event
    async def call_response(sid, data):
        await sio.emit("call_response", data, room=f"user:{data['caller_id']}")

    @sio.event
    async def webrtc_offer(sid, data):
        print("webrtc_offer", data)
        await sio.emit("webrtc_offer", data, room=f"user:{data['to_user_id']}")

    @sio.event
    async def webrtc_answer(sid, data):
        await sio.emit("webrtc_answer", data, room=f"user:{data['to_user_id']}")

    @sio.event
    async def ice_candidate(sid, data):
        await sio.emit("ice_candidate", data, room=f"user:{data['to_user_id']}")

    @sio.event
    async def call_end(sid, data):
        await sio.emit("call_end", data, room=f"user:{data['to_user_id']}")