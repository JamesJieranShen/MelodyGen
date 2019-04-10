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

    def __init__(self, note_name=None, octave=None, vel=100):
        """Default constructor for Note. Assigns random pitch in 3rd octave.
        
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
            self.octave = const.OCTAVES[5]
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
        """Static method to get midi value based on note name and octave.
        
        :param note_name: Name of note
        :param octave: Octave of note
        
        :type note_name: String
        :type octave: int

        :return: Returns MIDI value of note
        :rtype: int 
        """
        # Default note dictionary to flats
        note_dict = const.NOTE_DICT_FLATS

        # Parse for sharps or flats to change dictionary
        if len(note_name) > 1:
            if note_name[1] == "s":
                # Change note dictionary to sharps if note is sharp
                note_dict = const.NOTE_DICT_SHARPS

        # Get index of note
        note_index = note_dict.index(note_name)

        # Return (12 * octave_index) + note_index
        # Ex: C3 = (12 * 5) + 0 = 60
        # Ex: G4 = (12 * 6) + 7 = 79
        return (len(note_dict) * const.OCTAVES.index(octave)) + note_index

    # Class method to return random note name.
    def random_note(self, threshold=0.5):
        """Method to get random chromatic note. 
        
        :param threshold: Threshold for sharps (0) vs flats (1)
        
        :type threshold: float

        :return: Returns Note object 
        :rtype: Note 
        """
        # Randomly determine sharps or flats (default is 50/50)
        note_dict = const.NOTE_DICT_SHARPS if (random.random() > threshold) else const.NOTE_DICT_FLATS

        # Return random note
        return random.choice(note_dict)

    # Utility function to increase octave of a note
    def increase_octave(self):
        """Member method to increase octave of note. 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Get current octave index
        current_index = const.OCTAVES.index(self.octave)
        # If not the last element in OCTAVES
        if current_index < len(const.OCTAVES) - 1:
            # Increment index and increase octave
            current_index += 1
            self.octave = const.OCTAVES[current_index]

            # Update midi value
            self.midi_value = self.note_to_midi(self.note_name, self.octave)

    # Utility function to decrease octave of a note
    def decrease_octave(self):
        """Member method to decrease octave of note. 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Get current octave index
        current_index = const.OCTAVES.index(self.octave)

        # If not the first element in OCTAVES
        if current_index > 0:
            # Decrement index and decrease octave
            current_index -= 1
            self.octave = const.OCTAVES[current_index]

            # Update midi value
            self.midi_value = note_to_midi(self.note_name, self.octave)

    # Utility function to get note_name
    def get_note_name(self):
        """Utility function to get note_name.
       
        :return: Returns Note name
        :rtype: String 
        """
        return self.note_name

    # String representation of Note.
    def __str__(self):
        """Utility function to print Note.
       
        :return: String representation of Note
        :rtype: String 
        """
        return "<Note: name_name: %s, octave: %d, midi_value: %d, vel: %d>" % (self.note_name, self.octave, self.midi_value, self.vel)
