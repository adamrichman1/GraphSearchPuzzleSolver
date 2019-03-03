class State:

    def __init__(self):
        self.edges = []

    def get_edges(self):
        return self.edges

    def add_edge(self, to_state, cost):
        self.edges.append(Edge(self, to_state, cost))

    def add_edges(self, edges):
        for e in edges:
            self.edges.append(Edge(self, e[0], e[1]))

    def add_edge_no_cost(self, to_state):
        self.add_edge(to_state, 0)

    def get_id(self):
        return "Start"


class Edge:
    cost2 = 0

    def __init__(self, from_state, to_state, cost):
        self.cost = cost
        self.cost2 = Edge.cost2
        Edge.cost2 += 1
        self.to_state = to_state
        self.from_state = from_state

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost

    def get_cost2(self):
        return self.cost2

    def get_to_state(self):
        return self.to_state

    def get_from_state(self):
        return self.from_state
