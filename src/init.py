from pygame import Surface, font, Rect
from keyboard import KeyBoard
import pygame.midi
import pyGameHelpers

def initScore(baseDifficulty :int, multiplier :int):
    if baseDifficulty > 1:
        return int(baseDifficulty * (multiplier / 3))
    else:
        return 0


def initDifficulty(display :Surface, font :font.Font) -> int:
    difficulty = 1
    
    while True:
        display.fill((0,0,0))

        pyGameHelpers.showTextMiddle(display, font, (255, 255, 255),
                                     "Please select starting difficulty with arrows, enter to continue")

        pyGameHelpers.showTextMiddle(display, font, (255, 255, 255), str(difficulty), 100)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if difficulty < 3:
                        difficulty += 1
                elif event.key == pygame.K_LEFT:
                    if difficulty > 1:
                        difficulty -= 1
                elif event.key == pygame.K_RETURN:
                    return difficulty
            

def initKeyBoard(midi, display :Surface, font :font.Font) -> KeyBoard:
    display.fill((0,0,0))
    pyGameHelpers.showTextMiddle(display, font, (255, 255, 255),
                                 "Please press the lowest C on your MIDI device.")
    pygame.display.update()

    lowCKeyDown = pyGameHelpers.waitForMidiEvent(midi)
    down = lowCKeyDown[0][0]
    lowCNote = lowCKeyDown[0][1]
    
    lowCKeyUp = pyGameHelpers.waitForMidiEvent(midi)
    up = lowCKeyUp[0][0]

    display.fill((0,0,0))
    pyGameHelpers.showTextMiddle(display, font, (255, 255, 255),
                                 "Please press what you'd consider the middle C on your MIDI device.")
    pygame.display.update()

    midCKeyDown = pyGameHelpers.waitForMidiEvent(midi)
    midCNote = midCKeyDown[0][1]
    
    return KeyBoard(lowCNote, midCNote, down, up)



    