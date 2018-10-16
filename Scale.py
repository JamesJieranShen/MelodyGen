#!/usr/bin/env python3

import Note as note

# Scale object. Is an array of Notes
class Scale():

    # Constant note/octave dictionaries
    #KEY_DICT = ["C", "D", "E", "F", "G", "A", "B"]
    NOTE_DICT_NUMKEY = [ 0,   1,    2,   3,    4,   5,   6,    7,   8,    9,   10,   11]
    NOTE_DICT_SHARPS = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]
    NOTE_DICT_FLATS  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    OCTAVES = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Order of sharps/flats
    ORDER_OF_SHARPS = ["F", "C", "G", "D", "A", "E", "B"]
    ORDER_OF_FLATS  = ["B", "E", "A", "D", "G", "C", "F"]

    SCALE_DICT = {'MAJOR':        [2, 2, 1, 2, 2, 2, 1],
                  'IONIAN':       [2, 2, 1, 2, 2, 2, 1],
                  'DORIAN':       [2, 1, 2, 2, 2, 1, 2],
                  'PHRYGIAN':     [1, 2, 2, 2, 1 ,2, 2],
                  'LYDIAN':       [2, 2, 2, 1, 2, 2, 1],
                  'MIXOLYDIAN':   [2, 2, 1, 2, 2, 1, 2],
                  'MINOR':        [2, 1, 2, 2, 1, 2, 2],
                  'AEOLIAN':      [2, 1, 2, 2, 1, 2, 2],
                  'LOCRIAN':      [1, 2, 2, 1, 2, 2, 2],
                  'CHROMATIC':    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  'HARM_MINOR':   [2, 1, 2, 2, 1, 3, 1],
                  'MAJOR_PENT':   [2, 2, 3, 2, 3],
                  'MINOR_PENT':   [3, 2, 2, 3, 2],
                  'BLUES':        [3, 2, 1, 1, 3, 2]}

    MAJOR_MODE_DICT = ['MAJOR', 'IONIAN', 'LYDIAN', 'MIXOLYDIAN', 'CHROMATIC', 'MAJOR_PENT']
    MINOR_MODE_DICT = ['MINOR', 'DORIAN', 'PHRYGIAN', 'AEOLIAN', 'LOCRIAN', 'MINOR_PENT', 'BLUES']

    MAJOR_SHARP_FLAT_DICT = {'C': 'n', 'Cs': 's', 'Db': 'b', 'D': 's', 'Ds': 's', 'Eb': 'b',
                            'E': 's', 'F': 'b', 'Fs': 's', 'Gb': 'b', 'G': 's', 'Gs': 's',
                            'Ab': 'b', 'A': 's', 'As': 's', 'Bb': 'b', 'B': 's'}

    MINOR_SHARP_FLAT_DICT = {'C': 'b', 'Cs': 's', 'Db': 'b', 'D': 'b', 'Ds': 's', 'Eb': 'b',
                            'E': 's', 'F': 'b', 'Fs': 's', 'Gb': 'b', 'G': 'b', 'Gs': 's',
                            'Ab': 'b', 'A': 'n', 'As': 's', 'Bb': 'b', 'B': 's'}

    # Default constructor for Scale. Takes in mode and key
    def __init__(self, key, mode, starting_octave=OCTAVES[5]):
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
        return Scale.SCALE_DICT[mode.upper()]

    # Class method to determine if mode is major or minor
    def get_major_minor(self, mode):
        if mode in self.MAJOR_MODE_DICT:
            # 1: Major, 2: Minor
            return True, False
        else:
            # 1: Major, 2: Minor
            return False, True

    # Class method to determine if scale has sharps or flats
    def get_sharps_flats(self, key):
        # Assign sharp_flat_dict based on if major or minor
        if self.is_major:
            # Major sharp/flat dict
            sharp_flat_dict = self.MAJOR_SHARP_FLAT_DICT
        else:
            # Minor sharp/flat dict
            sharp_flat_dict = self.MINOR_SHARP_FLAT_DICT

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
        # Get index of key
        key_index = note_dict.index(key)

        # Splice and rearrange list at key_index
        return note_dict[key_index:] + note_dict[:key_index]

    # Class method to build scale
    def build_scale(self):

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
        last_note = note.Note("C", 1)
        current_note = note.Note("C", 1)
        first_run = True

        # Check if scale has sharps/flats
        if self.has_sharps:
            # Has sharps
            reordered_note_dict = self.note_dict_offset(self.key, self.NOTE_DICT_SHARPS)
        else:
            # Has flats
            reordered_note_dict = self.note_dict_offset(self.key, self.NOTE_DICT_FLATS)

        # Loop through reordered_note_dict and add notes based on intervals
        while (count < len(reordered_note_dict) and list_index < len(self.intervals)):

            # Save last note
            last_note = current_note

            # Get new current note
            current_note = note.Note(reordered_note_dict[full_count], self.starting_octave)

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
        current_note = note.Note(reordered_note_dict[0], self.starting_octave + 1)
        working_note_dict.append(current_note)

        return working_note_dict

    # String representation of Scale.
    def __str__(self):
        print("<Scale: key: %s, mode: %s>" % (self.key, self.mode))

        for note in self.notes:
            print("\t", note)

        return ""

    def __len__(self):
        return len(self.notes)
