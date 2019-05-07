#!/usr/bin/env python3
"""
.. module:: note
   :platform: Mac, Unix, Windows
   :synopsis: Note object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
from fractions import Fraction
import constants as const

# Base note object. Has Name of pitch and MIDI value.
class Note:
    def __init__(
        self,
        note=None,
        vel=100,
        length=None,
        length_mod=None,
        prob=1,
        scale=None,
        accented=False,
    ):
        """Default constructor for Note. Assigns random pitch and length if not 
        specified.
        
        :param note: MIDI note value 
        :param vel: Velocity of note
        :param length: Length of note
        :param length_mod: Rhythm modifier (dotted, triplet, etc.)
        :param prob: Probability that note is triggered 
        :param scale: Scale to choose random notes from

        :type note_name: int
        :type vel: int
        :type length: float 
        :type length_mod: float 
        :type vel: int
        :type scale: Scale

        :return: Returns a Note object
        :rtype: Note 
        """
        # Check for note_name
        if note is None:
            # Assign random note
            self.rand_note(scale)
        else:
            # Assign inputted note
            self.note = note

        # Set note velocity
        self.vel = vel

        # Check for length
        if length is None:
            # Assign random rhythm
            self.rand_length()
        else:
            # Assign inputted rhythm
            self.length = length

        # Check for length_mod
        if length_mod is None:
            # Assign random length mod
            self.rand_length_mod()
        else:
            # Assign inputted length mod
            self.length_mod = length_mod

        # Set note probability
        self.prob = prob

        # Set note accent
        self.accented = accented

    # Copy ctor for Note
    @staticmethod
    def copy_note(note):
        """Static copy constructor for Note. 
        
        :param note: Note object to copy 
        
        :type note: Note 

        :return: Returns a Note object, copy of note 
        :rtype: Note 
        """
        return Note(note.note, note.vel, note.length, note.length_mod, note.prob)

    # Get random note from scale and random rhythm value
    def rand(self, scale, custom_len_list=None, custom_len_mod_list=None, prob=1):
        """Class method to randomize note and rhythm values of Note. 
        
        :param scale: Scale object to pick random note from 
        :param custom_len_list: Optional list of custom length values 
        :param custom_len_mod_list: Optional list of custom length modifier values 
        :param prob: Probability that note is randomized 

        :type scale: Scale 
        :type custom_len_list: List of floats 
        :type custom_len_mod_list: Dict of floats 
        :type prob: float

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.rand_note(scale)
        self.rand_length(custom_len_list)
        self.rand_length_mod(custom_len_mod_list)
        return self

    # Class method to return random note
    def rand_note(self, scale=None, prob=1):
        """Method to get random note. 
       
        :param scale: Optional scale to choose random note from
        :param threshold: Threshold for sharps (0) vs flats (1)
        :param prob: Probability that note is randomized

        :type scale: Scale
        :type threshold: float
        :type prob: floats

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Don't randomize if random prob is larger than prob
        if random.random() > prob:
            return self

        # If scale was passed in, choose note from scale
        if scale is not None:
            self.note = random.choice(scale.notes).note
        else:
            self.note = random.randint(0, 127)
        return self

    # Get random length value
    def rand_length(self, custom_len_list=None, prob=1):
        """Class method to randomize length value of Note. 
        
        :param custom_len_list: Optional list of custom length values 
        :param prob: Probability that note is randomized

        :type custom_len_list: List of floats 
        :type prob: float

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Don't randomize if random prob is larger than prob
        if random.random() > prob:
            return self

        # Get random rhythm from class dict or custom dict
        if custom_len_list is None:
            self.length = random.choice(const.NOTE_LEN_DICT)
        else:
            self.length = random.choice(custom_len_list)
        return self

    # Get random length mod value
    def rand_length_mod(self, custom_len_mod_list=None, prob=1):
        """Class method to randomize rhythm value of Note. 
        
        :param custom_len_mod_list: Optional list of custom length modifier values 
        :param prob: Probability that note is randomized

        :type custom_len_mod_list: List of Strings 
        :type prob: floats

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Don't randomize if random prob is larger than prob
        if random.random() > prob:
            return self

        # Get random rhythm mod from class dict or custom dict
        if custom_len_mod_list is None:
            self.length_mod = random.choice(list(const.NOTE_LEN_MOD_DICT.values()))
        else:
            self.length_mod = random.choice(custom_len_mod_list)

        return self

    # Utility function to get note midi value
    def get_note(self):
        """Utility function to get note midi value.
       
        :return: Returns Note midi value
        :rtype: int 
        """
        return self.note

    # Mutate note and rhythm value
    def mutate(
        self,
        scale,
        custom_len_list=None,
        custom_len_mod_list=None,
        prob=1,
        threshold=0.5,
    ):
        """Class method to mutate note and rhythm values of Note. 
        
        :param scale: Scale object to pick random note from
        :param prob: Probability that Note is mutated
        :param custom_len_list: Optional list of custom length values 
        :param custom_len_mod_list: Optional list of custom length modifier
            values 
        
        :type scale: scale
        :type prob: float
        :type custom_len_list: List of floats 
        :type custom_len_mod_list: Dict of floats 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.mutate_note(scale, prob, threshold)
        self.mutate_length(custom_len_list, prob, threshold)
        self.mutate_length_mod(custom_len_mod_list, prob)
        # self.mutate_prob()
        return self

    # Mutate note based on scale (returns adjacent note in scale)
    def mutate_note(self, scale, prob=1, threshold=0.5):
        """Class method to mutate note value of Note. 
        
        :param scale: Scale object to pick random note from
        :param prob: Probability that Note is mutated
        :param threshold: Probability of mutating note up or down

        :type scale: Scale
        :type prob: float
        :type threshold: float

        :return: No return, modifys existing object 
        :rtype: None 
        """

        # Don't mutate if random prob is larger than prob
        if random.random() > prob:
            return self

        # Get index of note in Scale
        for index, note in enumerate(scale.notes):
            if self.note == note.note:
                scale_index = index
                break
            else:
                scale_index = -1

        # Raise error if note is not in scale
        if scale_index == -1:
            raise ValueError("Note not in scale for mutate_note")

        # If the first element, return next value
        if scale_index == 0:
            self.note = scale.notes[scale_index + 1].note

        # If the last element, return prev value
        elif scale_index == len(scale.notes) - 1:
            self.note = scale.notes[scale_index - 1].note

        # Else, return next or prev value based on threshold
        else:
            if random.random() >= threshold:
                self.note = scale.notes[scale_index + 1].note
            else:
                self.note = scale.notes[scale_index - 1].note
        return self

    # Mutate length value
    def mutate_length(self, custom_len_list=None, prob=1, threshold=0.5):
        """Class method to mutate length value of Note. 
        
        :param custom_len_list: Optional list of custom length values 
        :param prob: Probability that Note is mutated
        :param threshold: Determines whether length is mutated more up \ 
            or down
        
        :type custom_len_list: List of floats 
        :type prob: float
        :type threshold: float

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Don't mutate if random prob is larger than prob
        if random.random() > prob:
            return self

        # Get list of length values to mutate from
        len_list = []
        if custom_len_list is None:
            len_list = const.NOTE_LEN_DICT
        else:
            len_list = custom_len_list

        # Get index of note in Scale
        for index, length in enumerate(len_list):
            if self.length == length:
                len_index = index
                break
            else:
                len_index = -1

        # Raise error if rhythm is not in list
        if len_index == -1:
            raise ValueError("Length not in list for mutate_length")

        # If the first element, return next value
        if len_index == 0:
            self.length = len_list[len_index + 1]

        # If the last element, return prev value
        elif len_index == len(len_list) - 1:
            self.length = len_list[len_index - 1]

        # Else, return next or prev value based on threshold
        else:
            if random.random() >= threshold:
                self.length = len_list[len_index + 1]
            else:
                self.length = len_list[len_index - 1]
        return self

    # Mutate length mod value
    def mutate_length_mod(self, custom_len_mod_list=None, prob=1):
        """Class method to mutate length mod value of Note using
            rand_length_mod. 
        
        :param prob: Probability that Note is mutated
        :param custom_len_mod_list: Optional list of custom length modifier
            values 
        
        :type prob: float
        :type custom_len_mod_list: Dict of floats 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Don't mutate if random prob is larger than prob
        if random.random() > prob:
            return self

        old_length_mod = self.length_mod
        while self.length_mod == old_length_mod:
            self.rand_length_mod(custom_len_mod_list)
        return self

    # Set note and rhythm value
    def set(self, note, length, length_mod, prob=None):
        """Class method to set note and rhythm value of Note. 
        
        :param note: MIDI value to set Note to 
        :param length: Length to set Note to 
        :param length_mod: Length mod to set Note to 
        
        :type note: int
        :type length: float 
        :type length_mod: float 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.set_note(note)
        self.set_length(length)
        self.set_length_mod(length_mod)
        self.set_prob(prob)
        return self

    # Set note
    def set_note(self, note):
        """Class method to set note value of Note. 
        
        :param note: MIDI value to set Note to 
        
        :type note: int 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.note = note
        return self

    # Set length value
    def set_length(self, length):
        """Class method to set length value of Note. 
        
        :param length: Length to set Note to 
        
        :type length: float 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.length = length
        return self

    # Set length mod value
    def set_length_mod(self, length_mod):
        """Class method to set length mod value of Note. 
        
        :param length_mod: Length mod to set Note to 
        
        :type length_mod: float 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.length_mod = length_mod
        return self

    # Set prob value
    def set_prob(self, prob=None):
        """Class method to set probability of Note. 
        
        :param prob: Probability that Note is triggered 
        
        :type prob: float 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        if prob is None:
            self.prob = 1
        else:
            self.prob = prob
        return self

    def is_valid(self):
        """Class method to determine whether the note is a valid midi note.
        
        :return: True if is valid, False otherwise
        :rtype: Boolean
        """
        if self.note is None:
            return False
        elif self.note > 127 or self.note < 0:  # Pitch check
            return False
        elif self.vel > 127 or self.vel < 0:  # velocity check
            return False
        elif self.length is None or self.length <= 0:  # length check
            return False
        elif self.length_mod <= 0 or self.length_mod >= 2:
            return False  # length_mod sanity
        elif prob > 1 or prob < 0:  # prob between 0 & 1
            return False
        else:
            return True

    # String representation of Note.
    def __str__(self):
        """Utility function to print Note.
       
        :return: String representation of Note
        :rtype: String 
        """
        return """<Note: note: %d, vel: %d, length: %s, length_mod: %s,
            prob: %.2f>""" % (
            self.note,
            self.vel,
            Fraction(self.length),
            Fraction(self.length_mod).limit_denominator(),
            self.prob,
        )

