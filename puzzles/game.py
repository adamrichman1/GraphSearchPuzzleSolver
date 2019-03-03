from search import bfs, dfs, weighted_algorithms


class Game:
    heuristic = None
    search_algorithm = None

    def __init__(self, search_algorithm, heuristic):
        Game.search_algorithm = search_algorithm
        Game.heuristic = heuristic if heuristic is not None else "NA"

    def do_search(self):
        if Game.search_algorithm == 'bfs':
            Game.print_result(bfs.search(self))
        elif Game.search_algorithm == 'dfs':
            Game.print_result(dfs.search(self))
        elif Game.search_algorithm == 'unicost' or Game.search_algorithm == 'greedy' \
                or Game.search_algorithm == 'astar':
            Game.print_result(weighted_algorithms.search(self, Game.search_algorithm))
        else:
            print(">>> ERROR: Invalid search algorithm specified <<<")
            exit(0)

    @staticmethod
    def get_search_algorithm():
        return Game.search_algorithm

    @staticmethod
    def get_heuristic_function():
        return Game.heuristic

    @staticmethod
    def print_result(results):
        sol_path = results[0]
        num_nodes_created = results[1]
        max_frontier_size = results[2]
        max_visited_size = results[3]
        total_path_cost = 0
        if sol_path is not None:
            print("$$$ FOUND SOLUTION $$$\n\n-----Solution Path-----")
            for i, state in enumerate(sol_path):
                cost = str(0 if i == 0 else sol_path[i-1][1])
                print("$$$ State " + str(i + 1) + ": " + state[0].get_id() + " - Cost: " + cost + " $$$")
                total_path_cost += state[1]
        else:
            print("\n$$$ NO SOLUTION COULD BE FOUND $$$")

        print("\nSearch Algorithm: " + Game.search_algorithm)
        print("Search Heuristic: " + Game.heuristic)
        print("\n-----Time Complexity-----")
        print("Nodes created: " + str(num_nodes_created))
        print("Path cost: " + str(total_path_cost))

        print("\n-----Space Complexity-----")
        print("Max Frontier Size: " + str(max_frontier_size))
        print("Max Visited Size: " + str(max_visited_size))

    @staticmethod
    def was_already_visited(visited, new_state_id):
        return new_state_id in visited
