from __future__ import annotations
from enum import Enum
from playable import Chord

class ChordType(Enum):
    MAJOR = 0
    MINOR = 1
    DIM   = 2
    AUG   = 3
    SUS   = 4
    FIVE  = 3

class ChordBuilder():
    def __init__(self, baseText :str, baseNote :str, baseSteps :list[int], type :ChordType):
        self.text = baseText
        self.baseNote = baseNote
        self.steps = baseSteps
        self.key = None
        self.type = type
        self.playCount = 0

        self.major = "maj"
        self.flatNotation = "♭"
        self.sharpNotation = "#"

    def equals(self, other :ChordBuilder) -> bool:
        return self.baseNote == other.baseNote and self.steps == other.steps

    # new base note
    def slash(self, note :str):
        pass

    def flat5(self):
        if self.type == ChordType.AUG:
            raise Exception("Aug chord to flat 5 == major chord")
        self.steps[1] -= 1
        self.text += self.flatNotation + "5"

    def sharp5(self):
        if self.type == ChordType.AUG:
            raise Exception("Aug chord with sharp 5 == different major chord with ")
        self.steps[1] += 1
        self.text += self.sharpNotation + "5"

    def sixth(self):
        self.steps.append(9)
        self.text += "6"
    
    def flat6(self):
        self.steps.append(8)
        self.text += "-6"

    def half7(self) -> ChordBuilder:
        if self.type != ChordType.DIM:
            raise Exception("Only Diminished base chord can have Half seven!")
        self.steps.append(10)
        self.text = self.text.removesuffix("dim") +"⌀7"
        return self

    def dom7(self) -> ChordBuilder:
        if self.type != ChordType.MAJOR:
            raise Exception("Only major base chord can be dominant seven!")
        self.steps.append(10)
        self.text += "7"
        return self

    def major7(self) -> ChordBuilder:
        if self.type != ChordType.MINOR:
            raise Exception("Only minor base chord can have separate major seven notation!")
        self.steps.append(11)
        self.text.append(self.major + "7")
        return self

    def seventh(self) -> ChordBuilder:
        type = self.type

        if type == ChordType.MAJOR:
            self.steps.append(11)
            self.text += self.major + "7"
        elif type == ChordType.MINOR:
            self.steps.append(10)
            self.text += "7"
        elif type == ChordType.DIM:
            self.steps.append(9)
            self.text += "7"
        elif type == ChordType.AUG:
            self.steps.append(10)
        elif type == ChordType.SUS:
            self.steps.append(10)
            self.text = self.text[0] + "7" + self.text[1:]
        
        return self

            

def Major(baseNote: str) -> ChordBuilder:
    return ChordBuilder(baseNote.upper(), baseNote, [4, 7], ChordType.MAJOR) 

def Minor(baseNote: str) -> ChordBuilder:
    return ChordBuilder(baseNote.upper() + "m", baseNote, [3, 7], ChordType.MINOR)

def Dim(baseNote: str) -> ChordBuilder:
    return ChordBuilder(baseNote.upper() + "dim", baseNote, [3, 6], ChordType.DIM)

def Aug(baseNote: str) -> ChordBuilder:
    return ChordBuilder(baseNote.upper() + "aug", baseNote, [4, 8], ChordType.AUG)

def Five(baseNote: str):
    return ChordBuilder(baseNote.upper() + "5", baseNote, [7], ChordType.FIVE)


def Sus(baseNote: str, value :int) -> ChordBuilder:
    if value == 2:
        return ChordBuilder(baseNote.upper() + "sus2", baseNote, [2, 7], ChordType.SUS)
    elif value == 4:
        return ChordBuilder(baseNote.upper() + "sus4", baseNote, [5, 7], ChordType.SUS)
    else:
        raise Exception("Sustained base triplet can only be 2 or 4 valued!")