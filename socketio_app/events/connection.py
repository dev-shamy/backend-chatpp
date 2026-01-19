import logging
from app.core.jwt import verify_jwt_token
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def register(sio):
    @sio.event
    async def connect(sid, environ, auth):
        db = SessionLocal()
        try:
            if auth and "token" in auth:
                token = auth["token"]

            if not token:
                logger.warning("Socket rejected: missing token for websocket")
                return False

            user = verify_jwt_token(token, db)
            if not user or not getattr(user, "id", None):
                logger.warning("Socket rejected: invalid token or user not found")
                return False

            user_id = user.id
            await sio.enter_room(sid,f"user:{user_id}")

            await sio.emit(
                "user_status", {"user_id": user_id, "online": True}, skip_sid=sid
            )
            logger.info(f"Socket connected sid={sid}, user_id={user_id}")
            return True

        except Exception as e:
            logger.exception(f"Socket connection rejected: {e}")
            return False

    @sio.event
    async def disconnect(sid):
        rooms = sio.rooms(sid)
        for room in rooms:
            if room.startswith("user:"):
                user_id = int(room.split(":")[1])
                room_members = sio.manager.rooms.get("/", {}).get(room, set())

                if not room_members:
                    await sio.emit(
                        "user_status",
                        {"user_id": user_id, "online": False}
                    )
                break

    @sio.event
    async def get_online_users(sid):
        namespace_rooms = sio.manager.rooms.get("/", {})

        online_users = {
            int(room.split(":")[1]): list(sids)
            for room, sids in namespace_rooms.items()
            if isinstance(room, str) and room.startswith("user:")
        }

        await sio.emit("online_users", online_users, to=sid)
