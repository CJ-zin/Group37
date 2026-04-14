# data_structures.py
class Node:
    """Basic structural element for the LinkedList."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """A singly linked list to track chronological user recycling history."""
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def remove_last(self):
        """Removes the most recent record, useful for undo operations."""
        if not self.head: return None
        if self.head == self.tail:
            data = self.head.data
            self.head = self.tail = None
            return data
        current = self.head
        while current.next != self.tail:
            current = current.next
        data = self.tail.data
        self.tail = current
        self.tail.next = None
        return data

    def get_all_records(self):
        """Return all node data as a sequential list."""
        records = []
        current = self.head
        while current:
            records.append(current.data)
            current = current.next
        return records

    def is_empty(self): return self.head is None

class Stack:
    """LIFO stack to power the 'Undo' disposal functionality."""
    def __init__(self): self.items = []
    def push(self, item): self.items.append(item)
    def pop(self): return self.items.pop() if not self.is_empty() else None
    def is_empty(self): return len(self.items) == 0

class MinHeap:
    """Priority queue implementation driving Dijkstra's shortest path resolution."""
    def __init__(self): self.heap = []
    def push(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)
    def pop(self):
        if not self.heap: return None
        if len(self.heap) == 1: return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root
    def is_empty(self): return len(self.heap) == 0
    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx][0] < self.heap[parent][0]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._sift_up(parent)
    def _sift_down(self, idx):
        smallest = idx
        left, right = 2 * idx + 1, 2 * idx + 2
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]: smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]: smallest = right
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._sift_down(smallest)


class Queue:
    """FIFO queue to model user lines waiting at a recycling station."""
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.insert(0, item)
    def dequeue(self):
        return self.items.pop() if not self.is_empty() else None
    def is_empty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)


class BSTNode:
    """Node for UserLeaderboardBST."""
    def __init__(self, user):
        self.user = user
        self.left = None
        self.right = None

class UserLeaderboardBST:
    """Binary Search Tree keeping user records sorted by earned points."""
    def __init__(self):
        self.root = None

    def insert(self, user):
        """Insert user based on their accumulated points."""
        if not self.root:
            self.root = BSTNode(user)
            return
        curr = self.root
        while True:
            if user.points >= curr.user.points:
                if curr.left is None:
                    curr.left = BSTNode(user)
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = BSTNode(user)
                    break
                curr = curr.right

    def get_inorder_ranking(self):
        """Retrieve ranking sequentially from highest to lowest points."""
        ranking = []
        def inorder(node):
            if node:
                inorder(node.left)
                ranking.append({"name": node.user.name, "points": round(node.user.points, 1)})
                inorder(node.right)
        inorder(self.root)
        return ranking