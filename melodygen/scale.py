#!/usr/bin/env python3
"""
.. module:: scale
   :platform: Mac, Unix, Windows
   :synopsis: Scale object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
from note import Note
import constants as const

# Scale object. Is an array of Notes
class Scale:
    # Default constructor for Scale. Takes in mode and key
    def __init__(self, key, mode, starting_octave=None, num_octaves=1):
        """Default constructor for Scale. Assigns starting pitch in 3rd octave.
        
        :param key: Key of scale
        :param mode: Mode of scale
        :param starting_octave: Starting octave of scale 
        :param num_octaves: Number of octaves in Scale 

        :type key: String / int
        :type mode: String
        :type starting_octave: int / None
        :type num_octaves: int

        :return: Returns a Scale object
        :rtype: Scale 
        """
        # Initialize output paramaters for lookup/calculation functions
        self.intervals = []
        self.is_major = False
        self.is_minor = False
        self.notes = []

        # Assign mode and determine major/minor
        self.mode = mode
        self.is_major, self.is_minor = self.get_major_minor(self.mode)
        self.starting_octave = starting_octave
        self.num_octaves = num_octaves

        # Assign key
        if isinstance(key, str):
            if starting_octave is None:
                raise ValueError("Starting octave not specified for scale")
            else:
                self.key = self.get_midi(key, starting_octave)
        else:
            self.key = key

        # Lookup/calculate intervals, major/minor, sharps/flats
        self.intervals = Scale.get_intervals(self.mode)

        # Build scale
        self.notes = self.build_scale()

    # Method to get MIDI value of note based on note name and starting octave
    def get_midi(self, key, starting_octave):
        """Method to get MIDI note value based on
        note name and starting octave.
        
        :param key: Note name of key 
        :param starting_octave: Starting octave of scale 
        
        :type key: String
        :type starting_octave: int

        :return: MIDI value of note 
        :rtype: int 
        """
        return (starting_octave + 2) * 12 + const.MIDI_KEY_DICT[key]

    # Static method to get scale intervals based on mode
    @staticmethod
    def get_intervals(mode):
        """Static method to get scale intervals based on mode.
        
        :param mode: Mode of scale
        
        :type mode: String

        :return: List of intervals 
        :rtype: List of ints 
        """
        return const.SCALE_DICT[mode.upper()]

    # Class method to determine if mode is major or minor
    def get_major_minor(self, mode):
        """Class method to determine if mode is major or minor.
        
        :param mode: Mode of scale
        
        :type mode: String

        :return: Pair of booleans (#1 Major, #2 Minor)
        :rtype: booleans
        """
        if mode in const.MAJOR_MODE_DICT:
            # 1: Major, 2: Minor
            return True, False
        else:
            # 1: Major, 2: Minor
            return False, True

    # Class method to build scale
    def build_scale(self):
        """Method to build scale - called by __init__. 
       
        :return: Scale object
        :rtype: Scale object 
        """
        scale = []
        scale_degree = self.key
        for i in range(self.num_octaves):
            for interval in self.intervals:
                if 0 <= scale_degree <= 127:
                    scale.append(
                        Note(
                            scale_degree,
                            100,
                            const.NOTE_LEN_DICT[4],
                            const.NOTE_LEN_MOD_DICT["NONE"],
                        )
                    )
                scale_degree += interval
        if 0 <= scale_degree <= 127:
            scale.append(
                Note(
                    scale_degree,
                    100,
                    const.NOTE_LEN_DICT[4],
                    const.NOTE_LEN_MOD_DICT["NONE"],
                )
            )
        return scale

    # Class method to get scale degree of Scale
    def get_scale_degree(self, degree):
        """Utility function to return scale degree of Scale.
       
        :param degree: Scale degree to return

        :type degree: int
        
        :return: Note object at scale degree 
        :rtype: Note 
        """
        return Note.copy_note(self.notes[degree - 1])

    # String representation of Scale.
    def __str__(self):
        """Utility function to print Scale.
       
        :return: String representation of Scale
        :rtype: String 
        """
        print(
            "<Scale: key: %s, mode: %s, num_octaves: %d>"
            % (self.key, self.mode, self.num_octaves)
        )
        for note in self.notes:
            print("\t", note)

        return ""

    def __len__(self):
        """Utility function to get length of Scale.
       
        :return: Length of Scale object
        :rtype: int
        """
        return len(self.notes)
