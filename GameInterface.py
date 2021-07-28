import abc

class GameInterface( abc.ABC ):
    @abc.abstractclassmethod
    
    def generateBoard(self):
        pass

    def generateMoves(self):
        pass

    def is_finished(self):
        pass

    def __eq__(self, other):
        pass
    
    def __str__(self):
        pass
