from key import *
from chords import *

class CMajor(Key):
    def __init__(self, notes):
        super().__init__(notes, "c", NoteType.NATURAL, KeyType.MAJOR)
        
        self.chords = {
            1 : [Major("c"), Major("g"), Major("f")],
            2 : [Minor("d"), Minor("e"), Major("c").seventh(), Minor("a"), Major("f").seventh(), Major("f").seventh()],
            3 : [Five("c"), Five("g"), Five("f")],
            4 : [Major("a"), Minor("b"), Minor("c"), Minor("g"), Minor("f"), Major("d"), Major("e"), Minor("e").seventh()],
            5 : [Dim("c"), Minor("c").seventh(), Major("b"), Sus("c", 2), Sus("c", 4), Sus("d", 2), Sus("d", 4)],
            6 : [Minor("c").seventh(), Dim("c").seventh()],
            7 : [Dim("c").half7(), Aug("c"), Major("c").dom7(), Dim("c").seventh()]
        }