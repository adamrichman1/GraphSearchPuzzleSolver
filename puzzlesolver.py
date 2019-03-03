import sys
from puzzles.cities import CitiesGame
from puzzles.jugs import JugsGame
from puzzles.tiles import TilesGame


def read_config_file(filename):
    return [line.rstrip('\n') for line in open("resources/" + filename)]


def main():
    # Get command line args
    args = sys.argv
    num_args = len(args)

    # Confirm number of arguments is correct
    if num_args < 3 or num_args > 4:
        print(">>> ERROR: Please specify valid command line arguments <<<")
        exit(0)

    config_file_name = args[1]
    search_algorithm = args[2]

    if num_args == 4:
        heuristic = args[3]
    else:
        heuristic = None

    config = read_config_file(config_file_name)

    if config[0] == 'cities':
        game = CitiesGame(search_algorithm, heuristic, config)
    elif config[0] == 'jugs':
        game = JugsGame(search_algorithm, heuristic, config)
    elif config[0] == 'tiles':
        game = TilesGame(search_algorithm, heuristic, config)
    else:
        print(">>> ERROR: Invalid configuration file specified <<<")
        game = None
        exit(0)

    game.do_search()


main()
