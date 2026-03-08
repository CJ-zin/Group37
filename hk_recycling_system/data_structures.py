# data_structures.py

class Node:
    """Linked list node"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Singly linked list for storing chronological recycling history"""
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        """Append a new record to the end of the list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def get_all_records(self):
        """Get a list representation of all records"""
        records = []
        current = self.head
        while current:
            records.append(current.data)
            current = current.next
        return records

    def is_empty(self):
        return self.head is None