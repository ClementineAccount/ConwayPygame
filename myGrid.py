import pygame

#Size of the cell represented as a rect
defaultSize = 5
topLeft = 0


class Grid:
    def __init__(self, rowCount = 10):
        # List of Pygame Rectangles to draw
        self.rectList = []
        self.rowCount = rowCount
        self.createRect()

    def createRect(self):
        for i in range(self.rowCount):
            self.rectList.append(pygame.Rect(topLeft + i * defaultSize, 0, defaultSize, defaultSize))
    

