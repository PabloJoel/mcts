import random
from TicUCT import TicUCT
from BTree import BTree
from PlayerInterface import PlayerInterface
from UCT import UCT
from TicUCT import TicUCT
import time

class UCTPlayer(PlayerInterface):

    def __init__(self, player, game, type_game='checkers', iter=100, choose='max_value', heurs=False):
        self.player = player
        self.iter = iter
        self.choose = choose
        if type_game == 'checkers':
            self.uct = UCT(game,player)
        elif type_game == 'tic':
            self.uct = TicUCT(game)
        self.heurs = heurs

    def chooseMove(self, enemy_move):
        """Choosen a move according to the chosen strategy
        """
        start = time.time()

        #Update according to the enemy move
        if not(enemy_move.same_board(self.uct.tree.game)):
            if not self.uct.tree.nodes:
                self.uct.tree = BTree(game=enemy_move, parent=None)
            else:
                find = False
                i = 0
                while(not find):
                    if (enemy_move.same_board(self.uct.tree.nodes[i].game)):
                        self.uct.tree = self.uct.tree.nodes[i]
                        self.uct.tree.parent = None
                        find = True
                    else:
                        i += 1

        #Iterate
        self.uct.tree = self.uct.search(self.heurs, self.iter)

        #Choose new move
        if self.choose == 'max_value':
            best_value = UCT.UCB1(self.uct.tree.nodes[0])
            best_nodes = list()
            best_nodes.append(self.uct.tree.nodes[0])

            for node in self.uct.tree.nodes:
                value = UCT.UCB1(node)
                if value == best_value:
                    best_nodes.append(node)
                elif value > best_value:
                    best_nodes = list()
                    best_nodes.append(node)
                    best_value = value
        elif self.choose == 'most_visited':
            best_visits = self.uct.tree.nodes[0].visits
            best_nodes = list()
            best_nodes.append(self.uct.tree.nodes[0])

            for node in self.uct.tree.nodes:
                if node.visits == best_visits:
                    best_nodes.append(node)
                elif node.visits > best_visits:
                    best_node = list()
                    best_node.append(node)
                    best_visits = node.visits

        chosen = random.randint(0,len(best_nodes)-1)
        self.uct.tree = best_nodes[chosen]
        self.uct.tree.parent = None

        end = time.time()
        print(f'Tiempo: {end - start}')

        return self.uct.tree.game
        
        