import sys
import itertools
import numpy as np
import arrayprint

class Corde:
    def __init__(self, n, start, length):
        #this handles identification directeedcordes
        #n number of points around circle numbered counterclock wise
        #start number of one end of corde n in 0..n-1
        #length number of spaces skipped to the left of the corde 1..n-1
        #start point is start and end point is start + length mod n
        self.universe = n
        self.start = start
        self.length = length
        assert(start >= 0 and start < n), \
        "corde start value {} illegal".format(start)
        assert(length>=1 and length < n), \
        "corde length value {} illegal".format(length)
        #normalized numbers the two end points. normalized[0] < normalized[1]
        if self.start + self.length >= self.universe:
            self.normalized = (
                (self.start+self.length) % self.universe, self.start)
        else:
            self.normalized = (self.start, self.start + self.length)
        #print("corde")
        self.directed = (self.start, (self.start + self.length) % self.universe)
        
    def __eq__(self, other):
        res = (self.universe == other.universe)
        #print(res)
        res = res and ((
            self.start == other.start and self.length == other.length) or (
                self.start == (other.start + other.length) % self.universe) and (
                    self.length == self.universe - other.length))
        return res


    def __str__(self):
        return "Universe {}: start {}, length {}".format(
            self.universe, self.start, self.length)

    def graphic(self):
        res = ""
        res = res + (3*self.normalized[0] + 2)*" "
        res = res + ((self.normalized[1] - self.normalized[0])*3 + 1)*"."
        return res

    def rotate(self, r):
        assert 0<=r and r<self.universe, "rotation in Corde too high"
        if self.start + r >= self.universe:
            start = (self.start + r) % self.universe
        else:
            start = self.start + r
            
        return Corde(self.universe, start, self.length)
            
        
    def avoids(self, other):
        res = (self.universe == other.universe and 
               self.start != other.start and 
               self.start != (other.start + other.length) % self.universe and
               (self.start + self.length) % self.universe != other.start and
               (self.start + self.length) % self.universe != (
                   other.start + other.length) % self.universe )
        return res

    def getFlipped(self):
        return Corde(
            self.universe, self.start + self.length, 
            self.universe - self.length) 

    def flip(self):
        self.start = self.start + self.length
        self.length = self.universe - self.length
        return self

    def setDirection(self, dir):
        #dir = 0 first point around the clock is starting point
        #dir = 1 first point around the clock is ending point
        if self.start + self.length >= self.universe:
            if dir == 0:
                self.start = (self.start+self.length) % self.universe
                self.length = self.universe -  self.length
        else:
            if dir == 1:
                self.start = (self.start+self.length) % self.universe
                self.length = self.universe -  self.length

        self.directed = (self.start, (self.start + self.length) % self.universe)
                
    def getDirection(self):
        #see definition of direction in setDirection
        if self.start+ self.length >= self.universe:
            return 1
        return 0

    def getStartPoint(self):
        return self.start

    def getEndPoint(self):
        return (self.start + self.length) % self.universe

class DirectedCorde(Corde):
    #not used yet maybe never relevant
    def __eq__(self,  other):
        res = (self.universe == other.universe)
        print(res)
        res = res and (
            self.start == other.start and self.length == other.length) 
        return res

