class Node:
    def __init__(self, location, move=None, parent=None,):
        self._parent = parent
        self._location = location
        self._move = move
    
    def __str__(self):
        return f"{self.location}:{self.move}"
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def location(self):
        return self._location
    
    @property
    def move(self):
        return self._move

class Frontier:
    def __init__(self):
        self._frontier = set()
        self._explored = set()
    
    @property
    def explored(self):
        return self._explored

    def __str__(self):
        nodes = [str(node) for node in self._frontier]
        return f"{nodes}"

    def __iter__(self):
        for node in self._frontier:
            yield node

    def add(self, node: Node):
        self._frontier.add(node)
    
    def remove(self, node: Node):
        self._frontier.remove(node)
        self._explored.add(node.location)
        return node
