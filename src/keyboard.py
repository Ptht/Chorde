
class KeyBoard():
    def __init__(self, lowC :int, midC :int, down :int, up :int):
        self.lowC = lowC
        self.midC = midC
        self.down = down
        self.up = up

        self.playedKeys : list[tuple[int, str]] = []
    
    def keyUp(self, keyInfo :tuple[int, str]):
        if keyInfo in self.playedKeys:
            self.playedKeys.remove(keyInfo)

    def keyDown(self, keyInfo :tuple[int, str]):
        if keyInfo not in self.playedKeys:
            self.playedKeys.append(keyInfo)

    def clear(self):
        self.playedKeys.clear()