#!/usr/bin/env python3

import random
import time
import mido
import Note as note
import Scale as scale
import Slot as slot
import MIDIHandler as handler

# Constant slot dictionaries
SLOT_TYPE_DICT = ["NOTE", "REST"]
SLOT_LEN_DICT = [1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1, 2]
#SLOT_LEN_MOD_DICT = ["NONE", "TRIPLET", "DOTTED"]
SLOT_LEN_MOD_DICT = {"NONE": 1, "TRIPLET": 2/3, "DOTTED": 1.5}

# Phrase object. Is an array of Slots.
class Phrase():
    
    def __init__(self, tempo=120, debug=False):
        self.phrase = []
        self.tempo = tempo
        self.debug = debug
        self.handler = handler.MIDIHandler(tempo, debug)
    
    # Utility method to play phrase
    def play(self):
        for slot in self.phrase:
            trig = False
            if (random.random() <= slot.prob):
                trig = True
            if trig: self.handler.note_on(slot)
            time.sleep((240 * slot.length * slot.length_mod) / self.tempo)
            if trig: self.handler.note_off(slot)

    # Build phrase
    def generate_phrase(self):
        '''
        # Manual phrase building
        phrase1 = []
        phrase2 = []
        print("run")
        test_note = note.Note("C")
        scale = scale.Scale("A", 'HARM_MINOR', 3)
        handler = handler.MIDIHandler(100)
        '''

    # Set phrase
    def set_phrase(self, phrase):
        self.phrase = phrase

    # Copy ctor for Phrase
    @staticmethod
    def copy_ctor(phrase):
        new_phrase = []
        for slot in phrase.phrase:
            new_phrase.append(slot.Slot.copy_ctor(slot))

        return new_phrase 

    # Append to Phrase
    def append(self, input_slot):
        input_slot = slot.Slot.copy_ctor(input_slot)
        self.phrase.append(input_slot)

    # Str representation of Phrase
    def __str__(self):
        return ("<Note: phrase_length: {}, tempo: {}, debug: {}>".format(
                len(self.phrase), self.tempo, self.debug))
