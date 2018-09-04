import sys

class Corde:
    def __init__(self, n, start, length):
        #n number of points around circle numbered counterclock wise
        #start number of one end of corde n in 0..n-1
        #length number of spaces skipped to the left of the corde 1..n-1
        #i.e. end point is start + length mod n
        self.universe = n
        self.start = start
        self.length = length
        assert(start >= 0 and start < n), "corde start value {} illegal".format(start)
        assert(length>=1 and length < n), "corde length value {} illegal".format(length)
        #normalized not good for directed cordes
        if self.start + self.length >= self.universe:
            self.normalized = ((self.start+self.length) % self.universe, self.start)
        else:
            self.normalized = (self.start, self.start + self.length)
        #print("corde")

    def __eq__(self, other):
        res = (self.universe == other.universe)
        print(res)
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


            
        
    def avoids(self, other):
        res = (self.universe == other.universe and 
               self.start != other.start and 
               self.start != (other.start + other.length) % self.universe and
               (self.start + self.length) % self.universe != other.start and
               (self.start + self.length) % self.universe != (
                   other.start + other.length) % self.universe )
        return res

class DirectedCorde(Corde):
    
    def __eq__(self,  other):
        res = (self.universe == other.universe)
        print(res)
        res = res and (self.start == other.start and self.length == other.length) 
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
    
    
            
class CordeSets:        
    def __init__(self, n):
        self.universe = n
        self.setAllCordes()
        self.setAllExclusiveCordeSets()
        #self.allExclusiveSets()

    def setAllCordes(self):
        self.allCordes = []
        for start in range(0,self.universe):
            for length in range(1, self.universe - start):
                self.allCordes.append(Corde(self.universe, start, length))
                #print(Corde(self.universe, start, length))
        
        return self.allCordes

    def setAllExclusiveCordeSets(self):
        self.allExclusiveCordeSets = []
        all = self.allCordes
        allTestCords = all[:]
        #for (start, cord) in enumerate(allTestCords):
        #    result = CordeSet(self.universe, [])
        #    newRes = self.addExclusiveCord(
        #self.exclusiveCords, result, allTestCords[start+1:][:])
        
        result = CordeSet(self.universe, [])
        newRes = self.addExclusiveCord(
            self.allExclusiveCordeSets, result, allTestCords[:])
        return self.allExclusiveCordeSets
        

        
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
                    self.addExclusiveCord(allResults,
                                          testResult, remainingCords[current+1:][:])
            return None


            
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

    cS = CordeSets(5)
    #for c in cS.allCordes():
    #    print(c)
    res = cS.allExclusiveCordeSets
    for x in res:
        print(x.graphic())



    
if __name__ == '__main__':
    
    #simpletest2()
    fillSet()
