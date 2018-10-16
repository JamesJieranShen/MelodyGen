#!/usr/bin/env python3

import Note as note
import Scale as scale
import Slot as slot
import MIDIHandler as handler
import Phrase as phrase
import mido
import time
import random
import copy

# Constant slot dictionaries
SLOT_TYPE_DICT = ["NOTE", "REST"]
SLOT_LEN_DICT = [1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1, 2]
SLOT_LEN_MOD_DICT = {"NONE": 1, "TRIPLET": 2/3, "DOTTED": 1.5}

# Phrase building
test_note = note.Note("C")
scale = scale.Scale("A", 'HARM_MINOR', 3)
test_phrase = phrase.Phrase(120)
#print(str(scale))


# Populate Phrase
for i in range(len(scale)):
    test_slot = slot.Slot(test_note, SLOT_LEN_DICT[4],
            SLOT_LEN_MOD_DICT["NONE"])
    test_slot.rand_note(scale)
    test_phrase.append(test_slot)

test_phrase.play()
