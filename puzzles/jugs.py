import math

from graph import State
from game import Game
from ast import literal_eval
from copy import deepcopy


class JugsState(State):
    num_states = 0

    def __init__(self, capacities):
        self.capacities = list(capacities)
        self.heuristic = JugsGame.calculate_heuristic(capacities)
        JugsState.num_states += 1
        State.__init__(self)

    def get_capacities(self):
        return self.capacities

    def get_id(self):
        return str(self.capacities)

    def get_heuristic(self):
        return self.heuristic

    @staticmethod
    def get_num_states():
        return JugsState.num_states


class JugsGame(Game):
    max_capacities = []

    def __init__(self, search_algorithm, heuristic, config):
        Game.__init__(self, search_algorithm, heuristic)
        self.init_state, self.final_state = JugsGame.__parse_config(config)

    def get_init_state(self):
        return self.init_state

    def is_final_state(self, state):
        return state.get_capacities() == self.final_state.get_capacities()

    @staticmethod
    def get_next_moves(edge, visited):
        state = edge.get_to_state()
        fill_edges = {}
        empty_edges = {}
        pour_edges = {}
        for i, source_jug in enumerate(state.get_capacities()):
            if JugsGame.__can_fill_jug(source_jug, i):
                capacities = deepcopy(state.get_capacities())
                fill_amount = JugsGame.max_capacities[i]-capacities[i]
                capacities[i] = JugsGame.max_capacities[i]
                if not Game.was_already_visited(visited, str(capacities)):
                    fill_edges[JugsState(capacities)] = fill_amount
                    # print("$$$ Added fill edge to jug " + str(i) + ": " + str(capacities) + " $$$")
            if source_jug != 0:
                capacities = deepcopy(state.get_capacities())
                if JugsGame.__can_empty_jug(state.get_capacities(), i):
                    empty_amount = capacities[i]
                    capacities[i] = 0
                    if not Game.was_already_visited(visited, str(capacities)):
                        empty_edges[JugsState(capacities)] = empty_amount
                        # print("$$$ Added empty edge to jug " + str(i) + ": " + str(capacities) + " $$$")
            for j, dest_jug in enumerate(state.get_capacities()):
                if JugsGame.__can_do_pour(dest_jug, j, source_jug, i):
                    capacities = deepcopy(state.get_capacities())
                    space_remaining = JugsGame.max_capacities[j] - capacities[j]
                    to_pour = space_remaining if capacities[i] >= space_remaining else capacities[i]
                    capacities[i] -= to_pour
                    capacities[j] += to_pour
                    if not Game.was_already_visited(visited, str(capacities)):
                        pour_edges[JugsState(capacities)] = to_pour
                        # print("$$$ Added pour edge from jug " + str(i) + " to jug " + str(j) + ": " + str(capacities)
                        #       + " $$$")
        state.add_edges(JugsGame.__sort_edges(fill_edges))
        state.add_edges(JugsGame.__sort_edges(empty_edges))
        state.add_edges(JugsGame.__sort_edges(pour_edges))
        return state

    @staticmethod
    def __sort_edges(unsorted):
        sort = sorted(unsorted.iteritems(), key=lambda (k, v): (v, k))
        for index, s in enumerate(sort):
            sort[index] = (s[0], 0)
        sort.reverse()
        return sort

    @staticmethod
    def __can_do_pour(dest_jug, dest_index, source_jug, source_index):
        return dest_jug < JugsGame.max_capacities[dest_index] and source_jug != 0 and source_index != dest_index

    @staticmethod
    def __can_empty_jug(jugs, jug_index):
        num_jugs_with_water = 0
        for jug in jugs:
            if jug > 0:
                num_jugs_with_water += 1
                if num_jugs_with_water == 2:
                    return jugs[jug_index] != 0
        return False

    @staticmethod
    def __can_fill_jug(jug, jug_index):
        return jug < JugsGame.max_capacities[jug_index]

    @staticmethod
    def __parse_config(config):
        JugsGame.max_capacities = list(literal_eval(config[1]))
        return JugsState(literal_eval(config[2])), JugsState(literal_eval(config[3]))

    @staticmethod
    def get_num_states():
        return JugsState.get_num_states()

    @staticmethod
    def calculate_heuristic(capacities):
        heuristic = Game.get_heuristic_function()
        if heuristic is None and (Game.get_search_algorithm() == 'greedy' or Game.get_search_algorithm() == 'astar'):
            print(">>> ERROR: No heuristic function specified <<<")
            exit(0)
            return
        elif Game.get_search_algorithm() != 'greedy' and Game.get_search_algorithm() != 'astar':
            return 0
        elif heuristic == 'd':
            return JugsGame.__calculate_distance_heuristic(capacities)
        elif heuristic == 'mj':
            return JugsGame.__calculate_misplaced_jugs_heuristic(capacities)
        else:
            print(">>> ERROR: Invalid heuristic function specified <<<")
            exit(0)

    @staticmethod
    def __calculate_distance_heuristic(capacities):
        heuristic = 0
        for index, jug in enumerate(capacities):
            heuristic += JugsGame.__calculate_dist(index, capacities)
        return heuristic

    @staticmethod
    def __calculate_misplaced_jugs_heuristic(capacities):
        heuristic = 0
        for index, jug in enumerate(capacities):
            if JugsGame.max_capacities[index] != jug:
                heuristic += 1
        return heuristic

    @staticmethod
    def __calculate_dist(index, capacities):
        return abs(capacities[index]-JugsGame.max_capacities[index])
