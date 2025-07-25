from flask import request
from flask_socketio import SocketIO, emit
import requests


def register_socket_events(socketio: SocketIO, session_mgr, config):
    @socketio.on("connect")
    def on_connect():
        sid = request.sid
        session_id = session_mgr.create_session(sid)
        print(f"Connected: {sid} → Session: {session_id}")

    @socketio.on("disconnect")
    def on_disconnect():
        sid = request.sid
        print(f"Disconnected: {sid}")
        session_mgr.remove_session(sid)

    @socketio.on("message")
    def on_message(data):
        sid = request.sid
        session_id = session_mgr.get_session(sid)
        user_input = data.get("text")

        if not user_input:
            emit(
                "response",
                {"status": "error", "message": "Missing 'text' field"},
                room=sid,
            )
            return

        try:
            webhook_url = config.get("WEBHOOK_URL")
            response = requests.post(
                webhook_url,
                json={"message": user_input, "session_id": session_id},
            )
            response.raise_for_status()
            n8n_data = response.json()

            emit(
                "response",
                {
                    "status": "ok",
                    "session_id": session_id,
                    "reply": n8n_data.get("reply", "No reply field in response"),
                    "raw": n8n_data,
                },
                room=sid,
            )

        except Exception as e:
            emit(
                "response",
                {"status": "error", "message": f"Error contacting n8n: {str(e)}"},
                room=sid,
            )
