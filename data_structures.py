"""
Custom Data Structures Module
Implements LinkedList and HashMap for the Secure Message Chat System
"""

# ============================================================================
# LINKEDLIST IMPLEMENTATION
# ============================================================================

class Node:
    """Node class for LinkedList implementation"""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """
    Custom LinkedList implementation for storing messages in conversation history.
    Maintains insertion order and allows efficient traversal.
    """
    def __init__(self):
        self.head = None
        self.size = 0
    
    def insert(self, data):
        """Insert data at end of LinkedList"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def get_all(self):
        """Return all messages in order"""
        messages = []
        current = self.head
        while current:
            messages.append(current.data)
            current = current.next
        return messages
    
    def search(self, message_id):
        """Search for message by ID"""
        current = self.head
        while current:
            if current.data.get('id') == message_id:
                return current.data
            current = current.next
        return None
    
    def delete(self, message_id):
        """Delete message by ID"""
        if self.head is None:
            return False
        
        if self.head.data.get('id') == message_id:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data.get('id') == message_id:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False
    
    def __len__(self):
        return self.size


# ============================================================================
# HASHMAP IMPLEMENTATION
# ============================================================================

class HashMap:
    """
    Custom HashMap implementation using separate chaining for collision resolution.
    Used for efficient user lookups and storage.
    """
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        """Hash function using simple modulo"""
        return hash(key) % self.size
    
    def insert(self, key, value):
        """Insert key-value pair"""
        index = self._hash(key)
        
        # Check if key already exists and update
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        
        # Insert new key-value pair
        self.table[index].append((key, value))
    
    def search(self, key):
        """Search for value by key"""
        index = self._hash(key)
        
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                return True
        return False
    
    def get_all_values(self):
        """Return all values in HashMap"""
        values = []
        for chain in self.table:
            for k, v in chain:
                values.append(v)
        return values
