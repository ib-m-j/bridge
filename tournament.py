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
        self.nPairs = 0
        self.nTables = 0
        self.nDeals = 0
        self.nRounds = 0
        
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
        
    def __matrix__(self, tab = 3):
        table = {}
        tableRounds = {}
        for n,r in enumerate(self.rounds):
            for m in r:
                table[(m.NSpair,m.EWpair)] = m.dealset
                tableRounds[(m.NSpair,m.EWpair)] = n

        res = "Tournament: {} - by deals\n".format(self.name)
        for r in range(self.nRounds):
            line = ""
            for p in range(self.nPairs):
                if (r,p) in table:
                    line = line + "{:3}".format(table[r,p])
                else:
                    line = line + "{:3}".format("")
            res = res + line + "\n"

        res = res + "Tournament: {} - by rounds\n".format(self.name)
        for r in range(self.nRounds):
            line = ""
            for p in range(self.nPairs):
                if (r,p) in tableRounds:
                    line = line + "{:3}".format(tableRounds[r,p])
                else:
                    line = line + "{:3}".format("")
            res = res + line + "\n"
        return res
        


class GeneratedHowell(Tournament):
    def __init__(self, name, nPairs, nRounds = 0, nDeals = 0):
        Tournament.__init__(self, name)
        seeds = self.getAllHowellSeeds(nPairs - 1)
        self.roundGenerator = seeds[0][0]
        self.dealGenerator = seeds[0][1]
        self.nPairs = nPairs
        self.nTables = self.nPairs/2
        self.nDeals = nPairs - 1
        self.nRounds = nPairs - 1
        assert nPairs == self.roundGenerator.universe + 1, "mismatch in nPairs"

        nDealSet = 0
        deals = {}
        for cSDeal in self.dealGenerator.rotateAll():
            for corde in cSDeal:
                deals[corde.normalized] = nDealSet
            deals[(cSDeal.unMatched()[0], self.nPairs - 1)] = nDealSet 
            nDealSet = nDealSet + 1
        for d in sorted(deals.keys()):
            print(d, deals[d])

        for cS in self.roundGenerator.rotateAll():
            round = []
            for corde in cS:
                round.append(Match(
                    corde.normalized[0], corde.normalized[1], 
                    deals[corde.normalized]))
            print(cS.unMatched()[0], self.nPairs - 1, deals[
                cS.unMatched()[0], self.nPairs - 1])
            round.append(Match(
                cS.unMatched()[0], self.nPairs - 1,
                deals[(cS.unMatched()[0], self.nPairs - 1)]))

            self.rounds.append(round)
                

    @classmethod
    def getAllHowellSeeds(self, n):
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
    T = GeneratedHowell("Noname", 12)
    print(T.__matrix__())

if __name__ == '__main__':
    testTournament()
    #added comment
    #added more again comment
