import random
import math
import copy

class MCTSNode:
    def __init__(self, parent, action, board: TicTacToe):
        self.parent = parent
        self.action = action # the action that led to this node
        self.board = board
        self.children = []
        self.visits = 0
        self.value = 0
        self.c = 2 # exploration constant
        
        self.untried_actions = self.board.get_valid_moves()

    def select(self):
        return max(self.children, key=lambda child: child.ucb_score())
    
    def expand(self):
        action = self.untried_actions.pop()
        new_board = copy.deepcopy(self.board)
        new_board.player_turn(action)
        node = MCTSNode(self, action, new_board)
        self.children.append(node)
        return node
                

    def ucb_score(self):
        if self.visits == 0:
            return float('inf')
        exploitation = self.value / self.visits
        exploration = self.c * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration

    def rollout(self, node: MCTSNode = None):
        node = self if node is None else node
        rollout_board = copy.deepcopy(node.board)
        while rollout_board.check_win() is None:
            action = random.choice(rollout_board.get_valid_moves())
            rollout_board.player_turn(action)
        absolute_result = rollout_board.check_win()
        if self.board.current_player == 'X':
            return -absolute_result
        else:
            return absolute_result

    def backpropagate(self, value):
        self.visits += 1
        self.value += value
        if self.parent:
            self.parent.backpropagate(-value)


    def is_leaf_node(self):
        def is_fully_expanded():
            return not self.untried_actions
        def is_terminal_node():
            return self.board.check_win() is not None
        # Whilst no more possible actions and the game is not over, the node is a leaf node
        return is_terminal_node() or not is_fully_expanded()
    

    def __str__(self, level=0):
        indent = "  " * level
        s = f"{indent}Value: {self.value}, Visits: {self.visits}\n"
        for child in self.children:
            s += child.__str__(level + 1)
        return s
class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        self.current_player = 'X'

    def simulate(self):
        while True:
            if self.check_win():
                return self.check_win()
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

def mcts_search(board: TicTacToe, num_simulations: int):
    root_node = MCTSNode(None, None, board)
    for _ in range(num_simulations):
        node = root_node
        # while node is not a leaf node (not terminal )
        while not node.is_leaf_node():
            node = node.select()
        if node.visits != 0 and node.untried_actions:
            node = node.expand()
        value = node.rollout()
        node.backpropagate(value)
    best_child = max(root_node.children, key=lambda child: child.visits)
    return best_child.action

def play_game():
    game_board = TicTacToe()
    while True:
        print("Current player: ", game_board.current_player)
        if game_board.current_player == 'X':
            action = mcts_search(game_board, 10000)
        else:
            action = random.choice(game_board.get_valid_moves())
        print("Best action: ", action)
        game_board.player_turn(action)
        if game_board.check_win() and game_board.check_win() != 0:
            game_board.switch_player()
            print("Player ", game_board.current_player, " wins!")
            print(game_board)
            return
        elif game_board.check_win() == 0:
            game_board.switch_player()
            print("Draw!")
            print(game_board)
            return
        print(game_board)

play_game()