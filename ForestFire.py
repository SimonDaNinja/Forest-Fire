import random
import matplotlib.pyplot as plt

class Forest:

    def __init__(self, gridHeight, gridWidth, matchDropRate, growthRate, numberOfIterations, plot = True):
        self.gridHeight = gridHeight
        self.gridWidth = gridWidth
        self.matchDropRate = matchDropRate
        self.growthRate = growthRate
        self.plot = plot
        self.fire = set()
        self.forest = set()
        self.free = set([(i,j) for j in range(gridWidth) for i in range(gridHeight)])
        self.history = []
        self.Run(numberOfIterations)

    def Run(self, numberOfIterations):
        plotStarted = False
        lastFireSize = 0
        # This is some preparation for animation
        # TODO: optimize and make nicer
        if self.plot:
            figure = plt.figure()
            plt.axis([-1, self.gridHeight, -1, self.gridWidth])
        for i in range(numberOfIterations):
            for site in self.fire.copy():
                self.fire.remove(site)
                self.free.add(site)
            for position in self.free.copy():
                r = random.uniform(0,1)
                if r < growthRate:
                    self.free.remove(position)
                    self.forest.add(position)
            r = random.uniform(0,1)
            if r < matchDropRate:
                dropSite = random.sample(self.forest, 1)[0]
                self.DropMatch(dropSite)
            if len(self.fire)>0:
                lastFireSize = len(self.fire)
            if i%1==0:
                print("current iteration: {}\ncurrent number of trees: {}\nlast fire size: {}".format(i,len(self.forest),lastFireSize))

            self.history.append((self.fire.copy(),self.forest.copy(),self.free.copy()))
            # This is where animation happens
            # TODO: optimize and make nicer
            if self.plot:
                fireRow = [site[0] for site in self.fire]
                fireCol = [site[1] for site in self.fire]
                forestRow = [site[0] for site in self.forest]
                forestCol = [site[1] for site in self.forest]
                if not plotStarted:
                    plotStarted = True
                    a = plt.scatter(forestCol,forestRow,color=(0,.6,0))
                else:
                    aArray = [[site[0],site[1]] for site in self.forest]
                    a.set_offsets(aArray)
                if len(self.fire)>0:
                    b = plt.scatter(fireCol,fireRow,color=(1,.5,0))
                if len(self.fire)>0:
                    plt.pause(.1)
                    b.remove()
                else:
                    plt.pause(0.000001)


    def DropMatch(self,dropSite):
        fireQueue = set()
        if dropSite in self.forest:
            fireQueue.add(dropSite)
        while len(fireQueue)>0:
            site = fireQueue.pop()
            self.forest.remove(site)
            self.fire.add(site)
            neighbours = self.GetNeighbours(site)

            fireQueue |= (neighbours&self.forest)

    def GetNeighbours(self,site):
        row = site[0]
        col = site[1]

        leftNeighbourCol = (col-1)%self.gridWidth
        rightNeighbourCol = (col+1)%self.gridWidth
        topNeighbourRow = (row-1)%self.gridHeight
        bottomNeighbourRow = (row+1)%self.gridHeight

        neighbours = {(row,leftNeighbourCol),(row,rightNeighbourCol),(topNeighbourRow,col),(bottomNeighbourRow,col)}

        return neighbours

if __name__ == '__main__':
    gridHeight = 100
    gridWidth = 100
    matchDropRate = .1
    growthRate = .001
    numberOfIterations = 100000
    forest = Forest(gridHeight, gridWidth, matchDropRate, growthRate, numberOfIterations, plot = True)
