#!/usr/bin/env python3
import Note
import Scale
import Phrase
import MIDIHandler as handler
import mido
import time
import random
import Constants as const


# Scales 
a_harm_min = Scale.Scale("A", 'HARM_MINOR', 4)
c_min_pent = Scale.Scale("C", 'MINOR_PENT', 4)
g_phrygian = Scale.Scale("G", 'PHRYGIAN', 4)

scales = [a_harm_min, c_min_pent, g_phrygian]

for scale in scales:
    print(scale)

# Vars
phrase_len = 16
play_len = 5

# Phrase
phrase = Phrase.Phrase(120, True)

for i in range(phrase_len):
    phrase.append(Note.Note(length=1/16,
        length_mod=1, scale=a_harm_min, prob=0.8))

while(True):
    phrase.play()
    for note in phrase.phrase:
        note.rand_note(scale=random.choice(scales), prob=0.2)
        note.mutate_length(prob=0.01)
