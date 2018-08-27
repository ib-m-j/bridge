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
        print("corde")

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
    
    def addCorde(self, corde):
        assert self.hasRoom(corde) , "corde already inserted"
        self.cordes.append(corde)
        return self

    def hasRoom(self, corde):
        for c in self.cordes:
            if not c.avoids(corde):
                return False
        return True   

    
            
class CordeSets:        
    def __init__(self, n):
        self.universe = n
        self.allCords = []

    def allCordes(self):
        if self.allCords:
            return self.allCordes
        
        self.allCords = []
        for start in range(0,self.universe):
            for length in range(1, self.universe - start):
                self.allCords.append(Corde(self.universe, start, length))
                #print(Corde(self.universe, start, length))

        return self.allCords

    def allExclusiveSets(self):
        self.exclusiveCords = []
        all = self.allCordes()
        allTestCords = all[:]
        while True:
            result = CordeSet(self.universe, [])
            newRes = self.addExclusiveCord(result,allTestCords.__iter__())
            if newRes:
                self.exclusiveCords.append(newRes)
            print(newRes)
        for x in self.exclusiveCords:
            print(x)

    def addExclusiveCord(self, result, remainingCords):
        if len(result.cordes) >= self.universe // 2:
            return result
        else:
            while True:
                x = next(remainingCords)
                #print("Working on", x, len(remainingCords))
                #print(result, result.hasRoom(x))
                if result.hasRoom(x):
                    return self.addExclusiveCord(
                        result.addCorde(x), remainingCords)
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

def fillSet():

    cS = CordeSets(5)
    print(cS.allExclusiveSets()                  )
                      


    
if __name__ == '__main__':
    
    #simpletest1()
    fillSet()
