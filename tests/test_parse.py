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

# Initalize phrase
phrase = gen.Phrase(tempo=500, debug=True, endless=True, length=400)

# Load file from midi
# phrase.parse_midi("./midi_songs/cosmo.mid")

# Save phrase to file
# phrase.to_file("./tests/cosmo.song")

# Load phrase from file
phrase.from_file("./tests/output.song")
# phrase.resize()
# phrase.length += 1
# phrase.normalize_offset()
# phrase.quantize(division=1, quantize_length=True)
print(phrase)
phrase.play()

# phrase.resize()
# print(phrase.length)

# while True:
#     # for note in phrase.phrase:
#     #     note.set_length(1 / 8)

#     phrase.play()
