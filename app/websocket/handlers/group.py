
from app.websocket.connection_manager import manager
from app.websocket.events import ws_event

async def handle_send_group(payload: dict, sender, db):
    room_id = payload["room_id"]
    content = payload["content"]

    # TODO: validate membership & save message

    await manager.send_to_room(
        room_id,
        {
            "event": ws_event.RECEIVE_GROUP_MESSAGE,
            "payload": {
                "room_id": room_id,
                "from_user_id": sender.id,
                "content": content
            }
        }
    )
