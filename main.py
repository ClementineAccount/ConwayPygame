# Example file showing a basic pygame "game loop"
import pygame
import math
import os

# Learning to have more than one python file
import ConwayGrid

# Some configuration
width = 800
height = 600

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

# pygame setup
pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((width, height), vsync=False, flags=pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

grid = ConwayGrid.GridTable()

mouse = pygame.mouse
key = pygame.key


wasRight = False
wasPressedSpace = False
wasPressedD = False

elapsedTime = 0.0
tickTimeSeconds = 0.1
isPaused = True

while running:   
    dt = clock.tick(60) / 1000
    elapsedTime += dt
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                grid.resizeGrid(grid.colCount + 1, grid.rowCount)
            if event.key == pygame.K_s:
                grid.resizeGrid(grid.colCount, grid.rowCount + 1)
            if event.key == pygame.K_w:
                grid.resizeGrid(grid.colCount, grid.rowCount - 1)
            if event.key == pygame.K_a:
                grid.resizeGrid(grid.colCount - 1, grid.rowCount)    
                


    clicks = mouse.get_pressed(3)

    if clicks[0]:
        posX = mouse.get_pos()[0];
        posY = mouse.get_pos()[1];
        grid.clickGrid(posX, posY)
    

    if clicks[2] and not wasRight:
        #print("what")
        grid.UpdateGrid()
        wasRight = True
    elif not clicks[2] and wasRight:
        wasRight = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not wasPressedSpace:
        isPaused = not isPaused
        wasPressedSpace = True
    elif not keys[pygame.K_SPACE] and wasPressedSpace:
        wasPressedSpace = False
    

    if elapsedTime > tickTimeSeconds:
        elapsedTime = 0.0
        if not isPaused:
            grid.UpdateGrid()
    
            
 
    # flip() the display to put your work on screen
    #grid.setCellColor(2, 2, "green")

    screen.fill("snow3")
    grid.draw(screen)

    pygame.display.flip()
    pygame.display.set_caption(str(clock.get_fps()))
    
pygame.quit()