import sys
from enum import Enum

"""
Custom Types:
I neither want to go full OO or full FP here.
The game will still be very imperative to keep it easy to understand for a beginner.
I am just using class for typing. 
Something similar to defrecord in Clojure.
Tic-Tac-Toe is simple enough
    1. To be solved without thinking in terms of state machines
    2. To be modelled as a state machine.
    3. Can be achieved with basic enum types.
"""


class State(Enum):
    X_turn = "state_x_turn"
    O_turn = "state_o_turn"
    X_win = "state_x_win"
    O_win = "state_o_win"
    Draw = "state_draw"


class Player(Enum):
    X = "X"
    O = "O"


# This defines all the valid input for our state machines
class Move(Enum):
    x_n = "x_n"  # X moves, no winning happened, and board is not full
    x_w = "x_w"  # X moves, and X wins
    x_f = "x_f"  # X moves, board is full, no winning happens
    o_n = "o_n"  # O moves, no winning happened, and board is not full
    o_w = "o_w"  # O moves and O wins
    o_f = "o_f"  # O moves, board is full, no winning happens


def board():
    return ((None, None, None), (None, None, None), (None, None, None))


def place(board, row: int, col: int, mark):
    if board[row][col] is not None:
        sys.exit(1)
    return tuple(
        tuple(mark if (r == row and c == col) else board[r][c] for c in range(3))
        for r in range(3)
    )


def has_space(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return True
    return False


def calc_input(board, player):
    winning_moves = {Player.X: Move.x_w, Player.O: Move.o_w}
    next_moves = {Player.X: Move.x_n, Player.O: Move.o_n}
    stalemates = {Player.X: Move.x_f, Player.O: Move.o_f}

    # Check rows
    for row in board:
        if row == (player, player, player):
            return winning_moves[player]

    # Check columns
    for i in range(3):
        if tuple(board[x][i] for x in range(3)) == (player, player, player):
            return winning_moves[player]

    # Check main diagonal (top-left to bottom-right)
    if tuple(board[i][i] for i in range(3)) == (player, player, player):
        return winning_moves[player]

    # Check anti-diagonal (top-right to bottom-left)
    if tuple(board[i][2 - i] for i in range(3)) == (player, player, player):
        return winning_moves[player]

    if not has_space(board):
        return stalemates[player]
    return next_moves[player]


def transition(curr_state, move):
    return {
        (State.X_turn, Move.x_n): State.O_turn,
        (State.O_turn, Move.o_n): State.X_turn,
        (State.X_turn, Move.x_f): State.Draw,
        (State.O_turn, Move.o_f): State.Draw,
        (State.X_turn, Move.x_w): State.X_win,
        (State.O_turn, Move.o_w): State.O_win,
    }.get((curr_state, move))


def print_board(board):
    for row in board:
        formatted_row = [cell.value if cell is not None else "." for cell in row]
        print(" ".join(formatted_row))
    print()


def play():
    game_board = board()
    current_state = State.X_turn

    print("Welcome to Tic-Tac-Toe!")
    print("Enter moves as 'row col' (0-2 for each)")
    print()

    while current_state not in [State.X_win, State.O_win, State.Draw]:
        print_board(game_board)

        # Determine current player
        current_player = Player.X if current_state == State.X_turn else Player.O
        print(f"{current_player.value}'s turn")

        # Get player input
        try:
            user_input = input("Enter your move (row col): ").strip()
            row, col = map(int, user_input.split())

            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid position. Use 0-2 for row and column.")
                continue

            if game_board[row][col] is not None:
                print("Position already taken. Try again.")
                continue

            # Make the move
            game_board = place(game_board, row, col, current_player)

            # Calculate the move result
            move = calc_input(game_board, current_player)

            # Transition to next state
            current_state = transition(current_state, move)

        except (ValueError, IndexError):
            print("Invalid input. Please enter two numbers (0-2) separated by a space.")
        except SystemExit:
            print("Error placing piece. Position might be taken.")

    # Game over - print final board and result
    print_board(game_board)

    if current_state == State.X_win:
        print("X wins!")
    elif current_state == State.O_win:
        print("O wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    play()
