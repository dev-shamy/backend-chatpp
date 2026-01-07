
from app.websocket.events import ws_event
from app.websocket.handlers.personal import handle_send_personal
from app.websocket.handlers.group import handle_send_group

async def route_event(event: dict, user, websocket, db):
    event_type = event.get("event")
    payload = event.get("payload", {})

    if event_type == ws_event.SEND_PERSONAL_MESSAGE:
        await handle_send_personal(payload, user, db)

    elif event_type == ws_event.SEND_GROUP_MESSAGE:
        await handle_send_group(payload, user, db)

    else:
        await websocket.send_json({
            "event": ws_event.ERROR,
            "message": "Unknown event type"
        })
