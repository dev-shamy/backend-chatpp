"""Group message event handlers"""
from socketio_app.connection_manager import SocketIOManager
from socketio_app.events.connection import socketio_event


async def handle_send_group(
    payload: dict,
    sender_id: int,
    socket_id: str,
    manager: SocketIOManager,
    db
):
    """Handle sending a group message"""
    room_id = payload.get("room_id")
    content = payload.get("content")
    
    if not room_id or not content:
        await manager.sio.emit(
            socketio_event.ERROR,
            {"message": "Missing required fields: room_id and content"},
            room=socket_id
        )
        return
    
    # TODO: Validate user membership in room
    # TODO: Save message to database
    
    # Send message to all users in the room (except sender)
    await manager.send_to_room(
        room_id,
        socketio_event.RECEIVE_GROUP_MESSAGE,
        {
            "room_id": room_id,
            "from_user_id": sender_id,
            "content": content,
            "timestamp": None  # Add timestamp from DB
        },
        exclude_socket=socket_id
    )
    
    # Send delivery confirmation to sender
    await manager.sio.emit(
        socketio_event.GROUP_MESSAGE_DELIVERED,
        {
            "room_id": room_id,
            "message": "Message sent to group"
        },
        room=socket_id
    )


async def handle_join_room(
    payload: dict,
    user_id: int,
    socket_id: str,
    manager: SocketIOManager,
    db
):
    """Handle user joining a room"""
    room_id = payload.get("room_id")
    
    if not room_id:
        await manager.sio.emit(
            socketio_event.ERROR,
            {"message": "Missing required field: room_id"},
            room=socket_id
        )
        return
    
    # TODO: Validate user has permission to join room
    
    await manager.join_room(user_id, room_id, socket_id)
    
    # Notify others in the room
    await manager.send_to_room(
        room_id,
        socketio_event.USER_JOINED,
        {
            "room_id": room_id,
            "user_id": user_id
        },
        exclude_socket=socket_id
    )


async def handle_leave_room(
    payload: dict,
    user_id: int,
    socket_id: str,
    manager: SocketIOManager,
    db
):
    """Handle user leaving a room"""
    room_id = payload.get("room_id")
    
    if not room_id:
        await manager.sio.emit(
            socketio_event.ERROR,
            {"message": "Missing required field: room_id"},
            room=socket_id
        )
        return
    
    await manager.leave_room(user_id, room_id, socket_id)
    
    # Notify others in the room
    await manager.send_to_room(
        room_id,
        socketio_event.USER_LEFT,
        {
            "room_id": room_id,
            "user_id": user_id
        },
        exclude_socket=socket_id
    )
