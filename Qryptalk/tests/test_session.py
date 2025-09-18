import unittest
from Qryptalk.session.conversation import ConversationSession
from Qryptalk.session.session_manager import SessionManager

class TestConversationSession(unittest.TestCase):
    def test_add_message(self):
        session = ConversationSession("contact1", "KYBER_768")
        session.add_message("Hello")
        self.assertIn("Hello", session.message_history)

class TestSessionManager(unittest.TestCase):
    def test_create_and_get_session(self):
        manager = SessionManager()
        session = manager.create_session("contact1", "KYBER_768")
        self.assertEqual(manager.get_session("contact1"), session)

    def test_cleanup_expired_sessions(self):
        manager = SessionManager()
        # Implement test for cleanup if logic added
        self.assertTrue(True)  # Placeholder

if __name__ == "__main__":
    unittest.main()
