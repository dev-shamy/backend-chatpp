# Socket.IO Application

This is a Socket.IO-based real-time chat application module that can run standalone or be integrated with the main FastAPI application.

## Structure

```
socketio_app/
├── __init__.py
├── main.py                 # Socket.IO server setup and event handlers
├── server.py              # Standalone server entry point
├── connection_manager.py   # Connection and room management
├── events.py              # Event type definitions
├── middleware.py          # Authentication middleware
├── handlers/
│   ├── __init__.py
│   ├── personal.py        # Personal message handlers
│   └── group.py           # Group message handlers
└── README.md              # This file
```

## Features

- **JWT Authentication**: Secure token-based authentication for Socket.IO connections
- **Personal Messaging**: One-on-one real-time messaging
- **Group Messaging**: Room-based group chat functionality
- **Typing Indicators**: Real-time typing status notifications
- **Room Management**: Join/leave room functionality
- **Connection Management**: Multi-connection support per user

## Installation

Add `python-socketio` and `python-socketio[asyncio]` to your requirements:

```bash
pip install python-socketio[asyncio]
```

## Usage

### Standalone Server

Run the Socket.IO server independently:

```bash
python -m socketio_app.server
```

The server will run on port 8001 (configurable).

### Integration with FastAPI

To integrate Socket.IO with your existing FastAPI app:

```python
from fastapi import FastAPI
from socketio_app.main import create_socketio_app

app = FastAPI()

# Mount Socket.IO on FastAPI app
socketio_app = create_socketio_app(app)

# Use socketio_app as your ASGI application
```

## Client Connection

### JavaScript/TypeScript Example

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:8001', {
  auth: {
    token: 'your_jwt_token_here'
  }
});

// Listen for connection
socket.on('connected', (data) => {
  console.log('Connected:', data);
});

// Send personal message
socket.emit('send_personal_message', {
  to_user_id: 123,
  content: 'Hello!'
});

// Receive personal message
socket.on('receive_personal_message', (data) => {
  console.log('Message received:', data);
});

// Join a room
socket.emit('join_room', {
  room_id: 'room_123'
});

// Send group message
socket.emit('send_group_message', {
  room_id: 'room_123',
  content: 'Hello group!'
});

// Typing indicators
socket.emit('typing_start', {
  to_user_id: 123  // or room_id for group
});

socket.emit('typing_stop', {
  to_user_id: 123
});
```

## Event Types

### Client to Server Events

- `send_personal_message` - Send a personal message
- `send_group_message` - Send a group message
- `join_room` - Join a room/group
- `leave_room` - Leave a room/group
- `typing_start` - Start typing indicator
- `typing_stop` - Stop typing indicator

### Server to Client Events

- `connected` - Connection confirmed
- `receive_personal_message` - Receive a personal message
- `receive_group_message` - Receive a group message
- `personal_message_delivered` - Personal message delivery confirmation
- `group_message_delivered` - Group message delivery confirmation
- `user_joined` - User joined a room
- `user_left` - User left a room
- `typing` - Typing indicator update
- `error` - Error notification

## Authentication

Socket.IO connections require JWT authentication. Pass the token in the connection auth:

```javascript
const socket = io('http://localhost:8001', {
  auth: {
    token: 'your_jwt_token'
  }
});
```

The token is verified using the same JWT verification logic as the REST API.

## Configuration

The Socket.IO server uses the same configuration as the main FastAPI app (`app/core/config.py`). When running standalone, it uses port `PORT + 1` (default: 8001).
