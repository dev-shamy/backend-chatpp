
# from app.websocket.connection_manager import manager
# from app.websocket.events import ws_event


# async def handle_send_personal(payload: dict, sender, db):
#     receiver_id = payload["to_user_id"]
#     content = payload["content"]

#     # TODO: save message to DB here

#     await manager.send_to_user(
#         receiver_id,
#         {
#             "event": ws_event.RECEIVE_PERSONAL_MESSAGE,
#             "payload": {
#                 "from_user_id": sender.id,
#                 "content": content
#             }
#         }
#     )
