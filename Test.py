#!/usr/bin/env python3
import Note
import Scale
import Phrase
import MIDIHandler as handler
import mido
import time
import random
import Constants as const


# Phrase building
#test_scale = Scale.Scale("A", 'HARM_MINOR', 3)
test_scale = Scale.Scale(60, "BLUES")
#test_phrase = Phrase.Phrase(120)
test_note = Note.Note.copy_note(test_scale.notes[1])

#print(test_scale)
print(test_note)

test_note.mutate_note(test_scale, 1, .1)
print(test_note)

test_note.mutate_note(test_scale)
print(test_note)

'''
# Populate Phrase
for i in range(len(test_scale)):
    test_note = test_scale.notes[i]
    #test_note.rand_note(test_scale)
    #print(test_note.prob)
    #print(test_note)
    test_phrase.append(test_note)

# Copy phrase and mutate
rev_phrase = Phrase.Phrase.copy_ctor(test_phrase)
rev_phrase.reverse()

print("Phrase 1")
test_phrase.play()
print("Phrase 2")
rev_phrase.play()
'''
