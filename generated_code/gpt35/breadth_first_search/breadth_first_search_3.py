from collections import deque

def breadth_first_search(startnode, goalnode):
    queue = deque()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while queue:
        node = queue.popleft()

        if node == goalnode:
            return True
        else:
            queue.extend(successor for successor in node.successors if successor not in nodesseen)
            nodesseen.update(successor for successor in node.successors)

    return False