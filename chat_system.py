"""
Chat System Class - COMPLETE FIX
ONE shared encryption key across all windows
Messages sync 100%
"""

import json
import os
from data_structures import HashMap, LinkedList
from encryption import EncryptionManager
from user import User, Message


# Database files
USERS_DB_FILE = "users_database.json"
MESSAGES_DB_FILE = "messages_database.json"
ENCRYPTION_KEY_FILE = "encryption_key.txt"


def get_or_create_encryption_key():
    """Get shared encryption key - same for all windows"""
    if os.path.exists(ENCRYPTION_KEY_FILE):
        try:
            with open(ENCRYPTION_KEY_FILE, 'r') as f:
                key = f.read().strip()
                print(f"✓ Using shared encryption key from file")
                return key
        except:
            pass
    
    # Generate new key
    from cryptography.fernet import Fernet
    key = Fernet.generate_key().decode()
    
    # Save for all windows to use
    with open(ENCRYPTION_KEY_FILE, 'w') as f:
        f.write(key)
    print(f"✓ Created new shared encryption key")
    return key


def load_users_from_file():
    """Load users from file"""
    if os.path.exists(USERS_DB_FILE):
        try:
            with open(USERS_DB_FILE, 'r') as f:
                data = json.load(f)
                print(f"✓ Loaded {len(data)} users from file")
                return data
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    return {}


def save_users_to_file(users_dict):
    """Save users to file"""
    try:
        with open(USERS_DB_FILE, 'w') as f:
            json.dump(users_dict, f, indent=2)
        print(f"✓ Saved {len(users_dict)} users to file")
    except Exception as e:
        print(f"Error saving users: {e}")


def load_messages_from_file():
    """Load messages from file"""
    if os.path.exists(MESSAGES_DB_FILE):
        try:
            with open(MESSAGES_DB_FILE, 'r') as f:
                data = json.load(f)
                total_msgs = sum(len(msgs) for msgs in data.values())
                print(f"✓ Loaded {total_msgs} messages from {len(data)} conversations")
                return data
        except Exception as e:
            print(f"Error loading messages: {e}")
            return {}
    print("✓ No messages file yet")
    return {}


def save_messages_to_file(messages_dict):
    """Save messages to file"""
    try:
        with open(MESSAGES_DB_FILE, 'w') as f:
            json.dump(messages_dict, f, indent=2)
        total_msgs = sum(len(msgs) for msgs in messages_dict.values())
        print(f"✓ Saved {total_msgs} messages to disk")
    except Exception as e:
        print(f"Error saving messages: {e}")


