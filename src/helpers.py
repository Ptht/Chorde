import pygame 
from noteTransformer import NoteTranformer

def printDeviceInfos():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s, name :%s, opened :%s  %s"
            % (i, interf, name, opened, in_out)
        )

def tranformMidi2Events(midiInput):
    if midiInput.poll():
        midi_events = midiInput.read(10)
        # convert them into pygame events.
        midi_evs = pygame.midi.midis2events(midi_events, midiInput.device_id)

        for m_e in midi_evs:
            pygame.event.post(m_e)

notes = [ "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
flatNotes = [ "c", u"d♭", "d", u"e♭", "e", "f", u"g♭", "g", u"a♭", "a", u"b♭", "b"]