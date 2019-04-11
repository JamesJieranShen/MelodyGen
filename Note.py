#!/usr/bin/env python3
"""
.. module:: Note
   :platform: Mac, Unix, Windows
   :synopsis: Note object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import Constants as const

# Base note object. Has Name of pitch and MIDI value.
class Note():

    def __init__(self, note=None, vel=100, length=None, length_mod=None, prob=1):
        """Default constructor for Note. Assigns random pitch and length if not 
        specified.
        
        :param note: MIDI note value 
        :param vel: Velocity of note
        :param length: Length of note
        :param length_mod: Rhythm modifier (dotted, triplet, etc.)
        :param prob: Probability that note is triggered 
        
        :type note_name: int
        :type vel: int
        :type length: float 
        :type length_mod: float 
        :type vel: int

        :return: Returns a Note object
        :rtype: Note 
        """
        # Check for note_name
        if note is None:
            # Assign random note
            self.rand_note()
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

    # Get random note from scale and random rhythm value
    def rand(self, scale, custom_len_list=None, custom_len_mod_list=None):
        """Class method to randomize note and rhythm values of Note. 
        
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
        self.rand_length(custom_len_list)
        self.rand_length_mod(custom_len_mod_list)
        return self

    # Class method to return random note
    def rand_note(self, scale=None, threshold=0.5):
        """Method to get random note. 
       
        :param scale: Optional scale to choose random note from
        :param threshold: Threshold for sharps (0) vs flats (1)
       
        :type scale: Scale
        :type threshold: float

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # If scale was passed in, choose note from scale
        if (scale not None):
            self.note = random.choice(scale.notes)
            return self
        else
            # Randomly determine sharps or flats (default is 50/50)
            if (random.random() > threshold)
                note_dict = const.NOTE_DICT_SHARPS
            else
                note_dict = const.NOTE_DICT_FLATS

        # Get random note
        self.note = random.choice(note_dict)
        return self

    # Get random length value
    def rand_length(self, custom_len_list=None):
        """Class method to randomize length value of Note. 
        
        :param custom_len_list: Optional list of custom length values 
        
        :type custom_len_list: List of Strings 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Get random rhythm from class dict or custom dict
        if custom_len_list is None:
            self.length = random.choice(const.SLOT_LEN_DICT)
        else:
            self.length = random.choice(custom_len_list)
        
        return self

    # Get random length mod value
    def rand_length_mod(self, custom_len_mod_list=None):
        """Class method to randomize rhythm value of Note. 
        
        :param custom_len_mod_list: Optional list of custom length modifier values 
        
        :type custom_len_mod_list: List of Strings 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Get random rhythm mod from class dict or custom dict
        if custom_len_mod_list is None: 
            self.length_mod = random.choice(list(const.SLOT_LEN_MOD_DICT.values()))
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

    # String representation of Note.
    def __str__(self):
        """Utility function to print Note.
       
        :return: String representation of Note
        :rtype: String 
        """
        return "<Note: name: %d, vel: %d>, length: %f, length_mod: %f,
            prob: %f" % (self.note, self.vel, self.length, self.length_mod,
            self.prob)
