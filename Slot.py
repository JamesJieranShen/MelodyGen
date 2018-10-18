#!/usr/bin/env python3

import mido
import Note
import Scale
#import MIDIHandler as handler
import random

# Slot object. Capsule to hold item in phrase
# (note/rest) of various lengths and pitches.
class Slot():

    # Constant slot dictionaries
    SLOT_TYPE_DICT = ["NOTE", "REST"]
    SLOT_LEN_DICT = [1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1, 2]
    SLOT_LEN_MOD_DICT = {"NONE": 1, "TRIPLET": 2/3, "DOTTED": 1.5}

    # Constant note/octave dictionaries
    NOTE_DICT_NUMKEY = [ 0,   1,    2,   3,    4,   5,   6,    7,   8,    9,   10,   11]
    NOTE_DICT_SHARPS = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]
    NOTE_DICT_FLATS  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    OCTAVES = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Default ctor for Slot
    def __init__(self, note, length, length_mod, prob=1):
        self.note = note
        self.length = length
        self.length_mod = length_mod
        self.prob = prob
    
    # Copy ctor for Slot
    @staticmethod
    def copy_ctor(slot):
        return Slot(slot.note, slot.length, slot.length_mod, slot.prob)
           
    # Get random note from scale and random rhythm value
    def rand(self, scale, custom_len_list=None, custom_len_mod_list=None):
        self.rand_note(scale)
        self.rand_rhythm(custom_len_list, custom_len_mod_list)
        return self

    # Get random note from scale
    def rand_note(self, scale):
        self.note = random.choice(scale.notes)
        return self

    # Get random rhythm value
    def rand_rhythm(self, custom_len_list=None, custom_len_mod_list=None):
        # Get random rhythm from class dict or custom dict
        if custom_len_list is None:
            self.length = random.choice(self.SLOT_LEN_DICT)
        else:
            self.length = random.choice(custom_len_list)

        # Get random rhythm mod from class dict or custom dict
        if custom_len_mod_list is None:
            self.length_mod = random.choice(list(self.SLOT_LEN_MOD_DICT.values()))
        else:
            self.length_mod = random.choice(custom_len_mod_list)

        return self

    # Mutate note and rhythm value
    def mutate(self, scale, prob=1):
        self.mutate_note(scale, prob)
        self.mutate_rhythm()
        return self

    # Mutate note based on scale (returns adjacent note in scale)
    def mutate_note(self, scale, prob=1, threshold=0.5):
        # Don't mutate if random prob is larger than prob
        if random.random() > prob:
            return self
        
        # Get index of note in Scale
        for index, note in enumerate(scale.notes):
            if self.note.note_name == note.note_name:
                if self.note.octave == note.octave:
                    scale_index = index
                    break
            else:
                scale_index = -1

        # Raise error if note is not in scale
        if scale_index == -1:
            raise ValueError("Note not in scale for mutate_note")

        # If the first element, return next value
        if scale_index == 0:
            self.note = scale.notes[scale_index + 1]

        # If the last element, return prev value
        elif scale_index == len(scale.notes) - 1:
            self.note = scale.notes[scale_index - 1]

        # Else, return next or prev value based on threshold
        else:
            if random.random() >= threshold:
                self.note = scale.notes[scale_index + 1]
            else:
                self.note = scale.notes[scale_index - 1]

        return self

    # Mutate rhythm value
    def mutate_rhythm(self):
        return self

    # Set note and rhythm value
    def set(self, note, length, length_mod):
        self.set_note(note)
        self.set_rhythm(length, length_mod)
        return self

    # Set note
    def set_note(self, note):
        self.note = note
        return self

    # Set rhythm value
    def set_rhythm(self, length, length_mod):
        self.length = length
        self.length_mod = self.SLOT_LEN_MOD_DICT.get(length_mod)
        return self
