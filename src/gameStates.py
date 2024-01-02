import pygame
from pygame import Surface, font
import pyGameHelpers

def lose(display :Surface, font :font.Font, score :int) -> bool:
    
    text = "You lost!  Score: " + str(score) + " points! r to retry!"
    textSurface = font.render(text, True, (255, 50, 50))
    textMid = textSurface.get_rect()
    dispMid = display.get_rect()
    mid = pyGameHelpers.centerCoords(textMid, dispMid)

    display.blit(textSurface, mid)
    pygame.display.update()