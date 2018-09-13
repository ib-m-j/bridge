from cordes import CordeSets

class Match:
    def __init__(self, NSpair, EWpair, dealset):
        self.NSpair =  NSpair
        self.EWpair = EWpair
        self.dealset = dealset

    def __str__(self):
        return "({}, {}, {})".format(
            self.NSpair, self.EWpair, self.dealset)

    def __verbose__(self):
        return "NS: {}, EW: {}, Dealset: {}".format(
            self.NSpair, self.EWpair, self.dealset)

class Tournament:
    def __init__(self, name = "Noname"):
        #pairs 1..p
        #rounds 1..r
        #each round consists a of list of matches (at most p/2)
        #dealsets 1..d each dealset consists of  dealsPrSet deals
        self.name = name
        self.rounds = []
        
    def __str__(self):
        res = "Tournament: {}".format(self.name)
        for (n,round) in enumerate(self.rounds):
            res = res + "\nRound {}: ".format(n)
            for match in round:
                res = res + "{}, ".format(match)
            res = res[:-2]
        res = res+"\n"
        return res

    def __verbose__(self):
        res = "Tournament: {}".format(self.name)
        for (n,round) in enumerate(self.rounds):
            res = res + "\nRound {}: ".format(n)
            for match in round:
                res = res + "{},".format(match)
            res = res[:-1]
        res = res+"\n"
        return res

class GeneratedHowell(Tournament):
    def __init__(self, name, roundGenerator, dealGenerator):
        self.roundGenerator = roundGenerator
        self.dealGenerator = dealGenerator
        Tournament.__init__(self, name)
        self.nRounds = roundGenerator.universe + 2
        self.nDeals = dealGenerator.universe + 2
        assert self.nRounds == self.nDeals, "pairs and deals do not match"
        nDealSet = 0
        deals = {}
        for cSDeal in self.dealGenerator.rotateAll():
            for corde in cSDeal:
                deals[corde.normalized] = nDealSet
            deals[(cSDeal.unMatched()[0], cSDeal.universe + 1)] = nDealSet 
            nDealSet = nDealSet + 1
        print(deals)

        for cS in self.roundGenerator.rotateAll():
            round = []
            for corde in cS:
                round.append(Match(
                    corde.normalized[0], corde.normalized[1], 
                    deals[corde.normalized]))
            round.append(Match(
                cSDeal.unMatched()[0], cSDeal.universe + 1,
                deals[corde.normalized]))

            self.rounds.append(round)
                

    @classmethod
    def getAllSeedPairs(n):
        cSets = CordeSets(n)
        res = cSets.allCordeSizes
        orthogonal = []
        for (n,cS1) in enumerate(res):
            for cS2 in res[n:]:
                if cS1.maxOverlap(cS2)[0] == 1:
                    orthogonal.append((cS1, cS2))
        return orthogonal
    


def testTournament():
    #for pair in orthogonal:
    #    print(pair[0].graphic())
    #    print(pair[1].graphic())
    #    print("--------------------\n")
    orthogonal = GeneratedHowell.getAllSeedPairs()
    T = GeneratedHowell("Noname", orthogonal[0][0], orthogonal[0][1])
    print(T)

if __name__ == '__main__':
    testTournament()
    #added comment
