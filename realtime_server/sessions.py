import uuid


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, sid):
        session_id = str(uuid.uuid4())
        self.sessions[sid] = session_id
        return session_id

    def get_session(self, sid):
        return self.sessions.get(sid)

    def remove_session(self, sid):
        self.sessions.pop(sid, None)
