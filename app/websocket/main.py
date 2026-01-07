from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from app.websocket.connection_manager import manager
from app.core.jwt import verify_jwt_token
from app.db.session import SessionLocal
from app.websocket.router import route_event

router = APIRouter()

@router.websocket("/ws/chat")
async def personal_chat(websocket: WebSocket):
    db = SessionLocal()
    try:
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        user = verify_jwt_token(token, db)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await manager.connect(user.id, websocket)

        while True:
            data = await websocket.receive_json()
            await route_event(data, user, websocket, db)

    except WebSocketDisconnect:
        manager.disconnect(user.id)
        print(f"Client disconnected: user_id={user.id}")

    finally:
        db.close()

