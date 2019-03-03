from puzzles.graph import Edge, State
from heapq import heappush, heappop

# PriorityQueue backed list
frontier = []
max_frontier_size = 0

# Maps state objects to PriorityQueue Tuples
frontier_map = {}

# HashMap for visited states, entry present = visited
visited = {}


def search(game, search_algorithm):
    global max_frontier_size
    init_edge = Edge(State(), game.get_init_state(), 0)
    heappush(frontier, (init_edge.get_cost(), init_edge.get_cost2(), init_edge))
    frontier_map[init_edge.get_to_state()] = (init_edge.get_cost(), init_edge.get_cost2(), init_edge)
    iteration = 0
    while True:
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

        # Get next state
        edge = get_next_edge()[2]
        iteration += 1
        print("\nIteration " + str(iteration) + ": " + edge.get_to_state().get_id())
        state = game.get_next_moves(edge, visited)

        print("$$$ Edge: " + edge.get_from_state().get_id() + " ---> " + edge.get_to_state().get_id() + " $$$")

        # Add state to visited
        visited[state.get_id()] = edge

        # Check if state is final state
        print("$$$ Checking state " + state.get_id() + " $$$")
        if game.is_final_state(state):
            return create_sol_path(state), game.get_num_states(), max_frontier_size, len(visited)
        print("$$$ Incorrect state " + state.get_id() + " $$$")

        # Add unvisited edges to frontier list and update edges with improved costs if available
        edges = state.get_edges()
        for e in edges:
            s = e.get_to_state()
            if s.get_id() not in visited:
                new_cost = get_cost(search_algorithm, edge, e)
                if not frontier_contains(e):
                    heappush(frontier, (new_cost, e.get_cost2(), e))
                else:
                    if get_old_cost(search_algorithm, frontier.remove(frontier_map.get(e.get_to_state()))) > new_cost:
                        # Update the cost
                        e.set_cost(new_cost)
                        heappush(frontier, (new_cost, e.get_cost2(), e))
                        frontier_map[e.get_to_state()] = (new_cost, e.get_cost2(), e)
                        print("$$$ Added state " + s.get_id() + " to frontier list $$$")
                    else:
                        # Re-add to PQ
                        heappush(frontier, (new_cost, e.get_cost2(), e))

        # Break loop if all states have been checked
        if len(frontier) == 0:
            break

    return None


def get_next_edge():
    return heappop(frontier)


def frontier_contains(edge):
    return len(frontier) != 0 and frontier.__contains__(frontier_map.get(edge.get_to_state()))


def create_sol_path(state):
    sol_path = []
    edge_cost = 0
    while True:
        sol_path.append((state, edge_cost))
        edge = visited[state.get_id()]
        state = edge.get_from_state()
        edge_cost = edge.get_cost()
        if state.get_id() == "Start":
            break

    sol_path.reverse()
    return sol_path


def get_cost(search_algorithm, from_edge, to_edge):
    if search_algorithm == 'unicost':
        return from_edge.get_cost() + to_edge.get_cost()
    elif search_algorithm == 'greedy':
        return from_edge.get_to_state().get_heuristic()
    elif search_algorithm == 'astar':
        return from_edge.get_to_state().get_heuristic() + from_edge.get_cost() + to_edge.get_cost()
    else:
        print(">>> ERROR: Invalid search algorithm specified <<<")
        exit(0)


def get_old_cost(search_algorithm, node):
    if search_algorithm == 'unicost':
        return node[2].get_cost()
    elif search_algorithm == 'greedy':
        return node[0]
    elif search_algorithm == 'astar':
        return node[0]
    else:
        print(">>> ERROR: Invalid search algorithm specified <<<")
        exit(0)
