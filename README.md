# FastAPI Chat Application

A production-ready real-time chat application built with FastAPI, WebSockets, and SQLAlchemy with JWT authentication.

## Project Structure

```
chat_app/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── deps.py            # API dependencies (auth helpers)
│   │   └── routes/
│   │       └── auth.py        # Authentication routes
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   ├── jwt.py             # JWT token creation and verification
│   │   ├── logging_config.py  # Logging setup
│   │   └── security.py        # Password hashing utilities
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py            # SQLAlchemy base
│   │   ├── models.py          # Database models (Message)
│   │   └── session.py         # Database session management
│   ├── models/
│   │   └── user.py            # User model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication schemas
│   │   └── message.py         # Message schemas
│   ├── services/
│   │   └── message_service.py # Business logic
│   └── websocket/
│       ├── main.py            # WebSocket router
│       ├── router.py          # WebSocket event routing
│       ├── events.py          # WebSocket event types
│       ├── connection_manager.py # WebSocket connection management
│       └── handlers/
│           ├── personal.py    # Personal message handlers
│           └── group.py       # Group message handlers
├── env/                       # Virtual environment (not in repo)
├── chat.db                    # SQLite database file
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
```bash
cd chat_app
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

**Note**: The project uses the following key dependencies (see `requirements.txt`):
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server with performance optimizations
- `websockets` - WebSocket support
- `sqlalchemy` - Database ORM
- `pydantic` & `pydantic-settings` - Data validation and settings management
- `python-multipart` - Form data parsing
- `python-dotenv` - Environment variable management

**Additional dependencies** (used but may need to be added to requirements.txt):
- `python-jose[cryptography]` - JWT token handling
- `passlib[bcrypt]` - Password hashing with bcrypt backend

4. **Set up environment variables** (optional):
Create a `.env` file in the project root with the following variables (or use defaults from `app/core/config.py`):
```bash
# Application
APP_NAME=Chat Application API
APP_VERSION=1.0.0
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# Database (defaults to PostgreSQL, but SQLite is used if chat.db exists)
DATABASE_URL=postgresql+psycopg2://postgres:root@localhost:5432/chat_db

# Security (IMPORTANT: Change in production!)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["*"]
CORS_ALLOW_CREDENTIALS=True

# Logging
LOG_LEVEL=INFO
```

## Running the Application

### Development Mode

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## API Endpoints

### REST Endpoints

#### `GET /`
Welcome message and API information

#### `GET /health`
Health check endpoint

#### `POST /auth/signup`
Register a new user account
- **Request Body**: `{ "email": "user@example.com", "name": "User Name", "password": "password123" }`
- **Response**: `{ "message": "User created successfully", "access_token": "jwt_token", "email": "user@example.com" }`
- **Status Code**: 201 Created

#### `POST /auth/login`
Authenticate user and receive JWT token
- **Request Body**: `{ "email": "user@example.com", "password": "password123" }`
- **Response**: `{ "email": "user@example.com", "access_token": "jwt_token" }`
- **Status Code**: 200 OK

### WebSocket Endpoints

#### `WS /ws/chat`
Real-time chat WebSocket connection
- **Authentication**: Requires JWT token as query parameter (`?token=jwt_token`)
- **Supported Events**:
  - `SEND_PERSONAL_MESSAGE` - Send a personal message to another user
  - `SEND_GROUP_MESSAGE` - Send a message to a group
- **Event Response Types**:
  - `RECEIVE_PERSONAL_MESSAGE` - Receive a personal message
  - `RECEIVE_GROUP_MESSAGE` - Receive a group message
  - `PERSONAL_MESSAGE_DELIVERED` - Confirmation of message delivery
  - `GROUP_CREATED` - Notification of group creation
  - `ERROR` - Error notification

## Features

- **JWT Authentication**: Secure token-based authentication
- **Real-time Messaging**: WebSocket support for instant messaging
- **Personal Messages**: One-on-one chat functionality
- **Group Messages**: Group chat support
- **Password Security**: Bcrypt password hashing
- **CORS Support**: Configurable CORS middleware
- **Database**: SQLAlchemy ORM with support for SQLite and PostgreSQL
- **Logging**: Structured logging configuration
