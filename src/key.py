import random
from playable import Chord
from enum import Enum
import helpers
from chords import ChordBuilder

class KeyType(Enum):
    MAJOR = 0
    MINOR = 1

class NoteType(Enum):
    NATURAL = 0
    SHARP = 1
    FLAT = 2

class Key():
    def __init__(self, notes :list[str], baseNote : str, noteType :NoteType, keyType : KeyType):
        self.baseNote = baseNote
        self.keyType = keyType
        self.noteType = noteType
        self.allNotes = notes
        
        self.notes = self.getNotes()
        self.chords : dict[int, list[ChordBuilder]] = {}

    def checkDuplicates(self):
        for dif in self.chords.items():
            for i in range(0, len(dif[1])):
                chord = dif[1][i]
                for innerDif in self.chords.items():
                    for j in range(0, len(innerDif[1])):
                        if dif[0] == innerDif[0] and i == j: #looking at the same chord
                            continue
                        innedChord = innerDif[1][j]
                        if chord.equals(innedChord):
                            raise Exception(f"Chords '{chord.text}({dif[0]})' and '{innedChord.text}'({innerDif[0]}) are the same!")

    # Chord = (name :str, )
    def getRandomChord(self, difficultyFrom : int, difficultyTo: int) -> Chord:
        difficulty = random.randint(difficultyFrom, difficultyTo)

        if len(self.chords) <= difficulty:
            difficulty = len(self.chords)

        chord = random.choice(self.chords[difficulty])

        name = chord.text
        steps = chord.steps
        baseNote = chord.baseNote
        return Chord(name, self.buildChord(baseNote, steps), baseNote, difficulty)
    
    def getNotes(self) -> list[str]:
        if self.keyType == KeyType.MAJOR:
            return self.getNotesWithRule([2, 2, 1, 2, 2, 2])
        if self.keyType == KeyType.MINOR:
            return self.getNotesWithRule([2, 1, 2, 2, 1, 2])

    def getNotesWithRule(self, rule : list) -> list[str]: # rule list contains steps as half steps on the keys
        if self.keyType == KeyType.MAJOR:
            if self.noteType == NoteType.NATURAL:
                return self.takeNotesWithSteps(self.allNotes, rule)

    def takeNotesWithSteps(self, notes : list, steps : list) -> list[str]:
        baseIndex = notes.index(self.baseNote)
        maxIndex = len(notes) - 1
        result = [self.baseNote]
        index = baseIndex

        for step in steps:
            index += step
            if index > maxIndex:
                index -= (maxIndex + 1)
            
            result.append(notes[index])
        
        return result
        
    # Return list of notes in a chord
    def buildChord(self, baseNote :str, steps :list) -> list:
        baseIndex = self.allNotes.index(baseNote)
        maxIndex = len(self.allNotes) - 1
        notes = [baseNote]

        for step in steps:
            index = baseIndex + step
            if index > maxIndex:
                index -= (maxIndex + 1)

            notes.append(self.allNotes[index])

        return notes
    