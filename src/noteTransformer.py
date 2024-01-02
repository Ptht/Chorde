import helpers

class NoteTranformer():
    def __init__(self, firstC :int, notes :list):
        self.firstC = firstC
        self.middleCOctave = 4
        self.notes = notes

    def tranform(self, keyNumber :int) -> tuple[int, str]:
        octave = int((keyNumber - self.firstC) / 12)
        if octave < 0:
            return (-1, -1)
        
        return (octave, self.getNote(octave, keyNumber))
    
    def getNote(self, octave :int, keyNumber :int) -> str:
        return self.notes[((keyNumber - self.firstC) - (octave * 12))]