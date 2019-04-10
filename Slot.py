#!/usr/bin/env python3
"""
.. module:: Slot
   :platform: Mac, Unix, Windows
   :synopsis: Slot object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import mido
import Note
import Scale
import random
import Constants as const

# Slot object. Capsule to hold item in phrase
# (note/rest) of various lengths and pitches.
class Slot():
    # Default ctor for Slot
    def __init__(self, note, length, length_mod, prob=1):
        """Default constructor for Slot. 
        
        :param note: Note object to hold within slot 
        :param length: Length to play slot 
        :param length_mod: Modifier for length 
        :param prob: Probability that Slot is triggered 
        
        :type note: Note 
        :type length: float 
        :type length_mod: int
        :type prob: float 

        :return: Returns a Slot object
        :rtype: Slot 
        """
        self.note = note
        self.length = length
        self.length_mod = length_mod
        self.prob = prob
    
    # Copy ctor for Slot
    @staticmethod
    def copy_ctor(slot):
        """Static copy constructor for Slot. 
        
        :param slot: Slot object to copy 
        
        :type slot: Slot 

        :return: Returns a Slot object, copy of slot
        :rtype: Slot 
        """
        return Slot(slot.note, slot.length, slot.length_mod, slot.prob)
           
    # Get random note from scale and random rhythm value
    def rand(self, scale, custom_len_list=None, custom_len_mod_list=None):
        """Class method to randomize note and rhythm values of Slot. 
        
        :param scale: Scale object to pick random note from 
        :param custom_len_list: Optional list of custom length values 
        :param custom_len_mod_list: Optional list of custom length modifier values 
        
        :type scale: Scale 
        :type custom_len_list: List of Strings 
        :type custom_len_mod_list: List of Strings 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.rand_note(scale)
        self.rand_rhythm(custom_len_list, custom_len_mod_list)
        return self

    # Get random note from scale
    def rand_note(self, scale):
        """Class method to get random note from scale. 
        
        :param scale: Scale object to pick random note from 
        
        :type scale: Scale 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.note = random.choice(scale.notes)
        return self

    # Get random rhythm value
    def rand_rhythm(self, custom_len_list=None, custom_len_mod_list=None):
        """Class method to randomize rhythm value of Slot. 
        
        :param custom_len_list: Optional list of custom length values 
        :param custom_len_mod_list: Optional list of custom length modifier values 
        
        :type custom_len_list: List of Strings 
        :type custom_len_mod_list: List of Strings 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Get random rhythm from class dict or custom dict
        if custom_len_list is None:
            self.length = random.choice(const.SLOT_LEN_DICT)
        else:
            self.length = random.choice(custom_len_list)

        # Get random rhythm mod from class dict or custom dict
        if custom_len_mod_list is None:
            self.length_mod = random.choice(list(const.SLOT_LEN_MOD_DICT.values()))
        else:
            self.length_mod = random.choice(custom_len_mod_list)

        return self

    # Mutate note and rhythm value
    def mutate(self, scale, prob=1, custom_len_list=None, custom_len_mod_list=None):
        """Class method to mutate note and rhythm values of Slot. 
        
        :param scale: Scale object to pick random note from
        :param prob: Probability that Slot is mutated
        :param custom_len_list: Optional list of custom length values 
        :param custom_len_mod_list: Optional list of custom length modifier values 
        
        :type scale: scale
        :type prob: int
        :type custom_len_list: List of Strings 
        :type custom_len_mod_list: List of Strings 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.mutate_note(scale, prob)
        self.mutate_rhythm()
        return self

    # Mutate note based on scale (returns adjacent note in scale)
    def mutate_note(self, scale, prob=1, threshold=0.5):
        """Class method to mutate note value of Slot. 
        
        :param scale: Scale object to pick random note from
        :param prob: Probability that Slot is mutated
        :param threshold: Probability of mutating note up or down

        :type scale: scale
        :type prob: int
        :type threshold: int

        :return: No return, modifys existing object 
        :rtype: None 
        """

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
        """WORK IN PROGRESS - Class method to mutate rhythm value of Slot. 
        
        :param prob: Probability that Slot is mutated
        :param custom_len_list: Optional list of custom length values 
        :param custom_len_mod_list: Optional list of custom length modifier values 
        
        :type prob: int
        :type custom_len_list: List of Strings 
        :type custom_len_mod_list: List of Strings 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        return self

    # Set note and rhythm value
    def set(self, note, length, length_mod):
        """Class method to set note and rhythm value of Slot. 
        
        :param note: Note to set Slot to 
        :param length: Length to set Slot to 
        :param length_mod: Length mod to set Slot to 
        
        :type note: Note 
        :type length: String 
        :type length_mod: String 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.set_note(note)
        self.set_rhythm(length, length_mod)
        return self

    # Set note
    def set_note(self, note):
        """Class method to set note value of Slot. 
        
        :param note: Note to set Slot to 
        
        :type note: Note 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.note = note
        return self

    # Set rhythm value
    def set_rhythm(self, length, length_mod):
        """Class method to set rhythm value of Slot. 
        
        :param length: Length to set Slot to 
        :param length_mod: Length mod to set Slot to 
        
        :type length: String 
        :type length_mod: String 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.length = length
        self.length_mod = const.SLOT_LEN_MOD_DICT.get(length_mod)
        return self
