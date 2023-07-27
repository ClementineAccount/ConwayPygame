import pygame
import math

#Size of the cell represented as a rect
defaultSize = 10
gapSize = 1
left = 10
top = 10
gridColor = "red"

class Cell:
    def __init__(self, inputRect : pygame.Rect, color):
        self.color = color
        self.rect = inputRect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class GridTable:
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
            self.setCellColor(int(column), int(row), "blue")


        #print("Row:", row)
        #print("Col:", column)


    
    def accessCell(self, col, row):
        #print(math.floor(row * self.colCount + col))
        return self.cellList[int(row * self.colCount + col)]
    
    def setCellColor(self, col, row, color):
        self.accessCell(col, row).color = color
        


