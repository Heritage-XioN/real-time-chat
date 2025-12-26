import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Create FastAPI app instance
app = FastAPI()

# Configure CORS (Crucial for Socket.IO!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Socket.IO with ASGI mode and CORS
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[] # Allow all origins for dev; specify list for prod
)

# Wrap FastAPI in the Socket.IO ASGI App
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# --- Define Socket Events ---

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    # You might want to authenticate the user here using headers in 'environ'

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    # Broadcast the message to everyone
    await sio.emit('message', {'sender': sid, 'content': data})

# --- Define a Standard FastAPI Route ---

@app.get("/")
async def root():
    return {"message": "FastAPI is running alongside Socket.IO"}