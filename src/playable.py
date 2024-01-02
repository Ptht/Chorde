import pygame

class Playable():
    def __init__(self, text :str, xPos :int):
        self.pos = (xPos, 0)
        self.speed = 40 # pixels per second
        self.difficulty = 1
        self.text = text

    def init(self, pos :tuple[int, int], speed: int):
        self.pos = pos
        self.speed = speed

    def update(self, delta):
        deltaS = delta / 1000
        self.pos = (self.pos[0], self.pos[1] + (self.speed * deltaS))
        
    def draw(self, font, display):
        c = font.render(self.text, True, (255,255,255))
        display.blit(c, self.pos)

    def checkHit(self, played):
        raise Exception("Should be overriden!")


class Note(Playable):
    def __init__(self, text :str, xPos :int = 0):
        super().__init__(text, xPos)

    def checkHit(self, played: list):
        if len(played) == 1:
            if played[0][1][1] == self.text:
                return True
        else:
            return False


class Chord(Playable):
    def __init__(self, text :str,notes :list, baseNote :str, difficulty :int, xPos :int = 0):
        super().__init__(text, xPos)
        self.notes = notes
        self.baseNote = baseNote
        self.difficulty = difficulty

    def checkHit(self, played):
        allPlayed = False
        if len(played) == len(self.notes):
            playedNotes = [x[1][1] for x in played]
            for n in playedNotes:
                if self.notes.count(n) == 1:
                    allPlayed = True
                else:
                    return False
        return allPlayed