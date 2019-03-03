from puzzles.graph import Edge, State

# List-based stack
frontier = []
max_frontier_size = 0

# To hold current solution path during search to avoid cycles
solution_path = []
solution_path_indexes = {}


def search(game):
    global max_frontier_size
    iteration = 0
    frontier.append(Edge(State(), game.get_init_state(), 0))
    while True:
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

        # Add next edge to solution path
        edge = frontier.pop()
        iteration += 1
        print("\nIteration " + str(iteration) + ": " + edge.get_to_state().get_id())
        while True:
            if len(solution_path) == 0:
                break
            s = solution_path.pop()
            cost = s[1]
            s = s[0]
            solution_path_indexes.pop(s.get_id())
            if s.get_id() == edge.get_from_state().get_id():
                solution_path.append((s, cost))
                solution_path_indexes[s.get_id()] = len(solution_path)
                break
            print("--- Removing " + s.get_id() + " from solution path ---")
        print("+++ Adding " + edge.get_to_state().get_id() + " to solution path +++")
        solution_path.append((edge.get_to_state(), edge.get_cost()))
        solution_path_indexes[edge.get_to_state().get_id()] = len(solution_path)
        # print("*** New solution path: " + str(solution_path) + " ***")

        # Check if state is final state
        state = game.get_next_moves(edge, solution_path_indexes)
        print("$$$ Checking state " + state.get_id() + " $$$")
        if game.is_final_state(state):
            return solution_path, game.get_num_states(), max_frontier_size, 0

        print("$$$ Incorrect state " + state.get_id() + " $$$")

        # Recursively search tree until final state is found
        edges = state.get_edges()
        for e in edges:
            if not e.get_to_state().get_id() in solution_path_indexes:
                frontier.append(e)

        # Break loop if all states have been checked
        if len(frontier) == 0:
            break

    # return None if no solution was found
    return None
