import numpy as np
from tournament import Tournament, Match
from arrayprint import ArrayPrinter, DictArray

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


def findComparisons(name, definition):
#    definition = [
#            [(1,3), (4,7), (6,2), (9,8), (10,5)],
#            [(1,4), (3,8), (6,5), (7,9), (10,2)],
#            [(2,5), (4,9), (7,6), (8,1), (10,3)],
#            [(3,6), (5,1), (8,7), (9,2), (10,4)],
#            [(2,7), (5,4), (6,8), (9,3), (10,1)],
#            [(1,9), (2,4), (5,8), (7,3), (10,6)],
#            [(2,1), (3,5), (6,9), (8,4), (10,7)],
#            [(3,2), (4,6), (7,1), (9,5), (10,8)],
#            [(1,6), (4,3), (5,7), (8,2), (10,9)]
#            ]

    T = ManComparisons(name, definition)
    comparisons = T.getComparisons()
    return comparisons
    #print("\n",name)
    #print(ArrayPrinter(comparisons).print("comparisons"))

            
if __name__ == '__main__':
    tournamentOctober1 = [
        [(3,6), (4,2), (5,9), (7,8), (10,1)],
        [(4,7), (5,3), (6,1), (8,9), (10,2)],
        [(5,8), (6,4), (7,2), (9,1), (10,3)],
        [(1,2), (6,9), (7,5), (8,3), (10,4)],
        [(2,3), (7,1), (8,6), (9,4), (10,5)],
        [(1,5), (3,4), (8,2), (9,7), (10,6)],
        [(1,8), (2,6), (4,5), (9,3), (10,7)],
        [(1,4), (2,9), (3,7), (5,6), (10,8)],
        [(2,5), (3,1), (4,8), (6,7), (10,9)]
    ]

    tournamentOctober8 = [
        [(2,7), (5,4), (6,8), (9,3), (10,1)],
        [(1,4), (3,8), (6,5), (7,9), (10,2)],
        [(2,5), (4,9), (7,6), (8,1), (10,3)],
        [(3,6), (5,1), (8,7), (9,2), (10,4)],
        [(1,3), (4,7), (6,2), (9,8), (10,5)],
        [(1,9), (2,4), (5,8), (7,3), (10,6)],
        [(2,1), (3,5), (6,9), (8,4), (10,7)],
        [(3,2), (4,6), (7,1), (9,5), (10,8)],
        [(1,6), (4,3), (5,7), (8,2), (10,9)]
        ]
    
    comparisons1 = DictArray(findComparisons("October1", tournamentOctober1))
    comparisons2 = DictArray(findComparisons("October8", tournamentOctober8))

    print(ArrayPrinter(comparisons1).print("\nOvtober1"))
    print(ArrayPrinter(comparisons2).print("\nOvtober8"))
    print(ArrayPrinter(comparisons1 + comparisons2).print("\ntogether"))
