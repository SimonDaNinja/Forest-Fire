import random
import matplotlib.pyplot as plt

class Forest:

    def __init__(self, gridHeight, gridWidth, matchDropRate, growthRate, numberOfIterations, plot = True, storeHistory = False):
        self.gridHeight = gridHeight
        self.gridWidth = gridWidth
        self.matchDropRate = matchDropRate
        self.growthRate = growthRate
        self.plot = plot
        self.storeHistory = storeHistory
        self.fire = set()
        self.trees = set()
        self.empty = set([(i,j) for j in range(gridWidth) for i in range(gridHeight)])
        #TODO: pre-allocate memory more efficiently, or store history in other way to avoid performance drops
        if storeHistory:
            self.history = []
        self.Run(numberOfIterations)

    def Run(self, numberOfIterations):
        plotStarted = False
        lastFireSize = 0

        # This is some preparation for animation
        # TODO: optimize animation and make code nicer
        if self.plot:
            figure = plt.figure()
            plt.axis([-1, self.gridHeight, -1, self.gridWidth])

        for i in range(numberOfIterations):

            # Remove fires
            self.empty |= self.fire
            self.fire = set()

            # Grow trees
            numberOfNewTrees = sum([1 for i in range(len(self.empty)) if random.uniform(0,1)<growthRate])
            newTreePositions = set(random.sample(self.empty,numberOfNewTrees))
            self.trees |= newTreePositions
            self.empty -= newTreePositions
            """
            for position in self.empty.copy():
                r = random.uniform(0,1)
                if r < growthRate:
                    self.empty.remove(position)
                    self.trees.add(position)
            """

            # Drop match
            r = random.uniform(0,1)
            if r < matchDropRate:
                dropSite = random.sample(self.trees, 1)[0]
                self.DropMatch(dropSite)
            if len(self.fire)>0:
                lastFireSize = len(self.fire)

            # Output some hopefully useful information during runtime
            # TODO: select more useful information
            if i%1==0:
                print("current iteration: {}\ncurrent number of trees: {}\nlast fire size: {}".format(i,len(self.trees),lastFireSize))

            # Store state in history
            if self.storeHistory:
                self.history.append((self.fire.copy(),self.trees.copy(),self.empty.copy()))

            # This is where animation happens
            # TODO: optimize animation and make code nicer
            if self.plot:
                fireRow = [site[0] for site in self.fire]
                fireCol = [site[1] for site in self.fire]
                treesRow = [site[0] for site in self.trees]
                treesCol = [site[1] for site in self.trees]
                if not plotStarted:
                    plotStarted = True
                    a = plt.scatter(treesCol,treesRow,color=(0,.6,0))
                else:
                    aArray = [[site[0],site[1]] for site in self.trees]
                    a.set_offsets(aArray)
                if len(self.fire)>0:
                    b = plt.scatter(fireCol,fireRow,color=(1,.5,0))
                plt.pause(0.000001)
                if len(self.fire)>0:
                    b.remove()


    def DropMatch(self,dropSite):
        fireQueue = set()
        if dropSite in self.trees:
            fireQueue.add(dropSite)
        while fireQueue:
            site = fireQueue.pop()
            self.trees.remove(site)
            self.fire.add(site)
            neighbours = self.GetNeighbours(site)

            fireQueue |= (neighbours&self.trees)

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
    numberOfIterations = 3000
    plot = True # Note: this makes the program much slower
    storeHistory = False
    forest = Forest(gridHeight, gridWidth, matchDropRate, growthRate, numberOfIterations, plot = plot, storeHistory = storeHistory)
    print('terminated')
