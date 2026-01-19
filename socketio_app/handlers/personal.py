"""Personal message event handlers"""
from socketio_app.connection_manager import SocketIOManager
from socketio_app.events.connection import socketio_event


async def handle_send_personal(
    payload: dict,
    sender_id: int,
    socket_id: str,
    manager: SocketIOManager,
    db
):
    """Handle sending a personal message"""
    receiver_id = payload.get("to_user_id")
    content = payload.get("content")

    if not receiver_id or not content:
        await manager.sio.emit(
            socketio_event.ERROR,
            {"message": "Missing required fields: to_user_id and content"},
            room=socket_id
        )
        return
    
    # Send message to receiver
    await manager.send_to_user(
        receiver_id,
        socketio_event.RECEIVE_PERSONAL_MESSAGE,
        {
            "from_user_id": sender_id,
            "content": content,
            "timestamp": None  # Add timestamp from DB
        }
    )
    
    # Send delivery confirmation to sender
    await manager.sio.emit(
        socketio_event.PERSONAL_MESSAGE_DELIVERED,
        {
            "to_user_id": receiver_id,
            "message": "Message delivered"
        },
        room=socket_id
    )
