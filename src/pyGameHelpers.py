import pygame
from pygame import Rect, event, Surface, font

def centerCoords(objectRect :Rect, surfaceRect :Rect) -> tuple[int, int]:
    xMid = (surfaceRect.width / 2) - (objectRect.width / 2)
    yMid = (surfaceRect.height / 2) - (objectRect.height / 2)

    return (xMid, yMid)

def bottomLeftCoords(objectRect :Rect, surfaceRect :Rect) -> tuple[int, int]:
    yBottom = (surfaceRect.height) - (objectRect.height)
    return (0, yBottom)

def bottomRightCoords(objectRect :Rect, surfaceRect :Rect) -> tuple[int, int]:
    yBottom = surfaceRect.height - objectRect.height
    xRight = surfaceRect.width - objectRect.width - 20
    return (xRight, yBottom)

def topRightCoords(objectRect :Rect, surfaceRect :Rect) -> tuple[int, int]:
    yTop = 5
    xRight = surfaceRect.width - 150
    return (xRight, yTop)

def showTextMiddle(display :Surface, font :font.Font, color :tuple[int, int, int], text :str, yOffSet :int = 0):
    diffText = font.render(text, True, color)
    mid = centerCoords(diffText.get_rect(), display.get_rect())
    mid = (mid[0], mid[1] + yOffSet)
    display.blit(diffText, mid)

def anyKey():
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return
        elif event.type == pygame.KEYDOWN:
            return

# False if something else pressed
def waitForKey(key :int) -> bool:
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return
        elif event.type == pygame.KEYDOWN:
            if event.key == key:
                return True
            else:
                return False

def waitForMidiEvent(midi):
    while True:
        if midi.poll():
            return midi.read(10)[0]