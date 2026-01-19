"""Socket.IO Authentication Middleware"""
from typing import Optional
from socketio import AsyncServer
from app.core.jwt import verify_jwt_token
from app.db.session import SessionLocal


async def authenticate_socket(sio: AsyncServer, sid: str, auth: dict) -> Optional[int]:
    token = auth.get("token")
    if not token:
        return None
    
    db = SessionLocal()
    try:
        user = verify_jwt_token(token, db)
        if user:
            return user.id
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None
    finally:
        db.close()