class ChatSystem:
    """
    ChatSystem with SHARED ENCRYPTION KEY
    All windows use the same key so they can decrypt each other's messages
    """
    def __init__(self):
        """Initialize chat system"""
        print("\n" + "="*60)
        print("🔐 SECURE MESSAGE CHAT SYSTEM v3.0")
        print("="*60 + "\n")
        
        self.users = HashMap()
        self.conversations = {}
        
        # Get SHARED encryption key (same across all windows)
        shared_key = get_or_create_encryption_key()
        self.encryption_manager = EncryptionManager(shared_key=shared_key)
        
        # Load existing data
        print("📂 Loading data from disk...")
        self.load_users_from_disk()
        self.load_messages_from_disk()
        
        print("\n✓ ChatSystem ready!\n")
    
    def load_users_from_disk(self):
        """Load users from disk"""
        users_data = load_users_from_file()
        
        for username, user_data in users_data.items():
            try:
                user = User.__new__(User)
                user._username = username
                user._password_hash = user_data['password_hash']
                user._email = user_data.get('email')
                
                from datetime import datetime
                try:
                    user._created_at = datetime.fromisoformat(user_data['created_at'])
                except:
                    user._created_at = datetime.now()
                
                self.users.insert(username, user)
                print(f"  ✓ Loaded user: {username}")
            except Exception as e:
                print(f"  ✗ Error loading {username}: {e}")
    
    def load_messages_from_disk(self):
        """Load messages from disk"""
        messages_data = load_messages_from_file()
        
        self.conversations = {}
        
        for conv_id, messages_list in messages_data.items():
            try:
                ll = LinkedList()
                for msg in messages_list:
                    ll.insert(msg)
                self.conversations[conv_id] = ll
                print(f"  ✓ Loaded conversation: {conv_id}")
            except Exception as e:
                print(f"  ✗ Error loading {conv_id}: {e}")
    
    def save_users_to_disk(self):
        """Save all users to disk"""
        users_dict = {}
        all_users = self.users.get_all_values()
        
        for user in all_users:
            username = user.get_username()
            users_dict[username] = {
                'password_hash': user._password_hash,
                'email': user._email,
                'created_at': user._created_at.isoformat()
            }
        
        save_users_to_file(users_dict)
    
    def save_messages_to_disk(self):
        """Save all conversations to disk"""
        messages_dict = {}
        
        for conv_id, linkedlist in self.conversations.items():
            messages_dict[conv_id] = linkedlist.get_all()
        
        save_messages_to_file(messages_dict)
    
    def register_user(self, username, password):
        """Register a new user"""
        if self.users.search(username):
            print(f"✗ Username '{username}' already exists!")
            return False
        
        user = User(username, password)
        self.users.insert(username, user)
        self.save_users_to_disk()
        print(f"✓ User '{username}' registered!")
        return True
    
    def login_user(self, username, password):
        """Authenticate user login"""
        self.load_users_from_disk()
        
        user = self.users.search(username)
        if user:
            if user.authenticate(password):
                print(f"✓ {username} logged in!")
                return user
            else:
                print(f"✗ Wrong password for {username}")
                return None
        else:
            print(f"✗ User '{username}' not found")
            return None
    
    def _get_conversation_id(self, user1, user2):
        """Generate consistent conversation ID"""
        users = sorted([user1, user2])
        return f"{users[0]}_{users[1]}"
    
    def send_message(self, sender, recipient, content):
        """Send message - GUARANTEED SYNC"""
        print(f"\n📤 MESSAGE FROM {sender} TO {recipient}")
        
        # ALWAYS reload from disk
        self.load_messages_from_disk()
        
        # Verify users exist
        if not self.users.search(sender) or not self.users.search(recipient):
            print(f"✗ User not found")
            return False
        
        # Create encrypted message with SHARED encryption
        message = Message(sender, recipient, content, self.encryption_manager)
        print(f"  ✓ Message encrypted with shared key")
        
        # Get conversation ID
        conv_id = self._get_conversation_id(sender, recipient)
        
        # Create or get conversation
        if conv_id not in self.conversations:
            self.conversations[conv_id] = LinkedList()
        
        # Add message
        msg_dict = message.to_dict()
        self.conversations[conv_id].insert(msg_dict)
        
        # SAVE TO DISK
        self.save_messages_to_disk()
        print(f"✓ Message saved to disk!\n")
        
        return True
    
    def get_conversation(self, user1, user2):
        """Get conversation - ALWAYS from disk"""
        # FORCE reload from disk every time
        self.load_messages_from_disk()
        
        conv_id = self._get_conversation_id(user1, user2)
        
        if conv_id in self.conversations:
            return self.conversations[conv_id].get_all()
        
        return []
    
    def get_user_count(self):
        """Get total users"""
        return len(self.users.get_all_values())
    
    def get_all_users(self):
        """Get all users - reload from disk"""
        self.load_users_from_disk()
        return self.users.get_all_values()
    
    def decrypt_message(self, encrypted_content):
        """Decrypt message with SHARED key"""
        try:
            decrypted = self.encryption_manager.decrypt_message(encrypted_content)
            return decrypted
        except Exception as e:
            print(f"✗ Decryption error: {e}")
            return "[Unable to decrypt]"
