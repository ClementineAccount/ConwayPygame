import pygame
import Grid
import math

#Size of the cell represented as a rect
defaultSize = 10
gapSize = 1
left = 0
top = 0

class Cell(Grid.Cell):
    def __init__(self, inputRect : pygame.Rect, aliveColor = "white", deadColor = "black"):
        self.aliveColor = aliveColor
        self.deadColor = deadColor
        self.rect = inputRect
        self.alive = False

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.aliveColor, self.rect)
        else:
            pygame.draw.rect(screen, self.deadColor, self.rect)

    def setAlive(self, alive):
        self.alive = alive


#Every ten gaps there is a block of ten 'leftover'. In order to fit it for hardcoded 800x600 I can subtract the extra gap blocks
class GridTable(Grid.GridTable):
    def __init__(self, colCount = 80 - 8 + 1, rowCount = 60 - 6 + 1):
        # List of Pygame Rectangles to draw
        self.cellList = []
        self.rowCount = rowCount
        self.colCount = colCount
        self.gapSize = gapSize
        self.blockSize = defaultSize
        self.createRect()
        self.setAliveList = []
        self.setDeadList = []


    def createRect(self):
        for row in range(self.rowCount):
            for col in range (self.colCount):
                self.cellList.append(Cell(pygame.Rect(left + col * ( self.blockSize + self.gapSize), top + row * ( self.blockSize + self.gapSize),  self.blockSize,  self.blockSize)))
    
    def draw(self, screen):
        for i in range(len(self.cellList)):
            self.cellList[i].draw(screen)

    def checkBound(self, col, row):
        if col >= self.colCount or row >= self.rowCount:
            return False
        if col < 0 or row < 0:
            return False
        return True

    # For like mouse clicking on the thing and stuff
    def clickGrid(self, posX, posY):
        #Transform to the coordinate space
        posX = posX - left
        posY = posY - top

        # We could create a logger class in order to handle print statements (so can easily disable them)

        #print(posX)
        #print(posY)

        column = posX / (self.blockSize + self.gapSize)
        row = posY / (self.blockSize + self.gapSize)

        if self.checkBound(column, row):
            self.setCellAlive(int(column), int(row), True)

        #if self.checkBound(column, row):
        #    self.setCellColor(int(column), int(row), "blue")

    def accessCell(self, col, row):
        #print(math.floor(row * self.colCount + col))
        return self.cellList[int(row * self.colCount + col)]
    
    def setCellColor(self, col, row, color):
        self.accessCell(col, row).color = color

    def setCellAlive(self, col, row, alive):
        self.accessCell(col, row).setAlive(alive)


    def SetNeighbourLive(self, col, row, aliveList):
        if self.checkBound(col, row):
            aliveList.append(self.accessCell(col, row))
    
    def SetNeighbours(self, col, row, setAliveList):

        #Cool pattern but not same behavior
        #for x in range(-1, 1):
            #for y in range(-1, 1):
                #This only goes in the top left quadrant...
                #self.SetNeighbourLive(col + x, row + y, setAliveList)
                #This only goes in the bottom right quadrant...
                #self.SetNeighbourLive(col - x, row - y, setAliveList)

        #Upper right triangle shape
        #for x in range (-1, 1):
        #    self.SetNeighbourLive(col + x, row, setAliveList)
        #    self.SetNeighbourLive(col, row + x, setAliveList)

        #Bottom right triangle shape
        #for x in range (-1, 1):
        #    self.SetNeighbourLive(col - x, row, setAliveList)
        #    self.SetNeighbourLive(col, row - x, setAliveList)

        
        #It'd be pretty cool if there was a way to pass in a function pointer for something like this...
        #We will worry about that after the game of life demo though...

        #Alternatively, a double for loop can achieve the same thing with a "col + x, row + y" type logic. I bet I can do that now

        #Square Fill
        #self.SetNeighbourLive(col - 1, row - 1, setAliveList)
        #self.SetNeighbourLive(col - 1, row, setAliveList)
        #self.SetNeighbourLive(col - 1, row + 1, setAliveList)

        #self.SetNeighbourLive(col, row + 1, setAliveList)
        #self.SetNeighbourLive(col, row - 1, setAliveList)

        #self.SetNeighbourLive(col + 1, row - 1, setAliveList)
        #self.SetNeighbourLive(col + 1, row, setAliveList)
        #self.SetNeighbourLive(col + 1, row + 1, setAliveList)

        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 and y == 0):
                    continue
                self.SetNeighbourLive(col + x, row + y, setAliveList)

        


    #Dummy function for next time. Got to plan this out a bit more
    def SetNeighboursConway(self, col, row, setAliveList, setDeadList):

        #Rule 1: Any alive cell with two or three live neighbours become a live cell
        #Rule 2: Any dead cell with three live neighbours becomes a live cell

        cellCheck = self.accessCell(col, row)
        livingNeighbours = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 and y == 0):
                    continue
                if self.checkBound(col + x, row + y) and self.accessCell(col + x, row + y).alive:
                    livingNeighbours += 1
                    #print("Add Neighbour")
        if livingNeighbours == 3:
            setAliveList.append(cellCheck)
        elif cellCheck.alive and livingNeighbours == 2:
            setAliveList.append(cellCheck)
        else:
            #Rule 3: All other cells set to die
            setDeadList.append(cellCheck)

    def UpdateGrid(self):
        # Cells to update after a chec
        self.setAliveList.clear()
        self.setDeadList.clear()

        #Set top neighbour alive if I am alive (like a virus but one way... for testing...)
        for row in range(self.rowCount):
            for col in range(self.colCount):
                self.SetNeighboursConway(col, row, self.setAliveList, self.setDeadList)

                #if self.accessCell(col, row).alive:
                #    self.SetNeighbours(col, row, setAliveList)


        #After checking everyone, only then do you set the cell to live (determinsitic behaviour)
        for cell in self.setAliveList:
            cell.setAlive(True)

        for cell in self.setDeadList:
            cell.setAlive(False)
                    

            


