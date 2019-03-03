from graph import State
from game import Game
from ast import literal_eval
import math


class CitiesState(State):
    num_states = 0

    def __init__(self, city, x, y):
        self.city = city
        self.x = x
        self.y = y
        self.heuristic = CitiesGame.calculate_heuristic((x, y))
        CitiesState.num_states += 1
        State.__init__(self)

    def get_id(self):
        return self.city

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_heuristic(self):
        return self.heuristic

    @staticmethod
    def get_num_states():
        return CitiesState.num_states


class CitiesGame(Game):
    final_city = None
    final_coordinates = None

    def __init__(self, search_algorithm, heuristic, config):
        Game.__init__(self, search_algorithm, heuristic)
        init_city, self.states = self.__init_graph(config)
        self.init_state = self.__find_state(init_city)

    def get_init_state(self):
        return self.init_state

    @staticmethod
    def is_final_state(state):
        return state.get_id() == CitiesGame.final_city

    def __find_state(self, city):
        # Find init state data
        state = self.states[city]

        # Ensure initial state was created
        if state is None:
            print(">>> ERROR: COULDN'T FIND STATE FOR CITY: " + city + " <<<")
            exit(0)
        return state

    @staticmethod
    def get_next_moves(edge, visited):
        return edge.get_to_state()

    @staticmethod
    def __init_graph(config):
        # Parse config data
        config_data = CitiesGame.__parse_config(config)

        # Get Config data
        cities = config_data[0]
        init_city = config_data[1]
        CitiesGame.final_city = config_data[2]
        CitiesGame.final_coordinates = CitiesGame.__find_coordinates(config_data[2], cities)
        edges = config_data[3]

        states = CitiesGame.__create_states(cities, edges)

        return init_city, states

    @staticmethod
    def __find_coordinates(city, cities):
        for c in cities:
            if c[0] == city:
                return c[1], c[2]

    @staticmethod
    def __create_states(cities, edges):
        states = {}
        for city in cities:
            states[city[0]] = CitiesState(*city)

        for edge in edges:
            # print("$$$ Adding edge from " + edge[0] + " to " + edge[1])
            states[edge[0]].add_edge(states[edge[1]], edge[2])
            states[edge[1]].add_edge(states[edge[0]], edge[2])

        return states

    @staticmethod
    def __parse_config(config):
        edges = []
        for i, line in enumerate(config):
            if i <= 3:
                continue
            edges.append(literal_eval(config[i]))
        return [literal_eval(config[1]), literal_eval(config[2]), literal_eval(config[3]), edges]

    @staticmethod
    def get_num_states():
        return CitiesState.get_num_states()

    @staticmethod
    def calculate_heuristic(coordinates):
        heuristic = Game.get_heuristic_function()
        if heuristic is None and (Game.get_search_algorithm() == 'greedy' or Game.get_search_algorithm() == 'astar'):
            print(">>> ERROR: No heuristic function specified <<<")
            exit(0)
            return
        elif Game.get_search_algorithm() != 'greedy' and Game.get_search_algorithm() != 'astar':
            return 0
        elif heuristic == 'md':
            return CitiesGame.__calculate_manhattan_distance_heuristic(coordinates)
        elif heuristic == 'eu':
            return CitiesGame.__calculate_euclidean_distance_heuristic(coordinates)
        else:
            print(">>> ERROR: Invalid heuristic function specified <<<")
            exit(0)

    @staticmethod
    def __calculate_manhattan_distance_heuristic(coordinates):
        heuristic = 0
        heuristic += CitiesGame.__calculate_vertical_dist(coordinates[1]) + \
                     CitiesGame.__calculate_horizontal_dist(coordinates[0])
        return heuristic

    @staticmethod
    def __calculate_euclidean_distance_heuristic(coordinates):
        heuristic = 0

        sum_of_squares = math.pow(CitiesGame.__calculate_vertical_dist(coordinates[1]), 2) + \
                         math.pow(CitiesGame.__calculate_horizontal_dist(coordinates[0]), 2)
        heuristic += round(math.sqrt(sum_of_squares), 4)
        return heuristic

    @staticmethod
    def __calculate_vertical_dist(x):
        return abs(x - CitiesGame.final_coordinates[0])

    @staticmethod
    def __calculate_horizontal_dist(y):
        return abs(y - CitiesGame.final_coordinates[1])
