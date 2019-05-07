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

# Scales
e = gen.Scale("E", "MAJOR", 2, 1)
g = gen.Scale("G", "MAJOR", 2, 3)
c = gen.Scale("C", "MAJOR_PENT", 3, 2)
d = gen.Scale("D", "HARM_MINOR", 3, 2)

scales = [e, c, g, d]

# Vars
phrase_len = 16
play_len = 5
file_path = os.path.abspath("./melodygen/gen") + "/"

# Phrase
phrase = gen.Phrase(tempo=120, debug=False, endless=True)


phrase.generate_phrase(
    "MapMod",
    {
        "input_file": file_path + "pi.txt",
        "scales": [e],
        "gen_len": 16,
        "start_offset": 1,
        "note_len": 1 / 16,
    },
)

phrase.resize()

while True:
    # for note in phrase.phrase:
    #     note.set_length(1 / 8)

    phrase.play()
