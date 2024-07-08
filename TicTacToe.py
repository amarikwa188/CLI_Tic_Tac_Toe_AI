from copy import deepcopy
import time

board: list[list[str]] = [['[ ]', '[ ]', '[ ]'],
                          ['[ ]', '[ ]', '[ ]'],
                          ['[ ]', '[ ]', '[ ]']]

num_board: list[list[str]] = [['[1]', '[2]', '[3]'],
                              ['[4]', '[5]', '[6]'],
                              ['[7]', '[8]', '[9]']]


def print_board(state: list[list[str]]) -> None:
    """
    Prints the given game board.\n
    :param state: a 2-dimentional array of board spaces\n
    :return: None
    """
    for i in range(3):
        for j in range(3):
            print(state[i][j], end="")
        print()
    print()


def clear_board(state: list[list[str]]) -> None:
    """
    Clears all spaces on a given board.\n
    :param state: a 2-dimenional array of board spaces\n
    :return: None
    """
    for i in range(3):
        for j in range(3):
            state[i][j] = '[ ]'


def condense(state: list[list[str]]) -> list[str]:
    """
    Converts a given board into a list of strings representing \
    all rows, columns and diagonals.\n
    :param state: a 2-dimentional array of board spaces\n
    :return: horizontal, vertical and diagonal strings
    """
    lines: list[str] = list()

    for i in range(3):
        line: str = ''
        for j in range(3):
            line += state[i][j]
        lines.append(line)

    for i in range(3):
        line: str = ''
        for j in range(3):
            line += state[j][i]
        lines.append(line)

    lines.append(state[0][2] + state[1][1] + state[2][0])
    lines.append(state[0][0] + state[1][1] + state[2][2])

    return lines


def terminal(state: list[list[str]]) -> bool:
    """
    Determines whether the game is over for a given board.\n
    :param state: a 2-dimentional array of board spaces\n
    :return: True -> game is over, False -> game is ongoing
    """
    lines: list[str] = condense(state)
    full: bool = all('[ ]' not in line for line in lines)

    for line in lines:
        if line in ('[O][O][O]', '[X][X][X]'):
            return True

    return full


def value(state: list[list[str]]) -> int:
    """
    Calculates the value of a terminal game board.\n
    :param state: a 2-dimentional array of board spaces\n
    :return: 1 -> cpu win, 0 -> draw, -1 -> player win
    """
    if not terminal(state):
        raise "Error: state not terminal"

    lines: list[str] = condense(state)

    if '[O][O][O]' in lines:
        return 1
    elif '[X][X][X]' in lines:
        return -1
    else:
        return 0


def player(state: list[list[str]]) -> str:
    """
    Determines whose turn it is.\n
    :param state: a 2-dimentional array of board spaces\n
    :return: 'player' | 'cpu'
    """
    count: int = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != '[ ]':
                count += 1

    return "cpu" if count % 2 else "player"


def actions(state: list[list[str]]) -> list[list[list[str]]]:
    """
    Creates a list of every possible next move on a given board.\n
    :param state: a 2-dimentional array of board spaces\n
    :return: an array of single move boards
    """
    action_list: list[list[list[str]]] = list()
    empty_spaces: list[tuple[int]] = list()

    for i in range(3):
        for j in range(3):
            if state[i][j] == '[ ]':
                empty_spaces.append((i, j))

    for pos in empty_spaces:
        action: list[list[str]] = [['[ ]', '[ ]', '[ ]'], ['[ ]', '[ ]', '[ ]'], ['[ ]', '[ ]', '[ ]']]
        action[pos[0]][pos[1]] = '[O]' if player(state) == "cpu" else '[X]'
        action_list.append(action)
    return action_list


def result(state: list[list[str]], action: list[list[str]]) -> list[list[str]]:
    """
    Merges a given board and a single move action board and returns the result.\n
    :param state: a 2-dimentional array of board spaces
    :param action: a 2-dimentional array of board spaces\n
    :return: a board with the additional move played
    """
    new: list[list[str]] = deepcopy(state)

    for i in range(3):
        for j in range(3):
            if action[i][j] != '[ ]':
                new[i][j] = action[i][j]
    return new


def minimax(state: list[list[str]], depth: int, alpha: int, beta: int,  maximize: bool) -> int:
    """
    Determines the potential value of a given game board, simulating perfect oppositional play.\n
    :param state: a 2-dimentional array of board spaces
    :param depth: level of moves ahead of the current state
    :param alpha: highest quality play, used for pruning
    :param beta: highest quality play for opposition, used for pruning
    :param maximize: True -> simulating turn, False -> simulating opposition turn\n
    :return: value of game given state
    """
    if terminal(state):
        return value(state)

    if maximize:
        max_val: int = -100
        for action in actions(state):
            evaluation: int = minimax(result(state, action), depth+1, alpha, beta, False)
            max_val = max(max_val, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_val

    else:
        min_val: int = 100
        for action in actions(state):
            evaluation: int = minimax(result(state, action), depth+1, alpha, beta, True)
            min_val = min(min_val, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_val


def find_best_move(state: list[list[str]]) -> tuple:
    """
    Determines the potential value of every possible move using minimax() and\
    returns the position(x, y) of the best move.\n
    :param state: a 2-dimentional array of board spaces\n
    :return: the position of the best move
    """ 
    best_val: int = -100
    best_move: tuple = (-1, -1)

    for i in range(3):
        for j in range(3):
            if state[i][j] == '[ ]':
                state[i][j] = '[O]'

                move_val: int = minimax(state, 0, -100, 100, False)

                state[i][j] = '[ ]'

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move


def convert(inp: int) -> tuple:
    """
    Takes a postion on the board from 1-9 and returns the corresponding indexes\
    in the array.\n
    :param inp: board position from 1-9\n
    :return: equivalent array indexes
    """
    row: int = int(inp // 3.1)
    col: int = (inp % 3) - 1 if inp % 3 else 2
    return row, col


def revert(inp: tuple) -> int:
    """
    Takes a position on the board in the form of its array indexes and return\
    its corresponding value from 1-9.\n
    :param inp: 2-dimentional array indexes\n
    :return: equivalent ui position
    """
    return (inp[0]*3) + 1 + inp[1]


def play(pos: tuple, turn: str = "player") -> None:
    """
    Plays a move in a certain position.\n
    :param pos: the desired play position
    :param turn: the player making the move\n
    :return: None
    """
    print(f"{turn} plays {revert(pos)}")
    board[pos[0]][pos[1]] = '[O]' if turn == "cpu" else '[X]'


if __name__ == '__main__':
    print("TIC-TAC-TOE")
    print("-----------")
    print_board(num_board)
    print("Place 'X' on a cell from 1-9.")

    while not terminal(board):
        while True:
            try:
                com: int = int(input("Your play:\n>"))
            except ValueError:
                print("Invalid input: Enter a number")
            else:
                space: tuple = convert(com)
                if board[space[0]][space[1]] != '[ ]':
                    print("Invalid input: Space taken")
                else:
                    break

        play(space)
        print_board(board)

        if terminal(board):
            break

        time.sleep(0.3)
        play(find_best_move(board), turn="cpu")
        print_board(board)

    results: int = value(board)
    print("CPU wins!" if results > 0 else "Player wins" if results < 0 else "Draw!")