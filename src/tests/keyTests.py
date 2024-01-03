from key import Key, NoteType, KeyType

keyCMajor = Key("c", NoteType.NATURAL, KeyType.MAJOR)

expectedC = ["c", "d", "e", "f", "g", "a", "b"]

notes = keyCMajor.getNotes()
print("C:")
print(notes)
print(expectedC)

if set(expectedC) != set(notes):
    raise Exception("key.getnotes returned false notes!")

keyDMajor = Key("d", NoteType.NATURAL, KeyType.MAJOR)

expectedD = ["d", "e", "f#", "g", "a", "b", "c#"]

notes = keyDMajor.getNotes()
print("D:")
print(notes)
print(expectedD)

if set(expectedD) != set(notes):
    raise Exception("key.getnotes returned false notes!")
