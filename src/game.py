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
difficulty = startingDifficulty
rawDifficulty = startingDifficulty

helpers.printDeviceInfos()

allNotes = helpers.notes

transformer = NoteTranformer(keyboard.lowC, allNotes)

cMajor = CMajor(allNotes)
notes = cMajor.getNotes()

score = 0

noteTime = 3000 # ms
noteTimer = 0 # ms

chordTime = CHORDTIMEBASE
chordTimer = chordTime

activeNotes :list[Note] = []
activeChords :list[Chord] = []

clock = pygame.time.Clock()

FPSAVERAGECOUNT = int(FPSCAP / 2)
fpsList : list[int] = [FPSCAP] * FPSAVERAGECOUNT # 5 long list
fpsPosCounter :int = 0


while True:
    deltaT = clock.tick(FPSCAP)
    display.fill((0,0,0))

    requiredScore = DIFFICULTYDIFFERENCE * difficulty * (DIFFICULTYMULTIPLIER**difficulty)
    if score >= requiredScore:
        difficulty += 1
    #difficulty = int(score / DIFFICULTYDIFFERENCE) + startingDifficulty

    bottomLineStart = (0, displayRect.height - BOTTOMHEIGHT)
    bottomLineEnd = (displayRect.width, displayRect.height - BOTTOMHEIGHT)
    pygame.draw.line(display, (255, 255, 255), bottomLineStart, bottomLineEnd)

    topLineStart = (0, TOPHEIGHT)
    topLineEnd = (displayRect.width, TOPHEIGHT)
    pygame.draw.line(display, (255, 255, 255), topLineStart, topLineEnd)

    # FPS
    fpsPosCounter += 1
    if fpsPosCounter >= len(fpsList):
        fpsPosCounter = 0
    fpsList[fpsPosCounter] = int(1/(deltaT/1000))
    avgFps = int(statistics.mean(fpsList))

    fpsDisplay = chordFont.render("FPS: " + str(avgFps), True, (255, 255, 255))
    topRight = pyGameHelpers.topRightCoords(fpsDisplay.get_rect(), displayRect)
    display.blit(fpsDisplay, topRight)

    scoreDisplay = chordFont.render("score: " + str(score), True, (50, 255, 50))
    bottomLeft = pyGameHelpers.bottomLeftCoords(scoreDisplay.get_rect(), displayRect)
    display.blit(scoreDisplay, bottomLeft)
    
    difficultyDisplay = chordFont.render("Difficulty: " + str(difficulty), True, (50, 255, 50))
    bottomRight = pyGameHelpers.bottomRightCoords(difficultyDisplay.get_rect(), displayRect)
    display.blit(difficultyDisplay, bottomRight)

    #noteTimer += deltaT
    #if noteTimer >= noteTime:
    #    newNote = Note(random.choice(notes), random.randint(30, WIDTH - 30))
    #    activeNotes.append(newNote)
    #    noteTimer = 0

    # Add a chord that needs playing if timer is up
    chordTimer += deltaT
    if chordTimer >= chordTime:
        newChord = cMajor.getAdjustedRandomChord(1, difficulty)
        speed = int(40 + (1/newChord.difficulty) * score)
        if speed > MAXSPEED:
            speed = MAXSPEED
        newChord.init((random.randint(10, WIDTH - 80), TOPHEIGHT - 20), speed)
        #print("adding", newChord.text)

        activeChords.append(newChord)

        if difficulty >= cMajor.getMaxDifficulty():
            chordTime -= int(score/30)
        elif chordTime > MINCHORDTIME:
            chordTime -= int(score)
        chordTimer = 0

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
    for ac in activeChords:
        if ac.pos[1] >= HEIGHT - 100:
            # Chord hit the bottom, end the game, ask for retry
            retry = gameStates.lose(display, endFont, score)
            if pyGameHelpers.waitForR():
                keyboard.clear()
                activeChords.clear()
                difficulty = startingDifficulty
                score = 0
                chordTime = CHORDTIMEBASE
                chordTimer = 0
                clock.tick(FPSCAP)
            else:
                print("quit!")
                pygame.quit()
                pygame.midi.quit()
                sys.exit()
                
        if ac.checkHit(keyboard.playedKeys):
            # the notes played match a chord on the screen
            score += ac.difficulty
            activeChords.remove(ac)
            keyboard.clear()
            break

    # Update the position of all chords and draw them again
    for c in activeChords:
        c.update(deltaT)
        c.draw(chordFont, display)
 
    pygame.display.update()