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
            queue.extend(n for n in node.successors if n not in nodesseen)
            nodesseen.update(node.successors)

    return False