class CordeSet:
    def __init__(self, universe, cordes = []):
        self.universe = universe
        self.cordes = cordes

    def __str__(self):
        res =  "Cordeset: Size {}\n".format(self.universe)
        for c in self.cordes:
            res = res + "\tcorde: {}\n ".format(c)
        return res
    
    def showCordeDirs(self):
        res =  "Cordeset: Size {}\n".format(self.universe)
        for x in range(self.universe):
            res = res + "{:3d}".format(x)
        res = res + "\n"

        starters = {}
        enders = {}
        for n,c in enumerate(self.cordes):
            starters[c.start] = n
            enders[(c.start + c.length)%c.universe] = n

        for x in range(self.universe):
            if x in starters:
                res = res + "{:3d}".format(starters[x])
            else:
                res = res + "{:3}".format('')
        res = res + '\n'
        for x in range(self.universe):
            if x in enders:
                res = res + "{:3d}".format(enders[x])
            else:
                res = res + "{:3}".format('')

        return res
        
    def __iter__(self):
        for x in self.cordes:
            yield x
        
    def graphic(self):
        res = ""
        for x in range(self.universe):
            res = res + "{:3d}".format(x)
        res = res + "\n"

        for c in self.cordes:
            res = res + c.graphic() + "\n"

        return res
    
    def addCorde(self, corde):
        assert self.hasRoom(corde) , "corde already inserted"
        self.cordes.append(corde)
        return self

    def hasRoom(self, corde):
        for c in self.cordes:
            if not c.avoids(corde):
                return False
        return True   

    def clone(self):
        return CordeSet(self.universe, self.cordes[:])
    
    def overlap(self, other):
        overlap = 0
        for c1 in self.cordes:
            for c2 in other.cordes:
                if c1 == c2:
                    overlap = overlap + 1
        return overlap

    def rotateAll(self):
        for x in range(self.universe):
            yield self.rotate(x)
        
    def maxOverlap(self, other):
        resOverlap = 0
        resCordeSet = []
        for cSet in other.rotateAll():
            #print("testing", cSet)
            if self.overlap(cSet) > resOverlap:
                resOverlap = self.overlap(cSet)
                resCordeSet = cSet
                #print("found", resOverlap)
        assert resOverlap > 0, "overlap on incomplete sets"
        return(resOverlap, resCordeSet)    

    
    def isOrthogonal(self, other):
        if self.maxOverlap(other)[0] == 1:
            return True

    def rotate(self, r):
        assert 0<=r and r<self.universe, "rotate by too much"
        newCordes = [x.rotate(r) for x in self.cordes]
        return CordeSet(self.universe, newCordes)
    
    def unMatched(self):
        matched = []
        for x in self:
            matched.extend([x.normalized[0], x.normalized[1]])
        return list(set(range(self.universe))-set(matched))

    def setAllDirections(self):
        for selection in itertools.product(
                [0,1], repeat=len(self.cordes)):
            #print("\n", selection)
            for (dir, c) in zip(selection, self.cordes):
                c.setDirection(dir)
            #print(self.showCordeDirs())
            yield self

    def getAllEndPoints(self):
        res = []
        for c in self:
            res.append(c.getEndPoint())

        return res

    def getAllStartPoints(self):
        res = []
        for c in self:
            res.append(c.getStartPoint())

        return res
    
class CordeSets:        
    def __init__(self, n):
        self.universe = n
        self.setAllCordes()
        #print("allcordes")
        self.setAllExclusiveCordeSets()
        #print("allexcl")
        self.setAllCordeSizes()
        #print("allsizes")
        #only undirected
        #self.allExclusiveSets()


    def setAllCordes(self):
        self.allCordes = []
        for start in range(0,self.universe):
            for length in range(1, self.universe - start):
                self.allCordes.append(Corde(self.universe, start, length))
                #print(Corde(self.universe, start, length))
        
        return self.allCordes

    def setAllCordeSizes(self):
        #still normalized to 0.1 first
        self.allCordeSizes = []
        res = CordeSet(self.universe, [Corde(self.universe, 0,1)])
        maxLength = self.universe//2
        length = 2
        self.addNewSizeCorde(res, length, maxLength)
        return self.allCordeSizes

    def addNewSizeCorde(self, myRes, length, maxLength):
        #print("adding length", length)
        for x in range(2, self.universe):
            #print("testing corde", x, length)
            tester = Corde(self.universe, x, length)
            #print(myRes.graphic())
            if myRes.hasRoom(tester):
                if length == maxLength:
                    self.allCordeSizes.append(
                        myRes.clone().addCorde(tester).clone())
                    #print("found result\n")
                else:
                    self.addNewSizeCorde(
                        myRes.clone().addCorde(
                            tester).clone(), length + 1, maxLength)
            
                       
    
    def setAllExclusiveCordeSets(self):
        #standardised first corde is always 0.1
        self.allExclusiveCordeSets = []
        #all = self.allCordes

        #allTestCords = all[:]
        #for (start, cord) in enumerate(allTestCords):
        #    result = CordeSet(self.universe, [])
        #    newRes = self.addExclusiveCord(
        #self.exclusiveCords, result, allTestCords[start+1:][:])
        
        all = []
        startCorde = Corde(self.universe, 0,1)
        for x in  self.allCordes :
            if x != startCorde:
                all.append(x)
        result = CordeSet(self.universe, [startCorde])
        allTestCords = all[:]
        newRes = self.addExclusiveCord(
            self.allExclusiveCordeSets, result, allTestCords[:])
        return self.allExclusiveCordeSets
    
        #result = CordeSet(self.universe, [])
        #newRes = self.addExclusiveCord(
        #    self.allExclusiveCordeSets, result, allTestCords[:])
        #return self.allExclusiveCordeSets
        

        
    def addExclusiveCord(self, allResults, result, remainingCords):
        myInputResult = result.clone()
        #print("Setting inoput to:", myInputResult)
        if len(result.cordes) >= self.universe // 2:
            allResults.append(result)
            #print("found ", result)
            return True
        else:
            for (current, cord) in enumerate(remainingCords):
                #print("Working on", cord, len(remainingCords))
                #print("My input")
                #print(myInputResult)
                #print(  result.hasRoom(cord))
                #if cord.start == 2:
                #    sys.exit(0)
                if myInputResult.hasRoom(cord):
                    testResult = myInputResult.clone().addCorde(cord)
                    #if not(self.addExclusiveCord(allResults,
                    #    result, remainingCords[current+1:][:])):
                    #    break
                    self.addExclusiveCord(
                        allResults, testResult, remainingCords[current+1:][:])
            return None

    def allOrthogonal(self, selectedSet):
        for cSet in self.allExclusiveCordeSets:
            #print("testing ", cSet)
            if selectedSet.isOrthogonal(cSet):
                yield cSet 
        

    def getAllOrthogonalPairs(self, n):
        cSets = CordeSets(n)
        res = cSets.allCordeSizes
        orthogonal = []
        for (n,cS1) in enumerate(res):
            for cS2 in res[n:]:
                if cS1.maxOverlap(cS2)[0] == 1:
                    orthogonal.append((cS1, cS2))
        return orthogonal
    
        
            
