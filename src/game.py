import sys
import random
from playable import *
import pygame
from pygame.locals import *
from pygame.midi import *
import helpers
from noteTransformer import NoteTranformer
from keys import CMajor
import init
import gameStates
import pyGameHelpers
import statistics
import UI

pygame.init()
pygame.midi.init()

if not pygame.midi.get_init():
    raise Exception("Could not init midi module!")

vec = pygame.math.Vector2  # 2 for two dimensional
chordFont = pygame.font.Font("./src/seguisym.ttf", 30)
endFont = pygame.font.Font("./src/seguisym.ttf", 60)
 
HEIGHT = 750
WIDTH = 1200
BOTTOMHEIGHT = 80
TOPHEIGHT = 60
FPSCAP = 60
DIFFICULTYDIFFERENCE = 10
DIFFICULTYMULTIPLIER = 1.1
CHORDTIMEBASE = 3000
MAXSPEED = 110
MINCHORDTIME = 2500
 
display = pygame.display.set_mode((WIDTH, HEIGHT))
displayRect = display.get_rect()
pygame.display.set_caption("Chorde")

midiInputId = pygame.midi.get_default_input_id()
print(f"using input_id : {midiInputId}")
midiInput = pygame.midi.Input(midiInputId)

keyboard = init.initKeyBoard(midiInput, display, chordFont)

startingDifficulty = init.initDifficulty(display, chordFont)
progress = UI.Progress(display, chordFont, startingDifficulty)

helpers.printDeviceInfos()

allNotes = helpers.notes

transformer = NoteTranformer(keyboard.lowC, allNotes)

cMajor = CMajor(allNotes)
notes = cMajor.getNotes()

noteTime = 3000 # ms
noteTimer = 0 # ms

activeNotes :list[Note] = []

clock = pygame.time.Clock()

ui = UI.Ui(display)
fps = UI.Fps(display, FPSCAP, chordFont)
chordTimer = UI.ChordTimer(cMajor, progress, WIDTH - 90, TOPHEIGHT - 20)

while True:
    deltaT = clock.tick(FPSCAP)
    display.fill((0,0,0))

    difficulty = progress.getDifficulty()
    progress.draw()

    #difficulty = int(score / DIFFICULTYDIFFERENCE) + startingDifficulty

    ui.draw()
    fps.draw(deltaT)

    # Add a chord that needs playing if timer is up
    
    chordTimer.update(deltaT)

    helpers.tranformMidi2Events(midiInput)

    # Get midi input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            pygame.midi.quit()
            sys.exit()
        
        # Add or remove midi input depending whether signal is midi key up or down
        if event.type in [pygame.midi.MIDIIN]:
            keyNumber = event.data1
            note = transformer.tranform(keyNumber)
            #print("midi event:", event)
            if event.status == keyboard.up:
                keyboard.keyUp((keyNumber, note))
            elif event.status == keyboard.down:
                #print(keyNumber, note)
                keyboard.keyDown((keyNumber, note))
     
    for an in activeNotes:
        if an.pos[1] >= displayRect.height - BOTTOMHEIGHT + 30:
            activeNotes.remove(an)
        if an.checkHit(keyboard.playedKeys):
            activeNotes.remove(an)
            break

    # Check if a chord is hit or if chord has reached the bottom
    for ac in chordTimer.chords:
        if ac.pos[1] >= HEIGHT - 100:
            # Chord hit the bottom, end the game, ask for retry
            retry = gameStates.lose(display, endFont, progress.score)
            if pyGameHelpers.waitForKey(pygame.K_r):
                keyboard.clear()
                chordTimer.clear()
                progress.reset()
                clock.tick(FPSCAP)
            else:
                print("quit!")
                pygame.quit()
                pygame.midi.quit()
                sys.exit()
                
    chordTimer.checkHits(keyboard)

    # Update the position of all chords and draw them again
    for c in chordTimer.chords:
        c.update(deltaT)
        c.draw(chordFont, display)
 
    pygame.display.update()