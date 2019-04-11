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
test_note = Note.Note(60)
rand_note = Note.Note()
copy_note = Note.Note.copy_note(test_note)

print(test_note)
print(rand_note)
print(copy_note)
copy_note.set(40, const.NOTE_LEN_DICT[4], const.NOTE_LEN_MOD_DICT['NONE'])
print(test_note)
print(rand_note)
print(copy_note)
"""
test_scale = Scale.Scale("A", 'HARM_MINOR', 3)
test_phrase = Phrase.Phrase(120)
#print(str(test_scale))

# Populate Phrase
for i in range(len(test_scale)):
    test_slot = Slot.Slot(test_note, SLOT_LEN_DICT[4],
            SLOT_LEN_MOD_DICT["NONE"])
    test_slot.rand_note(test_scale)
    test_phrase.append(test_slot)

# Copy phrase and mutate
mutate_phrase = Phrase.Phrase.copy_ctor(test_phrase)
for slot in mutate_phrase.phrase:
    slot.mutate_note(test_scale, 0.5)

print("Phrase 1")
test_phrase.play()

print("Phrase 2")
#mutate_phrase.play()
"""
