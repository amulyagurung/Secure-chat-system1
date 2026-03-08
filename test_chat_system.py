"""
Unit Tests for Chat System
"""

import pytest
from encryption import EncryptionManager
from user import User, Message
from chat_system import ChatSystem


class TestEncryption:
    def test_encrypt_decrypt(self):
        em = EncryptionManager()
        original = "Hello"
        encrypted = em.encrypt_message(original)
        decrypted = em.decrypt_message(encrypted)
        assert decrypted == original


class TestUser:
    def test_creation(self):
        user = User("alice", "password123")
        assert user.get_username() == "alice"
    
    def test_authenticate_valid(self):
        user = User("alice", "password123")
        assert user.authenticate("password123") is True
    
    def test_authenticate_invalid(self):
        user = User("alice", "password123")
        assert user.authenticate("wrongpassword") is False


class TestChatSystem:
    def test_register_user(self):
        cs = ChatSystem()
        assert cs.register_user("alice", "pwd") is True
    
    def test_register_duplicate(self):
        cs = ChatSystem()
        cs.register_user("alice", "pwd")
        assert cs.register_user("alice", "pwd") is False
    
    def test_login_valid(self):
        cs = ChatSystem()
        cs.register_user("alice", "pwd")
        user = cs.login_user("alice", "pwd")
        assert user is not None
    
    def test_login_invalid(self):
        cs = ChatSystem()
        cs.register_user("alice", "pwd")
        user = cs.login_user("alice", "wrong")
        assert user is None
    
    def test_send_message(self):
        cs = ChatSystem()
        cs.register_user("alice", "pwd")
        cs.register_user("bob", "pwd")
        assert cs.send_message("alice", "bob", "Hello") is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
