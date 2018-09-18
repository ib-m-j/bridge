from cordes import CordeSets
from arrayprint import ArrayPrinter

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

    def getNS(self):
        return self.NSpair
    
    def getEW(self):
        return self.EWpair

    def getDealset(self):
        return self.dealset
    
class Tournament:
    def __init__(self, name = "Noname"):
        #pairs 1..p
        #rounds 1..r
        #each round consists a of list of matches (at most p/2)
        #dealsets 1..d each dealset consists of  dealsPrSet deals
        self.name = name
        self.rounds = []
        self.deals = {}
        #deals as dictionary assumes no ghost players
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
    def __init__(self, seedNo, name, nPairs, nRounds = 0, nDeals = 0):
        Tournament.__init__(self, name)
        seeds = self.getAllHowellSeeds(nPairs - 1)
        print("NoodfSeeds: ", len(seeds))
        self.roundGenerator = seeds[seedNo][0]
        self.dealGenerator = seeds[seedNo][1]
        print("round generator")
        print(self.dealGenerator.graphic())
        print("deal generator")
        print(self.roundGenerator.graphic())
        self.nPairs = nPairs
        self.nTables = self.nPairs/2
        self.nDeals = nPairs - 1
        self.nRounds = nPairs - 1
        assert nPairs == self.roundGenerator.universe + 1, "mismatch in nPairs"

        nDealSet = 0
        self.deals = {}
        for cSDeal in self.dealGenerator.rotateAll():
            for corde in cSDeal:
                self.deals[corde.normalized] = nDealSet
            self.deals[(cSDeal.unMatched()[0], self.nPairs - 1)] = nDealSet 
            nDealSet = nDealSet + 1
        #for d in sorted(self.deals.keys()):
        #    print(d, self.deals[d])

        #print(self.deals)
        self.matchups = {}
        
        r = 0
        for cS in self.roundGenerator.rotateAll():
            round = []
            for corde in cS:
                thisMatch = Match(
                    corde.directed[0], corde.directed[1], 
                    self.deals[corde.normalized])
                round.append(thisMatch)
                self.matchups[r, thisMatch.getNS()] = thisMatch.getEW()
            #print(cS.unMatched()[0], self.nPairs - 1,
            #      self.deals[
            #          cS.unMatched()[0], self.nPairs - 1])
            thisMatch = Match(
                self.nPairs - 1, cS.unMatched()[0], 
                self.deals[(cS.unMatched()[0], self.nPairs - 1)])
            round.append(thisMatch)
            self.matchups[r, thisMatch.getNS()] = thisMatch.getEW()
                
            self.rounds.append(round)
            r = r+1


    def getComparisons(self):
        deals = {}
        for round in self.rounds:
            for match in round:
                if match.getDealset() in deals:
                    deals[match.getDealset()].append(
                        (match.getNS(), match.getEW()))
                else:
                    deals[match.getDealset()] =  [
                        (match.getNS(), match.getEW())]
                    

        comparisons = {}
        for r in range(self.nPairs):
            for c in range(self.nPairs):
                if r != c:
                    comparisons[(r,c)] = 0
        #print(deals)
        for d, encounters in deals.items():
            #print(encounters)
            for n, encounter in enumerate(encounters):
                #print(n, encounter)
                ns = encounter[0]
                ew = encounter[1]
                comparisons[(ns, ew)] = comparisons[(ns,ew)] + self.nPairs - 1
                comparisons[(ew, ns)] = comparisons[(ew,ns)] + self.nPairs - 1
                for eOther in encounters[n+1:]:
                    otherNS = eOther[0]
                    otherEW = eOther[1]
                    comparisons[(ns, otherNS)] = comparisons[(ns, otherNS)] + 1
                    comparisons[(ns, otherEW)] = comparisons[(ns, otherEW)] - 1
                    comparisons[(ew, otherNS)] = comparisons[(ew, otherNS)] - 1
                    comparisons[(ew, otherEW)] = comparisons[(ew, otherEW)] + 1
                
                    comparisons[(otherNS, ns)] = comparisons[(otherNS, ns)] + 1
                    comparisons[(otherEW, ns)] = comparisons[(otherEW, ns)] - 1
                    comparisons[(otherNS, ew)] = comparisons[(otherNS, ew)] - 1
                    comparisons[(otherEW, ew)] = comparisons[(otherEW, ew)] + 1
        return comparisons
                    
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
    print("\n\nStarting seednO ", 25)
    T = GeneratedHowell(25, "Noname", 12)
    #print(T.__matrix__())
    #print(ArrayPrinter(T.deals).print("pairId, dealid"))
    #print(ArrayPrinter(T.matchups).print("round no, NS plaers -> opponentId"))

    print(ArrayPrinter(T.getComparisons()).print("comparisons"))
    
if __name__ == '__main__':
    testTournament()
    #added comment
    #added more again comment
