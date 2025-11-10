import random

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        self.current_player = 'X'

    def simulate(self):
        while self.check_win() is None:
            action = random.choice(self.get_valid_moves())
            self.player_turn(action)
        return self.check_win()

    # tictactoe for mcts
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def player_turn(self, action):
        self.board[action[0]][action[1]] = self.current_player
        self.switch_player()

    def get_valid_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def __str__(self):
        s = ''
        for row in self.board:
            s += '|'.join(row) + '\n'
            s += '-' * 5 + '\n'
        return s

    def check_win(self) -> int | None:
        players = ['X', 'O']
        for player in players:
            for i in range(3):
                if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                    return 1 if player == 'X' else -1
                if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                    return 1 if player == 'X' else -1
            if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
                return 1 if player == 'X' else -1
            if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
                return 1 if player == 'X' else -1
        if any(self.board[i][j] == ' ' for i in range(3) for j in range(3)):
            return None
        return 0

