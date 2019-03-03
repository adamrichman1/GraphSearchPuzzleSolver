import re
from graph import State
from game import Game
from ast import literal_eval
from copy import deepcopy
import math


class TilesState(State):
    num_states = 0

    def __init__(self, board):
        self.board = board
        self.heuristic = TilesGame.calculate_heuristic(board)
        TilesState.num_states += 1
        State.__init__(self)

    def get_board(self):
        return self.board

    def get_id(self):
        return str(self.board)

    def get_empty_index(self):
        for i, tile in enumerate(self.board):
            if tile == 'b':
                return i
        print(">>> ERROR: NO BLANK TILE FOUND <<<")
        exit(0)
        return None

    def get_heuristic(self):
        return self.heuristic

    @staticmethod
    def get_num_states():
        return TilesState.num_states


class TilesGame(Game):
    n = 0
    final_state = None

    def __init__(self, search_algorithm, heuristic, config):
        Game.__init__(self, search_algorithm, heuristic)
        self.init_state, TilesGame.final_state = TilesGame.__parse_config(config)
        print("$$$ Final State: " + str(self.final_state.get_board()) + " $$$\n")
        self.graph = TilesGame.__init_states(config)

    def get_init_state(self):
        return self.init_state

    def is_final_state(self, state):
        return state.get_board() == self.final_state.get_board()

    @staticmethod
    def get_next_moves(edge, visited):
        state = edge.get_to_state()
        board = state.get_board()
        empty_index = state.get_empty_index()

        # Top left corner
        if empty_index == 0:
            print("$$$ Top left corner $$$")
        # Top right corner
        elif empty_index == TilesGame.n - 1:
            print("$$$ Top right corner $$$")
        # Bottom left corner
        elif empty_index == TilesGame.n * (TilesGame.n - 1):
            print("$$$ Bottom left corner $$$")
        # Bottom right corner
        elif empty_index == TilesGame.n * TilesGame.n - 1:
            print("$$$ Bottom right corner $$$")
        # Left wall
        elif empty_index % TilesGame.n == 0:
            print("$$$ Left wall $$$")
        # Right wall
        elif (empty_index + 1) % TilesGame.n == 0:
            print("$$$ Right wall $$$")
        # Top wall
        elif empty_index < TilesGame.n:
            print("$$$ Top wall $$$")
        # Bottom wall
        elif empty_index > TilesGame.n * (TilesGame.n - 1):
            print("$$$ Bottom wall $$$")
        # Middle region
        else:
            print("$$$ Middle region $$$")

        if TilesGame.__can_move_right(empty_index):
            move_right = TilesGame.__swap_tiles(deepcopy(board), empty_index, empty_index + 1)
            if not Game.was_already_visited(visited, str(move_right)):
                new_state = TilesState(move_right)
                print("$$$ Adding RIGHT edge $$$")
                state.add_edge_no_cost(new_state)

        if TilesGame.__can_move_up(empty_index):
            move_up = TilesGame.__swap_tiles(deepcopy(board), empty_index, empty_index - TilesGame.n)
            if not Game.was_already_visited(visited, str(move_up)):
                new_state = TilesState(move_up)
                print("$$$ Adding UP edge $$$")
                state.add_edge_no_cost(new_state)

        if TilesGame.__can_move_left(empty_index):
            move_left = TilesGame.__swap_tiles(deepcopy(board), empty_index, empty_index - 1)
            if not Game.was_already_visited(visited, str(move_left)):
                new_state = TilesState(move_left)
                print("$$$ Adding LEFT edge $$$")
                state.add_edge_no_cost(new_state)

        if TilesGame.__can_move_down(empty_index):
            move_down = TilesGame.__swap_tiles(deepcopy(board), empty_index, empty_index + TilesGame.n)
            if not Game.was_already_visited(visited, str(move_down)):
                new_state = TilesState(move_down)
                print("$$$ Adding DOWN edge $$$")
                state.add_edge_no_cost(new_state)

        return state

    @staticmethod
    def __can_move_up(empty_index):
        return empty_index > TilesGame.n - 1

    @staticmethod
    def __can_move_down(empty_index):
        return empty_index < TilesGame.n * (TilesGame.n - 1)

    @staticmethod
    def __can_move_left(empty_index):
        return empty_index % TilesGame.n != 0

    @staticmethod
    def __can_move_right(empty_index):
        return (empty_index + 1) % TilesGame.n != 0

    @staticmethod
    def __init_states(config):
        return config

    @staticmethod
    def __swap_tiles(board, index1, index2):
        old = board[index1]
        board[index1] = board[index2]
        board[index2] = old
        return board

    @staticmethod
    def __parse_config(config):
        for i, line in enumerate(config):
            config[i] = re.sub(r'[^\x00-\x7f]', "'", line)
        TilesGame.n = literal_eval(config[1])
        return TilesState(literal_eval(config[2])), TilesState(literal_eval(config[3]))

    @staticmethod
    def get_num_states():
        return TilesState.get_num_states()

    @staticmethod
    def calculate_heuristic(board):
        heuristic = Game.get_heuristic_function()
        if heuristic is None and (Game.get_search_algorithm() == 'greedy' or Game.get_search_algorithm() == 'astar'):
            print(">>> ERROR: No heuristic function specified <<<")
            exit(0)
            return
        elif Game.get_search_algorithm() != 'greedy' and Game.get_search_algorithm() != 'astar':
            return 0
        elif heuristic == 'md':
            return TilesGame.__calculate_manhattan_distance_heuristic(board)
        elif heuristic == 'eu':
            return TilesGame.__calculate_euclidean_distance_heuristic(board)
        elif heuristic == 'mt':
            return TilesGame.__calculate_misplaced_tile_heuristic(board)
        else:
            print(">>> ERROR: Invalid heuristic function specified <<<")
            exit(0)

    @staticmethod
    def __calculate_manhattan_distance_heuristic(board):
        heuristic = 0
        for index, tile in enumerate(board):
            if tile != 'b':
                heuristic += TilesGame.__calculate_vertical_dist(index, board) + \
                             TilesGame.__calculate_horizontal_dist(index, board)
        return heuristic

    @staticmethod
    def __calculate_euclidean_distance_heuristic(board):
        heuristic = 0
        for index, tile in enumerate(board):
            if tile != 'b':
                sum_of_squares = math.pow(TilesGame.__calculate_vertical_dist(index, board), 2) + \
                                 math.pow(TilesGame.__calculate_horizontal_dist(index, board), 2)
                heuristic += round(math.sqrt(sum_of_squares), 4)
        return heuristic

    @staticmethod
    def __calculate_misplaced_tile_heuristic(board):
        heuristic = 0
        for index, tile in enumerate(board):
            if tile != 'b':
                if index != tile-1:
                    heuristic += 1
        return heuristic

    @staticmethod
    def __calculate_vertical_dist(index, board):
        final_index = board[index] - 1
        row = index / TilesGame.n
        final_row = final_index / TilesGame.n
        return abs(row - final_row)

    @staticmethod
    def __calculate_horizontal_dist(index, board):
        final_index = board[index] - 1
        column = index % TilesGame.n
        final_column = final_index % TilesGame.n
        return abs(column - final_column)
