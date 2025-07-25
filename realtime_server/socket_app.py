from flask import Flask
from flask_socketio import SocketIO
from .sessions import SessionManager
from . import config as app_config
from .events import register_socket_events


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config.Config)

    socketio = SocketIO(app, cors_allowed_origins="*")
    session_mgr = SessionManager()

    register_socket_events(socketio, session_mgr, app.config)

    return app, socketio
