from pygame import Surface, font, Rect
import pygame
import pyGameHelpers
import statistics
import random
from key import Key
import chords
import keyboard

class Ui:
    def __init__(self, display: Surface):
        self.display = display
        self.bottomHeight = 80
        self.topHeight = 60
        self.displayRect = display.get_rect()

    def draw(self):
        bottomLineStart = (0, self.displayRect.height - self.bottomHeight)
        bottomLineEnd = (self.displayRect.width, self.displayRect.height - self.bottomHeight)
        pygame.draw.line(self.display, (255, 255, 255), bottomLineStart, bottomLineEnd)

        topLineStart = (0, self.topHeight)
        topLineEnd = (self.displayRect.width, self.topHeight)
        pygame.draw.line(self.display, (255, 255, 255), topLineStart, topLineEnd)


class Fps:
    def __init__(self, display :Surface, fpsCap :int, font :font.Font):
        self.font = font
        self.display = display
        self.displayRect = display.get_rect()
        self.fpsCounter = 0
        self.fpsList : list[int] = [fpsCap] * int((fpsCap/2))

    def draw(self, deltaT :int):
        self.fpsCounter += 1
        if self.fpsCounter >= len(self.fpsList):
            self.fpsCounter = 0

        self.fpsList[self.fpsCounter] = int(1/(deltaT/1000))
        avgFps = int(statistics.mean(self.fpsList))

        fpsDisplay = self.font.render("FPS: " + str(avgFps), True, (255, 255, 255))
        topRight = pyGameHelpers.topRightCoords(fpsDisplay.get_rect(), self.displayRect)
        self.display.blit(fpsDisplay, topRight)

class Progress:
    def __init__(self, display :Surface, font :font.Font, startingDifficulty :int):
        self.display = display
        self.displayRect = display.get_rect()
        self.font = font
        self.startingDifficulty = startingDifficulty
        self.baseDifficultyDifference = 10
        self.difficultyMultiplier = 1.2

        self.reset()

    def reset(self):
        self.score = 0
        self.difficulty = self.startingDifficulty

    def draw(self):
        scoreDisplay = self.font.render("score: " + str(self.score), True, (50, 255, 50))
        bottomLeft = pyGameHelpers.bottomLeftCoords(scoreDisplay.get_rect(), self.displayRect)
        self.display.blit(scoreDisplay, bottomLeft)
    
        difficultyDisplay = self.font.render("Difficulty: " + str(self.difficulty), True, (50, 255, 50))
        bottomRight = pyGameHelpers.bottomRightCoords(difficultyDisplay.get_rect(), self.displayRect)
        self.display.blit(difficultyDisplay, bottomRight)

    def getDifficulty(self) -> int:
        requiredScore = self.baseDifficultyDifference * self.difficulty * (self.difficultyMultiplier**self.difficulty)
        if self.score >= requiredScore:
            self.difficulty += 1
        
        return self.difficulty

    def addPoints(self, points :int):
        self.score += points

class ChordTimer:
    def __init__(self, scale :Key, progress :Progress, width :int, fromTop :int):
        self.maxSpeed :int = 110
        self.progress :Progress = progress
        self.scale :Key = scale
        self.minChordTime :int = 2500
        self.fromTop :int = fromTop
        self.width :int = width
        self.clear()

    def update(self, deltaT):
        self.timer += deltaT
        if self.timer >= self.time:
            newChord = self.scale.getAdjustedRandomChord(1, self.progress.difficulty)
            speed = int(40 + (1/newChord.difficulty) * self.progress.score)
            if speed > self.maxSpeed:
                speed = self.maxSpeed
            newChord.init((random.randint(10, self.width), self.fromTop), speed)
            #print("adding", newChord.text)

            self.chords.append(newChord)

            if self.progress.difficulty >= self.scale.getMaxDifficulty():
                self.time -= int(self.progress.score/30)
            elif self.time > self.minChordTime:
                self.time -= int(self.progress.score)
            self.timer = 0

    # return points
    def checkHits(self, keyboard :keyboard.KeyBoard) -> int:
        for ac in self.chords:
            if ac.checkHit(keyboard.playedKeys):
                # the notes played match a chord on the screen
                self.progress.addPoints(ac.difficulty)
                self.chords.remove(ac)
                keyboard.clear()
                break

    def clear(self):
        self.timer :int = 1000
        self.time :int = 3000
        self.chords :list[chords.Chord] = []