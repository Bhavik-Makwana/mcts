import random
from mcts import MCTSNode
from tictactoe import TicTacToe
    
def mcts_search(board: TicTacToe, num_simulations: int):
    root_node = MCTSNode(None, None, board)
    for _ in range(num_simulations):
        node = root_node
        # while node is not a leaf node (not terminal )
        while not node.leaf_node():
            node = node.select()
        if node.untried_actions:
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
        result = game_board.check_win()
        if result and result != 0:
            game_board.switch_player()
            print("Player ", game_board.current_player, " wins!")
            print(game_board)
            return
        elif result == 0:
            game_board.switch_player()
            print("Draw!")
            print(game_board)
            return
        print(game_board)

play_game()