import unittest
from Qryptalk.network.protocol import MessageProtocol
from Qryptalk.network.client import NetworkClient

class TestMessageProtocol(unittest.TestCase):
    def test_serialize_deserialize(self):
        protocol = MessageProtocol()
        message = {"type": "test", "content": "hello"}
        serialized = protocol.serialize_message(message)
        deserialized = protocol.deserialize_message(serialized)
        self.assertEqual(message, deserialized)

class TestNetworkClient(unittest.TestCase):
    def test_register_user(self):
        client = NetworkClient()
        # Add mock or patch if needed
        self.assertIsNone(client.register_user("user1", b"public_key"))

    def test_send_message(self):
        client = NetworkClient()
        self.assertIsNone(client.send_message({"content": "hello"}))

    def test_fetch_pending_messages(self):
        client = NetworkClient()
        self.assertIsNone(client.fetch_pending_messages())

if __name__ == "__main__":
    unittest.main()
