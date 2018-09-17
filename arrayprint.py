class ArrayPrinter:
    def __init__(self, array, width = 0, height = 0, borders = True):
        self.array = array
        if width == 0:
            self.width = max([k[1] for k in array.keys()])
        else:
            self.width = width
        if height == 0:
            self.height = max([k[0] for k in array.keys()])
        else:
            self.height = height
        self.borders = borders

        
    def print(self, title = 'noname'):
        res = '\n' + title + '\n'
        starter = ''
        if self.borders:
            starter = '{:3}'.format('')
            res = res + starter + ''.join('{:3}'.format(x) for x in range(self.width))
            res = res + '\n' + ''.join(
                '{:3}'.format(3*'-') for x in range(self.width + 1))
        for i in range(self.height + 1):
            if self.borders:
                res = res + '\n' + '{:2}|'.format(i)
            else:
                res = ress + '\n'
            for j in range(self.width + 1):
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

    print(ArrayPrinter(array, width = 12, height = 12).print())