def simpletest1():
    C1 = Corde(5,1,2)
    C2 = Corde(5,4,1)
    print(C1)
    print("Equal?", C1 == C2)

    dC = DirectedCorde(5,1,2)
    print (dC.__dir__)
    dC1 = DirectedCorde(5,3,3)
    dC2 = DirectedCorde(5,1,2)
    print("Equal {} and {}? : {}".format(dC,dC2, dC == dC1))
    print("Equal {} and {}? : {}".format(dC,dC2,dC == dC2))
    
    C3 = Corde(5,4,4)
    print("avoids", C1,C3, C1.avoids(C3))

def simpletest2():
    cS = CordeSet(5)
    cS.addCorde( Corde(5,1,2))
    cS.addCorde( Corde(5,4,3))
    print(cS)
    print(cS.graphic())
    
def fillSet():

    cS = CordeSets(7)
    #for c in cS.allCordes():
    #    print(c)
    res = cS.allExclusiveCordeSets
    for x in res:
        print(x.graphic())
        print(cS.allExclusiveCordeSets[0].overlap(x),"\n\n")

    #print("starting rotation")
    #firstSet = res[0]
    #for n in range(firstSet.universe):
    #    print("rotate by ",n)
    #print(firstSet.rotate(n).graphic())

    print("starting rotatetall")
    for x in res[0].rotateAll():
        print(x.graphic())

    print("starting maxoverlap")
    print(res[0].graphic())
    print("\n")
    for c in res[1:]:
        print(c.graphic())
        maxOverlapCSet= res[0].maxOverlap(c)[1]
        print(maxOverlapCSet.graphic())
        print(res[0].overlap(maxOverlapCSet))

    print("starting allorthogonal")
    print(res[5].graphic())
    for c in cS.allOrthogonal(res[5]):
        print(c.graphic())

def testAllSizes():
    cSets = CordeSets(9)
    res = cSets.allCordeSizes
    overlaps = []
    for cS1 in res:
        overlapLine = []
        overlaps.append(overlapLine)
        print(cS1.graphic())
        for cS2 in res:
            overlapLine.append(cS1.maxOverlap(cS2)[0])
    
    for l in overlaps:
        line = ""
        for res in l:
            line = line + "\t{}".format(res)
        print(line)

def testUnmatched():
    cSets = CordeSets(9)
    res = cSets.allCordeSizes
    print(res[0].graphic())
    for x in res[0]:
        print(x)
    print(res[0].unMatched())

def testFlip():
    cSs = CordeSets(7)
    res = cSs.allCordeSizes
    for cordeSet in res[:1]:
        print(cordeSet.graphic())
        for corde in cordeSet:
            corde.flip()
        print(cordeSet.showCordeDirs())

    for corde in cordeSet:
        corde.setDirection(0)

    print(cordeSet.showCordeDirs())

    for corde in cordeSet:
        corde.setDirection(1)

    print(cordeSet.showCordeDirs())

    print("starting all dirs")
    cordeSet.setAllDirections()
    
    
