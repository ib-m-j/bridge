class DictArray:
    def __init__(self, dict):
        self.dict = dict


    def __add__(self, other):
        resDict = self.dict.copy()
        for key in other.dict.keys():
            if key in resDict:
                resDict[key] = resDict[key]+other.dict[key]
            else:
                resDict[key] = other.dict[key]
        
        return DictArray(resDict)

class ArrayPrinter:
    def __init__(self, array, width = 0, height = 0, borders = True):
        if isinstance(array, dict):
            #print("found dict")
            self.array = array
        elif isinstance(array, DictArray):
            #print("found dict")
            self.array = array.dict
            
        if width == 0:
            self.width = max([k[1] for k in self.array.keys()]) + 1
        else:
            self.width = width
        if height == 0:
            self.height = max([k[0] for k in self.array.keys()]) + 1
        else:
            self.height = height
        self.borders = borders

        
    def print(self, title = 'noname'):
        res = '\n' + title + '\n'
        starter = ''
        if self.borders:
            starter = '{:3}'.format('')
            res = res + starter + ''.join(
                '{:3}'.format(x) for x in range(self.width))
            res = res + '\n' + ''.join(
                '{:3}'.format(3*'-') for x in range(self.width + 1))
        for i in range(self.height):
            if self.borders:
                res = res + '\n' + '{:2}|'.format(i)
            else:
                res = ress + '\n'
            for j in range(self.width):
                if (i,j) in self.array:
                    res = res + '{:3}'.format(self.array[(i,j)])
                else:
                    res = res + '{:3}'.format('')
        return res

    @classmethod
    def arrayPrinterFromLists(self, lists):
        res = {}
        for i,row in enumerate(lists):
            for j,rowVal in enumerate(row):
                res[(i,j)] = rowVal
        return ArrayPrinter(res)

if __name__ == '__main__':
    array = {}
    for a in range(4):
        for b in range(3):
            array[(a,b)] = a*b
    theArray = ArrayPrinter(array)
    print(theArray.print())
    print(theArray.width)
    print(array)
