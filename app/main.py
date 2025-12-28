from contextlib import asynccontextmanager

import socketio  # pyright: ignore[reportMissingTypeStubs]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import auth_controller, messages_controller
from app.controllers.socket_controller import register_socket_events
from app.core.database import Base, engine
from app.models import messages, private_chat_rooms, users  # noqa: F401


# handles creating database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- initiate engine ---
    async with engine.begin() as conn:
        # create database table
        await conn.run_sync(Base.metadata.create_all)
    yield
    # --- Dispose engine ---
    await engine.dispose()


# Create FastAPI app instance
app = FastAPI(lifespan=lifespan)

# Include API router
app.include_router(messages_controller.router)
app.include_router(auth_controller.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Socket.IO with ASGI mode and CORS
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[],  # Allow all origins for dev; specify list for prod
)

# Wrap FastAPI in the Socket.IO ASGI App
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# --- Define Socket Events ---
register_socket_events(sio)


# --- Define a Standard FastAPI Route ---
@app.get("/")
async def root():
    return {"message": "FastAPI is running alongside Socket.IO"}
