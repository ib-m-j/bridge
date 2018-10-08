from cordes import CordeSets, profile
from arrayprint import ArrayPrinter
import numpy as np
import sys

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

    def simpleView(self):
        for r in self.rounds:
            print('a\n')
            line = ""
            for m in r:
                line = line + "{} {}:{} -- ".format(
                    m.getNS(), m.getEW(), m.getDealset())
            print(line)
    
class GeneratedHowell(Tournament):
    def __init__(self, name, roundGenerator, dealGenerator):
        Tournament.__init__(self, name)
        self.roundGenerator = roundGenerator
        self.dealGenerator = dealGenerator
        #print("round generator")
        #print(self.dealGenerator.graphic())
        #print("deal generator")
        #print(self.roundGenerator.graphic())
        self.nPairs = self.roundGenerator.universe + 1
        self.nTables = self.nPairs/2
        self.nDeals = self.nPairs - 1
        self.nRounds = self.nPairs - 1

        nDealSet = 0
        self.deals = {}
        for cSDeal in self.dealGenerator.rotateAll():
            for corde in cSDeal:
                self.deals[corde.normalized] = (nDealSet, corde.getDirection())
            self.deals[(cSDeal.unMatched()[0], self.nPairs - 1)] = (nDealSet, 1)
            
            nDealSet = nDealSet + 1
        #for d in sorted(self.deals.keys()):
        #    print(d, self.deals[d])

        #print(self.deals)
        self.matchups = {}
        
        r = 0
        for cS in self.roundGenerator.rotateAll():
            #print(self.roundGenerator.showCordeDirs())
            round = []
            for corde in cS:
                (dealNo, direction) = self.deals[corde.normalized]
                if direction == 0:
                    north = corde.normalized[0]
                    south = corde.normalized[1]
                else:
                    north = corde.normalized[1]
                    south = corde.normalized[0]
                    
                thisMatch = Match(north, south, dealNo)

                round.append(thisMatch)
                self.matchups[r, thisMatch.getNS()] = thisMatch.getEW()

            #print(cS.unMatched()[0], self.nPairs - 1,
            #      self.deals[
            #          cS.unMatched()[0], self.nPairs - 1])
            #below setting aelf.nPairs-1 NS
            #don't need to switch directions as we know details in this case
            thisMatch = Match(
                self.nPairs - 1, cS.unMatched()[0], 
                self.deals[(cS.unMatched()[0], self.nPairs - 1)][0])
            round.append(thisMatch)
            self.matchups[r, thisMatch.getNS()] = thisMatch.getEW()


            self.rounds.append(round)
            r = r+1

    def getNSSet(self, roundNo):
        res = []
        for m in self.rounds[roundNo]:
            res.append(m.getNS())

        return res
    
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
    def getAllHowellSeeds(self, nPairs):
        cSets = CordeSets(nPairs-1)
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
    allSeeds = GeneratedHowell.getAllHowellSeeds(8)
    print(len(allSeeds))

    #allseeds 12 and seedno 25 works nicely
    baseDealsGenerator = allSeeds[0][1]
    print("Deal generator:\n{}\n".format(baseDealsGenerator.showCordeDirs()))
          
    baseRoundsGenerator = allSeeds[0][0]
    print("Base round generator:\n{}\n".format(
        baseRoundsGenerator.showCordeDirs()))
    #print(allSeeds[0][1].showCordeDirs(),"\n")

    for dG in baseDealsGenerator.setAllDirections():
        print("Deal Genrator1:\n{}\n".format(dG.showCordeDirs()))
        T = GeneratedHowell("Noname", baseRoundsGenerator,
                            dG)
        print("NS set in round 0\n{}".format(T.getNSSet(0)))
        #for match in T.rounds[0]:
        #    NSs.append(match.getNS())
        #print(NSs)

        NSset = set([c.directed[0] for c in dG])
        #print("NS set in round generator\n{}".format(NSset))
        comparisons = T.getComparisons()
        (prVar, profileVal) = profile(dG.universe, NSset)
        if (np.var(list(comparisons.values())) == 0) or (prVar == 0):
            #print("\n\n",rG.showCordeDirs())
            print(ArrayPrinter(comparisons).print("comparisons"))
            print(profileVal)
            print(T.simpleView())
            print("aaaa")
    #print(T.simpleView())
    #print(ArrayPrinter(T.deals).print("pairId, dealid"))
    #print(ArrayPrinter(T.matchups).print("round no, NS plaers -> opponentId"))

    
if __name__ == '__main__':
    testTournament()
    #added comment
    #added more again comment
