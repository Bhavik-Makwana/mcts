import math
import copy
from tictactoe import TicTacToe

class MCTSNode:
    def __init__(self, parent, action, board: TicTacToe):
        self.parent = parent
        self.action = action # the action that led to this node
        self.board = board
        self.children = []
        self.visits = 0
        self.value = 0
        self.c = math.sqrt(2) # exploration constant
        
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

    def rollout(self):
        rollout_board = copy.deepcopy(self.board)
        absolute_result = rollout_board.simulate()
        if self.board.current_player == 'X':
            return -absolute_result
        else:
            return absolute_result

    def backpropagate(self, value):
        self.visits += 1
        self.value += value
        if self.parent:
            self.parent.backpropagate(-value)


    def leaf_node(self):
        def is_fully_expanded():
            return not self.untried_actions
        def is_terminal_node():
            return self.board.check_win() is not None
        return is_terminal_node() or self.untried_actions
    

    def __str__(self, level=0):
        indent = "  " * level
        s = f"{indent}Value: {self.value}, Visits: {self.visits}\n"
        for child in self.children:
            s += child.__str__(level + 1)
        return s