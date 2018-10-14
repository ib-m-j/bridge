import numpy as np
from tournament import Tournament, Match
from arrayprint import ArrayPrinter

class ManComparisons(Tournament):
    #this class does not handle rounds everything in one round
    def __init__(self, name, dealsDefinition):
        #dealsDefinition: list of dealsets (no external ID)
        #each dealset list of  matches in format
        # (NSpair, EWPair)
        Tournament.__init__(self, name)
        dealsetID = 0
        onlyRound = []
        deals = {}
        self.rounds = [onlyRound]
        self.Nrounds = 1
        self.nPairs = 0
        #assuming pairs numbered 1..nPairs
        for dealset in dealsDefinition:
            for m in dealset:
                a = m[0] 
                b = m[1]
                if a>self.nPairs:
                    self.nPairs = a
                if b>self.nPairs:
                    self.nPairs = b
                onlyRound.append(Match(a-1, b-1, dealsetID))
            dealsetID +=1


def findComparisons():
    definition = [
            [(1,3), (4,7), (6,2), (9,8), (10,5)],
            [(1,4), (3,8), (6,5), (7,9), (10,2)],
            [(2,5), (4,9), (7,6), (8,1), (10,3)],
            [(3,6), (5,1), (8,7), (9,2), (10,4)],
            [(2,7), (5,4), (6,8), (9,3), (10,1)],
            [(1,9), (2,4), (5,8), (7,3), (10,6)],
            [(2,1), (3,5), (6,9), (8,4), (10,7)],
            [(3,2), (4,6), (7,1), (9,5), (10,8)],
            [(1,6), (4,3), (5,7), (8,2), (10,9)]
            ]

    T = ManComparisons("noname", definition)
    comparisons = T.getComparisons()
    print(ArrayPrinter(comparisons).print("comparisons"))

            
if __name__ == '__main__':
    findComparisons()
