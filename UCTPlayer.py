from BTree import BTree
from PlayerInterface import PlayerInterface
from UCT import UCT
import time

class UCTPlayer(PlayerInterface):

    def __init__(self, game, iter=100, choose='max_value', heurs=False):
        self.iter = iter
        self.choose = choose
        self.uct = UCT(game)
        self.heurs = heurs

    def chooseMove(self, enemy_move):
        """Choosen a move according to the chosen strategy
        """
        start = time.time()

        #Update according to the enemy move
        if not(enemy_move.black_tiles == self.uct.tree.game.black_tiles and enemy_move.white_tiles == self.uct.tree.game.white_tiles):
            if not self.uct.tree.nodes:
                self.uct.tree = BTree(game=enemy_move, parent=None)
            else:
                find = False
                i = 0
                while(not find):
                    if (enemy_move.black_tiles == self.uct.tree.nodes[i].game.black_tiles and enemy_move.white_tiles == self.uct.tree.nodes[i].game.white_tiles):
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
            best_node = self.uct.tree.nodes[0]
            for node in self.uct.tree.nodes:
                value = UCT.UCB1(node)
                if value > best_value:
                    best_node = node
                    best_value = value
        elif self.choose == 'most_visited':
            best_visits = self.uct.tree.nodes[0].visits
            best_node = self.uct.tree.nodes[0]
            for node in self.uct.tree.nodes:
                if node.visits > best_visits:
                    best_node = node
                    best_visits = node.visits

        self.uct.tree = best_node
        self.uct.tree.parent = None

        end = time.time()
        print(f'Tiempo: {end - start}')

        return self.uct.tree.game
        
        