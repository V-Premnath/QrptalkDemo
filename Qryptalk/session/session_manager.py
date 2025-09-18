from .conversation import ConversationSession

class SessionManager:
    """
    Manages all active conversation sessions.
    """
    def __init__(self):
        self.sessions = {}

    def create_session(self, contact_id, security_level):
        session = ConversationSession(contact_id, security_level)
        self.sessions[contact_id] = session
        return session

    def get_session(self, contact_id):
        return self.sessions.get(contact_id)

    def cleanup_expired_sessions(self):
        # Implement session expiration and cleanup logic
        pass
