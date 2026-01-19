"""Socket.IO Main Application"""

import socketio
from socketio_app.events import connection, chat
import logging

logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[
        "http://localhost:5173",  # EXACT frontend origin
    ],
    allow_credentials=True,
)
#wrap with ASGI application
# socket_app = socketio.ASGIApp(sio)


def register_socket_events(sio):
    connection.register(sio)
    chat.register(sio)
    logger.info("Socket.IO events registered.")
