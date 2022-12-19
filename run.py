import pygame
import globals
import sprites
import time

#################################################################

pygame.init()
screen = pygame.display.set_mode((globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT)) 
pygame.display.set_caption("THE CURSED FOREST")
pygame.mouse.set_visible(False)

sprites = sprites.Sprites(screen)

while 1==1:
    sprites.animate()
    time.sleep(globals.REFRESH_DELAY_S)