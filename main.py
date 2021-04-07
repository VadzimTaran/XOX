from random import randint

# Constants
X_0 = ["X", "0"]  # Playing characters
NUM_OF_PLAYERS = 2  # Number of players
BOARD_SIZE_RANGE = range(2, 11)


##### Board ##############
##### Init Board #########
def init_board(board_size):
    if board_size not in BOARD_SIZE_RANGE:
        print("Error: wrong entered board size")
        return []

    # | 1 | 2 | 3 |
    # -------------
    # | 4 | 5 | 6 |
    # -------------
    # | 7 | 8 | 9 |
    board = []
    # create a board and enumerate cells
    cell_num = 0
    for i in range(board_size):
        row = []
        for j in range(board_size):
            cell_num += 1
            row.append(str(cell_num))
        board.append(row)
    # print_board(board, length)
    # print(cells)
    return board


##### Print Board #########
def print_board(board, player_dict):
    if len(board) == 0:
        print("Error: empty board")
        return

    if len(board) != len(board[0]):
        print("Error: wrong board size")
        return

    # clear screen
    print("\n" * 10)

    length = len(str(board[len(board) - 1][len(board) - 1]))

    # display players
    for player, char in player_dict.items():
        print(player, "{:<{}}".format(":", length * len(board) - 1), char)

    # draw board
    # | 1 | 2 | 3 |
    # -------------
    # | 4 | 5 | 6 |
    # -------------
    # | 7 | 8 | 9 |
    print("-" * ((length + 3) * len(board) + 1))
    for i in range(len(board)):
        for j in range(len(board)):
            print("|", "{:{}}".format(board[i][j], length), "", end="")
        print("|\n", end="")
        print("-" * ((length + 3) * len(board) + 1))


##### Game ##############
def enter_player_name(players):
    if len(players) >= NUM_OF_PLAYERS:  # 2 players
        print("All players are registered")
        return players

    KEY_WORD = "End"  # key word to break the loop
    while len(players) < NUM_OF_PLAYERS:
        player = input(f"Please enter name of player {len(players) + 1} or '{KEY_WORD}': ")
        if player == KEY_WORD:
            break
        # check for duplicates
        if player in players:
            print("Player already exists. Please, try once more")
        # check for empty name
        if player == "":
            print("Player's name is empty. Please, try once more")
        else:
            players.append(player)
    return players


##### Init Players #########
def init_players():
    player_dict = dict()
    print("Enter names of players")
    # enter names
    player_list = []
    player_list = enter_player_name(player_list)
    # check if all palyers registered
    if len(player_list) < NUM_OF_PLAYERS:
        print("Not all players are registered")
        return player_dict
    # select 0 or X
    # select 0
    o_or_x = randint(0, 1)
    # select who first
    who_first = randint(0, 1)
    rev_player_list = player_list[::-1]
    for i, player in enumerate(player_list if who_first else rev_player_list):
        fst_snd_str = ""
        if not i:  # 0
            fst_snd_str = "first"
            player_dict[player] = X_0[o_or_x]
        else:
            fst_snd_str = "second"
            player_dict[player] = X_0[(len(X_0) - 1) - o_or_x]
        print(f"Player {player} plays {fst_snd_str} with {player_dict[player]}.")
    return player_dict


##### Check Board #########
def check_row_filled(row):
    return len(set(row)) == 1


##### Check if Horizontal Rows Filled #########
def check_filled_horizontal(board):
    for row in board:
        if check_row_filled(row):
            return True
    return False


##### Check if Vertical Columns Filled #########
##### Transpose Board #########
def transpose_board(board):
    transpd_board = []
    for i in range(len(board)):
        transpd_board_row = []
        for j in range(len(board[i])):
            transpd_board_row.append(board[j][i])
        transpd_board.append(transpd_board_row)
    return transpd_board


##### Check Board #########
def check_filled_vertical(board):
    return check_filled_horizontal(transpose_board(board))


##### Check if Diagonals Filled #########
# is_direct - direct or reverse
def check_filled_diagonal(board, is_direct=True):
    checked_elem = ""
    for i in range(len(board)):
        if is_direct:
            current_elem = board[i][i]
        else:
            current_elem = board[i][len(board) - i - 1]
        # print(current_elem)
        if current_elem not in X_0:
            return False
        if checked_elem != "" and checked_elem != current_elem:
            return False
        checked_elem = current_elem
    return True


##### Check if any Player Has Won - One Line Is Filled #########
def is_won(board):
    return check_filled_horizontal(board) or \
           check_filled_vertical(board) or \
           check_filled_diagonal(board, True) or \
           check_filled_diagonal(board, False)


##### Check if no more Cell Available #########
def is_all_filled(board):
    for row in board:
        if len(set(row)) > len(X_0):
            return False
    return True


##### Check if Int Value Entered #########
def enter_int_value(str_):
    while True:
        try:
            int_value = int(input(str_))
            # check for 0 value, throw exception if true
            if not int_value:
                raise ValueError
        except ValueError:
            print("Wrong value (none-integer) entered. Please, try once more.")
        else:
            break
    return int_value


##### Check if Correct Board Size Entered #########
def enter_board_size():
    while True:
        size = enter_int_value("Please enter board size: ")
        if size not in BOARD_SIZE_RANGE:
            print("Wrong value (not in range [2, 10]) entered. Please, try once more.")
        else:
            break
    return size


##### Make Move #########
def make_move(board, player_str, player_dict):
    print(f"Player {player_str} makes a move.")
    while True:
        cell_num = enter_int_value("Please enter a cell index or '-1' to stop the game: ")
        if cell_num == -1:
            return []
        # calculate coords
        i_coord = (cell_num - 1) // len(board)
        j_coord = cell_num % len(board) - 1
        print(f"You entered {board[i_coord][j_coord]}.")
        if board[i_coord][j_coord] not in X_0:
            board[i_coord][j_coord] = player_dict[player_str]
            break
        else:
            print("Wrong value (already filled) entered. Please, try once more.")
    return board


##### Main #########
def main():
    print("Hello")
    # select board
    board_size = enter_board_size()
    # init board with entered size
    game_board = init_board(board_size)
    # select players
    players = init_players()
    if len(players) < NUM_OF_PLAYERS:
        print("End")
        exit()
    # start game
    print_board(game_board, players)
    # play until one wins all cells are filled or special character is entered
    i = 0
    is_victory = False
    while not is_all_filled(game_board):
        #   show board
        game_board = make_move(game_board, list(players.keys())[i], players)
        if not len(game_board):
            break
        print_board(game_board, players)
        if is_won(game_board):
            is_victory = True
            break
        i = 1 if i == 0 else 0
    # Victory
    if is_victory:
        print(f"Player {list(players.keys())[i]} won!")
    else:
        print("Game was stopped. Draw")


if __name__ == '__main__':
    main()
