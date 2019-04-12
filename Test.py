#!/usr/bin/env python3
import Note
import Scale
import Slot
import Phrase
import MIDIHandler as handler
import mido
import time
import random
import Constants as const

# Phrase building
test_scale = Scale.Scale("A", 'HARM_MINOR', 3)
test_phrase = Phrase.Phrase(120)

# Populate Phrase
for i in range(len(test_scale)):
    test_note = Note.Note(60, 1/4, 1)
    test_note.rand_note(test_scale)
    #print(test_note.prob)
    #print(test_note)
    test_phrase.append(test_note)

'''
# Copy phrase and mutate
mutate_phrase = Phrase.Phrase.copy_ctor(test_phrase)
for slot in mutate_phrase.phrase:
    slot.mutate_note(test_scale, 0.5)
'''
print("Phrase 1")
test_phrase.play()
print("done")
'''
print("Phrase 2")
#mutate_phrase.play()
'''
