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

wasRight = False

while running:   
    dt = clock.tick(60) / 1000
   
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


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
            
 
    # flip() the display to put your work on screen
    #grid.setCellColor(2, 2, "green")

    screen.fill("snow3")
    grid.draw(screen)

    pygame.display.flip()
    pygame.display.set_caption(str(clock.get_fps()))
    
pygame.quit()