import pyaudio
import numpy as np
import threading
from queue import Queue, Full
from array import array
import time
import matplotlib.pyplot as plt
from freq2note import *

# Multithreaded pyaudio implementation heavily inspired by
# https://stackoverflow.com/questions/19070290/pyaudio-listen-until-voice-is-detected-and-then-record-to-a-wav-file
# user Erik Kaplun

plt.interactive(True)

CHUNK_SIZE = 1024 * 8
MIN_VOLUME = 500
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 2
RATE = 44100
PERIOD = (1/RATE)*CHUNK_SIZE
FUNDAMENTALFREQ = 1/PERIOD
NYQUISTFREQ = FUNDAMENTALFREQ * CHUNK_SIZE / 2

def showFreqAmplPlot():
    plt.show()

    #data = resultDataQueue.get()
    data = []
    y = [y[1] for y in data]
    x = [x[0] for x in data]
    
    if max(y) > 600:
        plt.clf()
        #for i in range(1, int(CHUNK_SIZE / 256)):
        #    plt.plot(x[((i-1)*256):i*256], y[((i-1)*256):i*256])
        
        plt.xlim(0, 512)
        plt.xlabel('Frequency')
        plt.ylim(0, 1000)
        plt.ylabel('Amplitude')
        plt.plot(x, y)#, markersize=2, pickradius=1)
        #plt.plot(data)
    
    plt.pause(0.1)

def main():
    stopped = threading.Event()
    listenQueue = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
    freqQueue :Queue[int, list[float]] = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
    resultDataQueue :Queue[list[float, float]] = Queue(maxsize=2)

    listen_t = threading.Thread(target=listen, args=(stopped, listenQueue))
    listen_t.start()
    record_t = threading.Thread(target=process, args=(stopped, listenQueue, freqQueue, resultDataQueue))
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)

    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()

def listen(stopped :threading.Event, q :Queue):
    audio = pyaudio.PyAudio()
    print(audio.get_default_input_device_info())
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=2,
        rate=RATE,
        input=True,
        frames_per_buffer=1024,
    )

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            mv = memoryview(stream.read(CHUNK_SIZE)).cast('h')
            l = [x for x in mv][::2]
            q.put(l)
        except Full:
            pass  # discard


def useHistorySmoothing():
    avgCounter = 0
    history :list[list[float, float]] = [[] for i in range(3)]
    sums :list[list[float]] = []

    avgCounter = avgCounter + 1 if avgCounter < 3 else 0

    pairs = []
    avgCounter += 1
    sortedPairs = sorted(pairs, key=lambda x: x[1])
    
    for values in history:
        for pair in values:
            found : bool = False
            for s in sums:
                if pair[0] == s[0]:
                    s[1] += pair[1]
                    found = True
                    break

            if not found:
                sums.append([pair[0], pair[1]])

    sortedSums = sorted(sums, key=lambda x: x[1])
    history[avgCounter] = sortedPairs[-20:]
    pair = sortedSums[0]

def notesAndCounts():
    amplSortedPairs = []
    top = amplSortedPairs[-20:]
    noteFinder = ""

    noteInfos = []
    for x in top:
        info = noteFinder.getNote(x[0])
        if info is not None:
            noteInfos.append(info)

    notes = [x[0] for x in noteInfos]

    uniqueNotes = set(notes)

    notesAndCounts :list[str, int] = []
    for uNote in uniqueNotes:
        notesAndCounts.append((uNote, notes.count(uNote)))

    countSorted = sorted(notesAndCounts, key=lambda x: x[1])

    #freqSortedTop5 = sorted(top5, key=lambda x: x[0])

def process(stopped :threading.Event, queue :Queue[np.ndarray], result :Queue[int, list[int, float]], data:Queue[list[float, float]] ):
    counter :int = 0
    noteFinder = freq2note()

    while True:
        counter += 1
        chunkList = queue.get()

        a = np.array(chunkList)
        fftResult = np.fft.fft(a)
        frequencies = np.array([FUNDAMENTALFREQ*n if n<CHUNK_SIZE/2 else FUNDAMENTALFREQ*(n-CHUNK_SIZE) for n in range(CHUNK_SIZE)])
        amplitudes = 2 / CHUNK_SIZE * np.abs(fftResult) 
        pairs = [(abs(round(frequencies[i], 2)), abs(round(amplitudes[i], 2))) for i in range(CHUNK_SIZE)]

        try:
            #data.put(pairs)
            pass
        except Full:
            pass

        amplSortedPairs = sorted(pairs, key=lambda x: x[1])
        pair = amplSortedPairs[-1]

        if (pair[1] > 150):
            top = amplSortedPairs[-16:]

            topNotes = [x[0] for x in (noteFinder.getNote(f[0]) for f in top) if x is not None]
            print(f"top freq: {pair[0]} - {noteFinder.getNote(pair[0])}, - {topNotes}")
                  #({noteFinder.getNote(amplSortedPairs[-2][0])}, {noteFinder.getNote(amplSortedPairs[-3][0])})" )
    
    try:
        result.put((time.time_ns, fftResult.tolist()))
    except Full:
        pass
    
main()