import socketio

# A mock function to simulate verifying a JWT
# in your real app, you would import your existing `verify_token` function here
async def get_current_user(token: str):
    if token == "user_123_secret_token":
        return {"id": 1, "username": "Xheri"}
    return None


# This function will register all events
def register_socket_events(sio: socketio.AsyncServer):
    
    @sio.event
    async def connect(sid, environ, auth):
        print(f"Client connected: {sid}")
        # In the future, we will check auth tokens here

        # 1. Extract the token
        # 'auth' might be None if the client didn't send anything
        token = auth.get("token") if auth else None

        # 2. Validate the token
        user = await get_current_user(token)
        
        if not user:
            print(f"Refusing connection: Invalid token for {sid}")
            raise socketio.exceptions.ConnectionRefusedError("Invalid token")

        # 3. Save User to Session
        # This attaches the user object to this specific socket ID safely
        print(f"User authenticated: {user['username']}")
        await sio.save_session(sid, {"user": user})
    
    @sio.event
    async def disconnect(sid):
        print(f"Client disconnected: {sid}")


    # --- ROOM LOGIC ---
    @sio.event
    async def join_room(sid, room_name):
        """Allows a user to join a specific chat room"""
        print(f"User {sid} joined room: {room_name}")
        await sio.enter_room(sid, room_name)
        # Notify others in the room
        await sio.emit('system_message', {'content': f'User joined {room_name}'}, room=room_name)

    @sio.event
    async def leave_room(sid, room_name):
        """Allows a user to leave a room"""
        print(f"User {sid} left room: {room_name}")
        sio.leave_room(sid, room_name)
        await sio.emit('system_message', {'content': f'User left {room_name}'}, room=room_name)

    @sio.event
    async def send_message(sid, data):
        """
        Expects data to be: 
        {
            "room": "room_name",
            "message": "Hello World"
        }
        """
        room = data.get("room")
        content = data.get("message")
        
        print(f"Sending to {room}: {content}")

        # 4. Retrieve User from Session
        # We don't trust the client to tell us who they are. We look up our session.
        session = await sio.get_session(sid)
        user = session['user'] # We are guaranteed this exists because of the connect check
        
        print(f"User {user['username']} sent: {content}")
        
        # Broadcast ONLY to that specific room
        # skip_sid=sid ensures the sender doesn't get their own message back immediately
        # (useful if you optimistically update UI)
        await sio.emit('new_message', {
            #'sender': sid,
            'sender': user['username'], # Now we send the REAL username, not the random SID
            'content': content
        }, room=room, skip_sid=sid)