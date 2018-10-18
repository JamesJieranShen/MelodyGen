#!/usr/bin/env python3

import random

# Base note object. Has Name of pitch and MIDI value.
class Note():

    # Constant note/octave dictionaries
    NOTE_DICT_NUMKEY = [ 0,   1,    2,   3,    4,   5,   6,    7,   8,    9,   10,   11]
    NOTE_DICT_SHARPS = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]
    NOTE_DICT_FLATS  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    OCTAVES = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]

    # 
    def __init__(self, note_name=None, octave=None, vel=100):
        """Default constructor for Note. Assigns random pitch in 3rd octave
        
        :param note_name: Name of note
        :param octave: Octave of note
        :param vel: Velocity of note
        
        :type note_name: String
        :type octave: int
        :type vel: int

        :return: Returns a Note object
        :rtype: Note 
        """
        # Check for note_name
        if note_name is None:
            # Assign random note
            self.note_name = self.random_note()
        else:
            # Assign inputted note
            self.note_name = note_name

        # Check for octave
        if octave is None:
            # Assign octave 3
            self.octave = self.OCTAVES[5]
        else:
            # Assign inputted octave
            self.octave = octave

        # Calculate midi value based on note name
        self.midi_value = self.note_to_midi(self.note_name, self.octave)

        # Set note velocity
        self.vel = vel

    # Static method to return the MIDI value of a note based on its name/octave.
    @staticmethod
    def note_to_midi(note_name, octave):
        # Default note dictionary to flats
        note_dict = Note.NOTE_DICT_FLATS

        # Parse for sharps or flats to change dictionary
        if len(note_name) > 1:
            if note_name[1] == "s":
                # Change note dictionary to sharps if note is sharp
                note_dict = Note.NOTE_DICT_SHARPS

        # Get index of note
        note_index = note_dict.index(note_name)

        # Return (12 * octave_index) + note_index
        # Ex: C3 = (12 * 5) + 0 = 60
        # Ex: G4 = (12 * 6) + 7 = 79
        return (len(note_dict) * Note.OCTAVES.index(octave)) + note_index

    # Class method to return random note name.
    def random_note(self, threshold=0.5):
        # Randomly determine sharps or flats (default is 50/50)
        note_dict = self.NOTE_DICT_SHARPS if (random.random() > threshold) else self.NOTE_DICT_FLATS

        # Return random note
        return random.choice(note_dict)

    # Utility function to increase octave of a note
    def increase_octave(self):
        # Get current octave index
        current_index = self.OCTAVES.index(self.octave)
        # If not the last element in OCTAVES
        if current_index < len(self.OCTAVES) - 1:
            # Increment index and increase octave
            current_index += 1
            self.octave = self.OCTAVES[current_index]

            # Update midi value
            self.midi_value = self.note_to_midi(self.note_name, self.octave)

    # Utility function to decrease octave of a note
    def decrease_octave(self):
        # Get current octave index
        current_index = OCTAVES.index(self.octave)

        # If not the first element in OCTAVES
        if current_index > 0:
            # Decrement index and decrease octave
            current_index -= 1
            self.octave = OCTAVES[current_index]

            # Update midi value
            self.midi_value = note_to_midi(self.note_name, self.octave)

    # Utility function to get note_name
    def get_note_name(self):
        return self.note_name

    # String representation of Note.
    def __str__(self):
        return "<Note: name_name: %s, octave: %d, midi_value: %d, vel: %d>" % (self.note_name, self.octave, self.midi_value, self.vel)
