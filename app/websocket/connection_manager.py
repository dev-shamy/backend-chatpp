
from collections import defaultdict
from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.user_connections: Dict[int, Set[WebSocket]] = defaultdict(set)
        self.room_users: Dict[int, Set[int]] = defaultdict(set)

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        print("client connected with user id:", user_id)
        self.user_connections[user_id].add(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.user_connections[user_id].discard(websocket)
        if not self.user_connections[user_id]:
            del self.user_connections[user_id]
        print("client disconnected with user id:", user_id)

    async def send_to_user(self, user_id: int, message: dict):

        for ws in self.user_connections.get(user_id, []):
            await ws.send_json(message)

    async def send_to_room(self, room_id: int, message: dict):
        for user_id in self.room_users.get(room_id, []):
            await self.send_to_user(user_id, message)


manager = ConnectionManager()
