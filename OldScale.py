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
    def __init__(self, key, mode, starting_octave=const.OCTAVES[5]):
        """Default constructor for Scale. Assigns starting pitch in 3rd octave.
        
        :param key: Key of scale
        :param mode: Mode of scale
        :param starting_octave: Starting octave of scale 
        
        :type key: String
        :type mode: String
        :type starting_octave: int

        :return: Returns a Scale object
        :rtype: Scale 
        """
        # Assign mode and key
        self.key = key
        self.mode = mode
        self.starting_octave = starting_octave

        # Initialize output paramaters for lookup/calculation functions
        self.intervals = []
        self.is_major = False
        self.is_minor = False
        self.has_sharps = False
        self.has_flats = False
        self.notes = []

        # Lookup/calculate intervals, major/minor, sharps/flats
        self.intervals = Scale.get_intervals(self.mode)
        self.is_major, self.is_minor = self.get_major_minor(self.mode)
        self.has_sharps, self.has_flats = self.get_sharps_flats(self.key)

        # Build scale
        self.notes = self.build_scale()

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

    # Class method to create new note_dict starting with note of key
    def note_dict_offset(self, key, note_dict):
        """Class method to create new note_dict starting with note of key.
        
        :param key: Key of scale
        :param note_dict: Set of notes to rearrange 
        
        :type key: String
        :type note_dict: Dictionary of Note objects 

        :return: Rearranged note_dict
        :rtype: Dictionary of Note objects 
        """
        # Get index of key
        key_index = note_dict.index(key)

        # Splice and rearrange list at key_index
        return note_dict[key_index:] + note_dict[:key_index]

    # Class method to build scale
    def build_scale(self):
        """Method to build scale - called by __init__. 
       
        :return: Scale object
        :rtype: Scale object 
        """

        # Counter to add notes on
        count = 0

        # Counter to loop through all notes (for octave wrapping)
        full_count = 0

        # Counter to make sure loop ends
        list_index = 0

        # Initialize empty dicts
        reordered_note_dict = []
        working_note_dict = []

        # Initialize note octave wrapping logic
        has_wrapped = False
        last_note = Note.Note("C", 1)
        current_note = Note.Note("C", 1)
        first_run = True

        # Check if scale has sharps/flats
        if self.has_sharps:
            # Has sharps
            reordered_note_dict = self.note_dict_offset(self.key, const.NOTE_DICT_SHARPS)
        else:
            # Has flats
            reordered_note_dict = self.note_dict_offset(self.key, const.NOTE_DICT_FLATS)

        # Loop through reordered_note_dict and add notes based on intervals
        while (count < len(reordered_note_dict) and list_index < len(self.intervals)):

            # Save last note
            last_note = current_note

            # Get new current note
            current_note = Note.Note(reordered_note_dict[full_count], self.starting_octave)

            # If notes are wrapping from B back to C, increase octave
            if (not has_wrapped and not first_run and
                last_note.note_name[0] == "B" and current_note.note_name[0] == "C"):
                has_wrapped = True

            # First run logic
            if first_run:
                last_note = current_note
                first_run = False

            # If scale has wrapped, increase octave of note
            if has_wrapped:
                current_note.increase_octave()

            # If the current loop is part of the set of intervals, add new note
            if (count == full_count):
                # Add note
                working_note_dict.append(current_note)
                # Increase interval counter
                count += self.intervals[list_index]
                # Increase list_index counter
                list_index += 1

            # Increase full loop count
            full_count += 1

        # Add first note at end (up an octave)
        current_note = Note.Note(reordered_note_dict[0], self.starting_octave + 1)
        working_note_dict.append(current_note)

        return working_note_dict

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
