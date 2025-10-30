class Node():
    def __init__(self, person_id,movie_id, explored, parent):
        self.person_id = person_id
        self.movie_id = movie_id
        self.explored = explored
        self.parent = parent


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_person_movie(self, person_id,movie_id):
        return any(node.person_id == person_id and node.movie_id == movie_id for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0
    
    def next(self):
        for node in self.frontier:
            if node.explored is False:
                return node
        
        return None

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
