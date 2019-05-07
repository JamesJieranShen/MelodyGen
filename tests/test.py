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
e = gen.Scale("E", "MAJOR", 3, 3)
g = gen.Scale("G", "MAJOR", 3, 3)
c = gen.Scale("C", "MAJOR_PENT", 4, 2)
d = gen.Scale("D", "HARM_MINOR", 4, 2)

scales = [e, c, g, d]

# Vars
phrase_len = 16
play_len = 5
file_path = os.path.abspath("./melodygen/gen") + "/"

"""
# Notes
note = Note.Note(note = 60, vel = 100, length = 1/2, length_mod = 1, prob = 1)
handler = handler.MIDIHandler(tempo = 80);
handler.play_note(note);
note.pitch_shift(7);
handler.play_note(note);
"""

# Phrase
phrase = gen.Phrase(tempo=120, debug=True, endless=True, length=2)

clock = 0
for i in range(phrase_len):
    note_len = random.choice([1, 1.5, 2 / 3])
    phrase.append(
        clock,
        gen.Note(
            length=1 / 16, length_mod=note_len, scale=random.choice(scales), prob=1
        ),
    )
    clock += 1 / 16 * note_len

# phrase.generate_phrase(
#     "MapMod", {"input": file_path + "pi.txt", "scales": scales, "gen_len": 8}
# )

while True:
    phrase.play()
    # phrase.unify_prob()
    if random.random() < 0.2:
        if random.random() < 0.5:
            phrase.reverse()
            print("Reversed")
        else:
            phrase.flip()
            print("Flipped")
    for note in phrase.phrase:
        note.set_length(1 / 16)
        note.rand_note(scale=random.choice(scales), prob=0.15)
        note.mutate_length(prob=0.05)
"""

while(True):
    for note in phrase.phrase:
        #note.set_prob(0.8)
        if random.random() < 0.5:
            note.set_length(1/16)
        else:
            note.set_length(1/8)

    phrase.play()
"""
