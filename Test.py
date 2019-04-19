#!/usr/bin/env python3
import Note
import Scale
import Phrase
import MIDIHandler as handler
import Generate
import Constants as const
import mido
import time
import random

# Scales 
e = Scale.Scale("E", 'MAJOR', 3)
g = Scale.Scale("G", 'MAJOR', 3)
c = Scale.Scale("C", 'MAJOR_PENT', 4)

scales = [e, c, g]

"""
for scale in scales:
    print(scale)
"""
# Vars
phrase_len = 16
play_len = 5

"""
# Notes
note = Note.Note(note = 60, vel = 100, length = 1/2, length_mod = 1, prob = 1)
handler = handler.MIDIHandler(tempo = 80);
handler.play_note(note);
note.pitch_shift(7);
handler.play_note(note);
"""

# Phrase
phrase = Phrase.Phrase(120, True)

"""
for i in range(phrase_len):
    phrase.append(Note.Note(length=1/16,
        length_mod=random.choice([1, 1.5, 2/3]), scale=random.choice(scales), prob=0.8))

while(True):
    phrase.play()
    #phrase.unify_prob()
    if random.random() < 0.2:
        if random.random() < 0.5:
            phrase.reverse()
            print("Reversed")
        else:
            phrase.flip();
            print("Flipped")
    for note in phrase.phrase:
        note.rand_note(scale=random.choice(scales), prob=0.15)
        note.mutate_length(prob=0.05)
"""

print(e.get_scale_degree(1))
phrase.generate_phrase("MapMod", {"scale": e, "index": 5})
print(phrase)
phrase.generate_phrase("MapMod", {"scale": g})
print(phrase)
