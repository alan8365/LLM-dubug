class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def detect_cycle(node):
    hare = tortoise = node

    while True:
        if hare.next is None:
            return False

        tortoise = tortoise.next
        hare = hare.next.next

        if hare is tortoise:
            return True