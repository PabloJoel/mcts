#Utils
import random
import copy
import numpy as np

#Tree
from BTree import BTree

class UCT():

    def __init__(self, game):
        self.tree = BTree(game=game, parent=None)
        
    def search(self, heurs, max_iter=100):
        tree = copy.deepcopy(self.tree)

        #Initialize tree
        movs = tree.game.generateMoves()
        for new_game in movs:
            tree.nodes.append(BTree(game=new_game, parent=tree))

        if len(movs)==1:
            return tree

        for node in tree.nodes:
            finish, winner = node.game.is_finished()
            if finish and winner == tree.game.next_player: #Winning move
                new_nodes = list()
                new_nodes.append(node)
                tree.nodes = new_nodes
                return tree
            elif finish and winner != 0: #Losing move
                node.value = float('-inf')

        iter = 0
        while(iter < max_iter):
            selected_node = UCT.selection(tree)
            sim_value = UCT.simulation(selected_node, heurs)
            UCT.backpropagation(selected_node, sim_value)
            iter += 1

        return tree

    def selection(node):
        if node.game.is_finished()[0]:
            return node
        else:
            if not node.nodes: #Leaf node
                if node.visits > 0: #Already visited
                    #Expand
                    movs = node.game.generateMoves()
                    for new_game in movs:
                        node.nodes.append(BTree(game=new_game, parent=node))
                    
                    chosen = random.randint(0,len(node.nodes)-1)
                    return node.nodes[chosen]
                else: #Non visited node
                    return node
            else: #Non leaf node
                best_nodes = list() 
                best_nodes.append(node.nodes[0])

                best_ucb = UCT.UCB1(node.nodes[0])
                for subnode in node.nodes[1:]:
                    ucb = UCT.UCB1(subnode)
                    if ucb == best_ucb:
                        best_nodes.append(subnode)
                    elif ucb > best_ucb:
                        best_nodes = list()
                        best_nodes.append(subnode)
                        best_ucb = ucb
                chosen = random.randint(0,len(best_nodes)-1)
                return UCT.selection(best_nodes[chosen])

    def simulation(node, heurs): 
        winner = UCT.__play(node.game,heurs)
        return winner

    def __play(game, heurs):
        current_game = copy.deepcopy(game)
        turn1 = current_game.next_player
        all_moves = dict()

        while(True): 
            if turn1:
                player_color = 'Black'
            else:
                player_color = 'White'

            moves = current_game.generateMoves()
            if not moves:
                if player_color == 'Black':
                    return 'White'
                else:
                    return 'Black'
            else:
                if heurs:
                    chosen = list()
                    chosen.append(0)
                    best_heuristic_value = moves[0].heuristic_eval()
                    for i,game in enumerate(moves[1:]):
                        new_heurs = game.heuristic_eval()
                        if new_heurs > best_heuristic_value:
                            best_heuristic_value = new_heurs
                            chosen.clear()
                            chosen.append(i)
                        elif new_heurs == best_heuristic_value:
                            chosen.append(i)
                    index = random.randint(0, len(chosen)-1)
                    chosen = chosen[index]
                else:
                    chosen = random.randint(0, len(moves)-1)
                current_game = moves[chosen]

                #Repeat position
                if current_game in all_moves:
                    all_moves[current_game] += 1
                else:
                    all_moves.update({current_game:1})

                # Draw because of definition 1.32.1
                if all_moves[current_game] > 2:
                    return 'Draw'

                # Draw because of definition 1.32.2
                if current_game.cond1 > 40 and current_game.cond2 > 40:
                    return 'Draw'
                turn1 = current_game.next_player

    def backpropagation(node, value):
        node.visits += 1
        if value == 'Black' and node.game.next_player == False:
            node.value += 1
        elif value == 'White'  and node.game.next_player == True:
            node.value += 1
        elif value == 'Draw':
            node.value += 0.25

        #node.value += value
        if node.parent is not None:
            UCT.backpropagation(node.parent, value)

    def UCB1(node, expl_const=(1/(np.sqrt(2)))):
        """Basic UCB1 function
        """
        if node.visits == 0:
            return float('inf')
        else:
            exploitation = (node.value/node.visits)

            inside_square_root = (2*(np.log(node.parent.visits)))/node.visits 
            exploration  = 2*expl_const*(np.sqrt(inside_square_root))

            return (exploitation + exploration)