def testAllDirections():
    cSs = CordeSets(7)
    res = cSs.allCordeSizes
    for cS in res[:1]:
        print(cS.graphic())
        for x in cS.setAllDirections():
            print(x.showCordeDirs())


def profile(universe, startSet):
    #for a set of numbers in 0..universe-1
    #look at all cordelengths and check number of
    #cordes that span from the set to the complementary set
    #and cordes that do not
    #if the profile is very flat we have a candidate for
    #a Howell round generator that will give a balanced tournament
    #first value for each cordelength is number of NoSpanning cordes
    profile = []
    compSet = set([x for x in range(universe)])-startSet
    for length in range(1,universe):
        start = Corde(universe, 0, length)
        span = 0
        noSpan = 0
        for x in range(universe):
            tester = start.rotate(x)
            if (
                (tester.normalized[0] in startSet and
                 tester.normalized[1] in startSet) or
                (tester.normalized[0] in compSet and
                 tester.normalized[1] in compSet)):
                noSpan += 1
            else:
                span +=1
                
        profile.append((noSpan, span))
    #print(startSet)
    #print(compSet)
    #print(profile)
    profileVar = [x for (x,y) in profile]
    return (np.var(profileVar), profile)

def fullTest(n):
    print("Full test for n=",n)
    cSets = CordeSets(n)
    allLines = cSets.allCordeSizes

    count = 0
    for line in allLines:
        print('\nLine no: {}\n{}'.format(
            count, line.graphic()))
        count +=1


    overlaps = []
    for cS1 in allLines:
        overlapLine = []
        overlaps.append(overlapLine)
        for cS2 in allLines:
            overlapLine.append(cS1.maxOverlap(cS2)[0])

    print(arrayprint.ArrayPrinter.arrayPrinterFromLists(overlaps).print(
        "Overlaps between lines:\n"))
            

    print("\nOrthogonal line pairs:\n")
    orthogonals = []
    for rowNo in range(len(overlaps)):
        for colNo in range(rowNo, len(overlaps[rowNo])):
            if overlaps[rowNo][colNo] == 1:
                orthogonals.append((rowNo, colNo))

    res = ""
    for x in orthogonals:
        res = res + "({},{}) ".format(x[0], x[1])
    print(res)


    #below probably only works for n = 9
    ##############################################
    print("\nProfiles for one line no {}:\n".format(orthogonals[0][1]))
    tester = allLines[orthogonals[0][1]]
    #we need sum ofnospan and span in profile to be constat = 8 for n=9
    #below we start ot by restricting the small no span to be 3
    #and the large nospan to be 5. This should reduce numbver of trials in
    #the loop as we know sum will be 8 for cordlength 1
    cordeLengthOneSameSmall = []
    cordeLengthOneSameLarge = []
    for testerWithDir in tester.setAllDirections():
        #print(testerWithDir.showCordeDirs())
        #print(testerWithDir.getAllEndPoints())
        endPoints = testerWithDir.getAllEndPoints()
        theProfile = profile(tester.universe, set(endPoints))[1]
        if theProfile[0][0] == 3:
            cordeLengthOneSameSmall.append(
                (set(endPoints), [x for (x,y) in theProfile]))
        if theProfile[0][0] == 5:
            cordeLengthOneSameLarge.append(
                (set(endPoints), [x for (x,y) in theProfile]))

    print("\nAll small length one profile:\n")
    for x in cordeLengthOneSameSmall:
        print(x)
        
    print("\nAll large length one profile:\n")
    for x in cordeLengthOneSameLarge:
        print(x)
        

    print("Balanced pairs\n")
    balanced = []
    for seta, a in cordeLengthOneSameSmall:
        for setb, b in cordeLengthOneSameLarge:
            res = True
            for x,y in zip(a,b):
                if x + y != 8:
                    res = None
                    break
            if res:
                print(seta, setb)
                print(a,b)
                


                
if __name__ == '__main__':
    
    #simpletest2()
    #fillSet()
    #testAllSizes()
    #testUnmatched()
    #testFlip()
    #testAllDirections()
    #res = profile(7, set([1,2,3]))
    #print(res)
    fullTest(9)
