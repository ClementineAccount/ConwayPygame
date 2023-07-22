import pygame
import Grid
import math

#Size of the cell represented as a rect
defaultSize = 10
gapSize = 1
left = 10
top = 10
gridColor = "red"

class Cell(Grid.Cell):
    def __init__(self, inputRect : pygame.Rect, aliveColor = "red", deadColor = "blue"):
        self.color = "blue"
        self.aliveColor = aliveColor
        self.deadColor = deadColor
        self.rect = inputRect
        self.alive = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def setAlive(self, alive):
        self.alive = alive
        self.color = self.deadColor
        if self.alive:
            self.color = self.aliveColor


class GridTable(Grid.GridTable):
    def __init__(self, colCount = 50, rowCount = 50):
        # List of Pygame Rectangles to draw
        self.cellList = []
        self.rowCount = rowCount
        self.colCount = colCount
        self.gridColor = "red"
        self.gapSize = gapSize
        self.blockSize = defaultSize
        self.createRect()

    def createRect(self):
        for row in range(self.rowCount):
            for col in range (self.colCount):
                self.cellList.append(Cell(pygame.Rect(left + col * ( self.blockSize + self.gapSize), top + row * ( self.blockSize + self.gapSize),  self.blockSize,  self.blockSize),
                                     self.gridColor))
    
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

    def UpdateGrid(self):
        # Cells to update after a check
        setAliveList = []

        #Set top neighbour alive if I am alive (like a virus but one way... for testing...)
        for row in range(self.rowCount):
            for col in range(self.colCount):
                if self.accessCell(col, row).alive:
                    #print("Hello")
                    self.SetNeighbourLive(col, row + 1, setAliveList)
                    self.SetNeighbourLive(col, row - 1, setAliveList)
                    self.SetNeighbourLive(col + 1, row, setAliveList)
                    self.SetNeighbourLive(col - 1, row, setAliveList)
                    self.SetNeighbourLive(col + 1, row - 1, setAliveList)
                    self.SetNeighbourLive(col + 1, row + 1, setAliveList)
                    self.SetNeighbourLive(col - 1, row - 1, setAliveList)
                    self.SetNeighbourLive(col - 1, row + 1, setAliveList)

        #After checking everyone, only then do you set the neighbours to live (determinsitic behaviour)
        for cell in setAliveList:
            cell.setAlive(True)
                    

            

