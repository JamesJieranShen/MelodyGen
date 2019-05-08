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
phrase = gen.Phrase(tempo=120, debug=True, endless=True, length=400)

phrase.parse_midi("./midi_songs/cosmo.mid")

while True:
    # for note in phrase.phrase:
    #     note.set_length(1 / 8)

    phrase.play()
