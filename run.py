from realtime_server.socket_app import create_app

app, socketio = create_app()

if __name__ == "__main__":
    print("✅ Flask-SocketIO server running on port 8000")
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
