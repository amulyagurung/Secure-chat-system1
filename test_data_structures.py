"""
Unit Tests for Data Structures
"""

import pytest
from data_structures import LinkedList, HashMap


class TestLinkedList:
    def test_insert_single(self):
        ll = LinkedList()
        ll.insert("msg1")
        assert len(ll) == 1
    
    def test_insert_multiple(self):
        ll = LinkedList()
        for i in range(5):
            ll.insert(f"msg_{i}")
        assert len(ll) == 5
    
    def test_search_found(self):
        ll = LinkedList()
        msg = {'id': '123', 'content': 'Hello'}
        ll.insert(msg)
        found = ll.search('123')
        assert found == msg
    
    def test_search_not_found(self):
        ll = LinkedList()
        ll.insert({'id': '123', 'content': 'Hello'})
        found = ll.search('999')
        assert found is None
    
    def test_delete_found(self):
        ll = LinkedList()
        ll.insert({'id': '123', 'content': 'Hello'})
        ll.insert({'id': '456', 'content': 'World'})
        result = ll.delete('123')
        assert result is True
        assert len(ll) == 1


class TestHashMap:
    def test_insert_single(self):
        hm = HashMap()
        hm.insert('user1', 'data1')
        assert hm.search('user1') == 'data1'
    
    def test_insert_multiple(self):
        hm = HashMap()
        for i in range(5):
            hm.insert(f'user{i}', f'data{i}')
        assert hm.search('user0') == 'data0'
    
    def test_update_key(self):
        hm = HashMap()
        hm.insert('user1', 'old')
        hm.insert('user1', 'new')
        assert hm.search('user1') == 'new'
    
    def test_delete_found(self):
        hm = HashMap()
        hm.insert('user1', 'data1')
        result = hm.delete('user1')
        assert result is True
        assert hm.search('user1') is None
    
    def test_collision_handling(self):
        hm = HashMap(size=1)  # Force collisions
        hm.insert('key1', 'val1')
        hm.insert('key2', 'val2')
        hm.insert('key3', 'val3')
        assert hm.search('key1') == 'val1'
        assert hm.search('key2') == 'val2'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
