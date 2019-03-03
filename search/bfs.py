from Queue import Queue
from puzzles.graph import Edge, State

# FIFO Queue of states to visit next
frontier = Queue()
max_frontier_size = 0

# HashMap for visited states, entry present = visited
visited = {}


def search(game):
    global max_frontier_size
    frontier.put(Edge(State(), game.get_init_state(), 0))
    iteration = 0
    while True:
        if frontier.qsize() > max_frontier_size:
            max_frontier_size = frontier.qsize()

        # Get next state
        edge = frontier.get()

        iteration += 1
        print("\nIteration " + str(iteration) + ": " + str(edge.get_to_state().get_id()))

        state = game.get_next_moves(edge, visited)

        # Add state to visited
        visited[str(state.get_id())] = edge

        # Check if state is final state
        print("$$$ Checking state " + str(state.get_id()) + " $$$")
        if game.is_final_state(state):
            return create_sol_path(state), game.get_num_states(), max_frontier_size, len(visited)

        print("$$$ Incorrect state " + str(state.get_id()) + " $$$")

        # Get next state
        for edge in state.get_edges():
            state = edge.get_to_state()
            if state.get_id() not in visited:
                print("$$$ Added state " + str(state.get_id()) + " to frontier list $$$")
                frontier.put(edge)
            else:
                print("$$$ State already visited " + str(state.get_id()) + " $$$")

        # Break loop if all states have been checked
        if frontier.empty():
            break

    return None


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
