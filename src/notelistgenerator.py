import helpers
import math

def getNote(i : int) -> (int, str):
    currentIndex = i % len(helpers.notes)
    octave = int(i / (len(helpers.notes) if i > 0 else len(helpers.notes) + 1) )

    if i < 0:
        octave -= 1

    return (octave, helpers.notes[currentIndex])


# note, octave, frequency
def getListFromATo(start :int, end :int, step :int) -> list[str, int, float]:
    result :list[str, int, float] = []

    for i in range(start, end, step):
        noteindex = i + 9
        noteinfo = getNote(noteindex)
        freq = 2**(i/12) * 440 # Hz
        result.append((noteinfo[1], noteinfo[0], freq))
    return result

# works
#print(getNote(15))

upList = getListFromATo(0, 26, 1)
for x in reversed(upList):
    print(x, ",") 

downlist = getListFromATo(0, -34, -1)
for x in downlist:
    print(x, ",") 