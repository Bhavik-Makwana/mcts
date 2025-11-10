import random

class TicTacToe:
    def __init__(self, size=3):
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.size = size
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
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == ' ']

    def __str__(self):
        s = ''
        for row in self.board:
            s += '|'.join(row) + '\n'
            s += '-' * 5 + '\n'
        return s

    def check_win(self) -> int | None:
        players = ['X', 'O']
        for player in players:
            # Check rows
            for i in range(self.size):
                if all(self.board[i][j] == player for j in range(self.size)):
                    return 1 if player == 'X' else -1
            
            # Check columns
            for j in range(self.size):
                if all(self.board[i][j] == player for i in range(self.size)):
                    return 1 if player == 'X' else -1
            
            # Check main diagonal (top-left to bottom-right)
            if all(self.board[i][i] == player for i in range(self.size)):
                return 1 if player == 'X' else -1
            
            # Check anti-diagonal (top-right to bottom-left)
            if all(self.board[i][self.size - 1 - i] == player for i in range(self.size)):
                return 1 if player == 'X' else -1
        
        # Check if board is full (tie)
        if any(self.board[i][j] == ' ' for i in range(self.size) for j in range(self.size)):
            return None
        return 0

