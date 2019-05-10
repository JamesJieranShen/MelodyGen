#!/usr/bin/env python3
from context import melodygen as gen
from melodygen import (
    Note,
    Scale,
    Phrase,
    MIDIHandler as handler,
    Generate,
    constants as const,
)
import mido
import time
import random
import os

# Phrase
phrase = gen.Phrase(tempo=200, debug=True, endless=True, length=400)

counter = 0
note_len = 1 / 4
for i in range(4):
    phrase.append(counter, Note(note=60, length=note_len, length_mod=1))
    counter += note_len

# phrase.parse_midi("./midi_songs/cosmo.mid")

# phrase.quantize(division=1, quantize_length=True)


phrase.resize()
print(phrase.length)

while True:
    # for note in phrase.phrase:
    #     note.set_length(1 / 8)

    phrase.play()
