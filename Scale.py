#!/usr/bin/env python3
"""
.. module:: Scale
   :platform: Mac, Unix, Windows
   :synopsis: Scale object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import Note
import Constants as const

# Scale object. Is an array of Notes
class Scale():
    # Default constructor for Scale. Takes in mode and key
    def __init__(self, key, mode, starting_octave=None):
        """Default constructor for Scale. Assigns starting pitch in 3rd octave.
        
        :param key: Key of scale
        :param mode: Mode of scale
        :param starting_octave: Starting octave of scale 
        
        :type key: String / int
        :type mode: String
        :type starting_octave: int / None

        :return: Returns a Scale object
        :rtype: Scale 
        """
        # Initialize output paramaters for lookup/calculation functions
        self.intervals = []
        #self.is_major = False
        #self.is_minor = False
        self.has_sharps = False
        self.has_flats = False
        self.notes = []

        # Assign mode and determine major/minor
        self.mode = mode
        self.is_major, self.is_minor = self.get_major_minor(self.mode)
        self.starting_octave = starting_octave

        # Assign key
        if (isinstance(key, str)):
            if (starting_octave is None):
                raise ValueError("Starting octave not specified for scale")
            else:
                self.key = self.get_midi(key, starting_octave)
        else:
            self.key = key

        # Assign sharps/flats
        #self.has_sharps, self.has_flats = self.get_sharps_flats(self.key)
        
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
        return (starting_octave + 2) * const.MIDI_KEY_DICT[key]

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

    '''
    # Class method to determine if scale has sharps or flats
    def get_sharps_flats(self, key):
        """Class method to determine if scale has sharps or flats.
        
        :param key: Key of scale
        
        :type key: String

        :return: Pair of booleans (#1 Sharps, #2 Flats)
        :rtype: booleans
        """
        # Assign sharp_flat_dict based on if major or minor
        if self.is_major:
            # Major sharp/flat dict
            sharp_flat_dict = const.MAJOR_SHARP_FLAT_DICT
        else:
            # Minor sharp/flat dict
            sharp_flat_dict = const.MINOR_SHARP_FLAT_DICT

        # Check for key in sharp_flat_dict
        if key in sharp_flat_dict:
            if sharp_flat_dict[key] == 's':
                # Has sharps
                # 1: Sharps, 2: Flats
                return True, False
            else:
                # Has flats
                # 1: Sharps, 2: Flats
                return False, True
    '''

    # Class method to build scale
    def build_scale(self):
        """Method to build scale - called by __init__. 
       
        :return: Scale object
        :rtype: Scale object 
        """
        scale = []
        scale_degree = self.key
        for interval in self.intervals:
            if 0 <= scale_degree <= 127:
                scale.append(Note.Note(scale_degree, 100, const.NOTE_LEN_DICT[4],
                const.NOTE_LEN_MOD_DICT["NONE"])) 
            scale_degree += interval
        if 0 <= scale_degree <= 127:
            scale.append(Note.Note(scale_degree, 100, const.NOTE_LEN_DICT[4],
                const.NOTE_LEN_MOD_DICT["NONE"])) 
        return scale

    # String representation of Scale.
    def __str__(self):
        """Utility function to print Scale.
       
        :return: String representation of Scale
        :rtype: String 
        """
        print("<Scale: key: %s, mode: %s>" % (self.key, self.mode))
        for note in self.notes:
            print("\t", note)

        return ""

    def __len__(self):
        """Utility function to get length of Scale.
       
        :return: Length of Scale object
        :rtype: int
        """
        return len(self.notes)
