#!/usr/bin/env python3
"""
.. module:: Phrase
   :platform: Mac, Unix, Windows
   :synopsis: Phrase object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import time
import mido
from note import Note
#from scale import Scale
from generate import Generate
from midi_handler import MIDIHandler as handler
#from signature import Signature

# Phrase object. Is an array of Notes.
class Phrase():
    def __init__(self, tempo=120, debug=False, endless=False):
        """Default constructor for Phrase. 
        
        :param tempo: Tempo of phrase 
        :param debug: Whether or not to display debug info when playing
        :param endless: Whether or not phrase will exit program after finishing
        
        :type tempo: int 
        :type debug: boolean 
        :type endless: boolean

        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        self.phrase = []
        self.tempo = tempo
        self.debug = debug
        self.handler = handler(tempo, debug)
        self.signature = None
        self.endless = endless

    def attach_signature(self, signature):
        if self.signature is not None:
            detach_signature()
        self.signature = signature
        on_attach_signature()
    
    def detach_signature(self):
        self.signature = None
        on_detattch_signature()
    
    def on_attach_signature(self):
        pass

    def on_detach_signature(self):
        pass

    # Utility method to play phrase
    def play(self):
        """Utility method to play Phrase. 
        
        :return: Plays Phrase via MIDIHandler
        :rtype: None 
        """
        end_note = None
        for note in self.phrase:
            self.handler.play_note(note)
            end_note = note
        if not self.endless:
            self.handler.exit_program(end_note)

    # Build phrase
    def generate_phrase(self, algorithm, params):
        """Class method to generate Phrase - delegates to Generate. 
       
        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        self.set_phrase(Generate(algorithm, params))
    
    # Set phrase
    def set_phrase(self, phrase):
        """Utility method to set Phrase. 
        
        :param phrase: Phrase to set 
        
        :type phrase: Phrase 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.phrase = phrase

    # Copy ctor for Phrase
    @staticmethod
    def copy_ctor(old_phrase):
        """Static copy constructor for Phrase. 
        
        :param old_phrase: Phrase object to copy 
        
        :type old_phrase: Phrase 

        :return: Returns a Phrase object, copy of old_phrase
        :rtype: Phrase
        """
        # Create new phrase
        new_phrase = Phrase()
        
        # Copy tempo, debug, handler info
        new_phrase.tempo = old_phrase.tempo
        new_phrase.debug = old_phrase.debug
        new_phrase.handler = old_phrase.handler

        # Copy actual phrase info
        for note in old_phrase.phrase:
            new_phrase.append(note)
        
        return new_phrase 

    # Append to Phrase
    def append(self, input_note):
        """Utility method to append a Note to a Phrase
        
        :param input_slot: Note to append 
        
        :type input_slot: Note 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        input_note = Note.copy_note(input_note)
        self.phrase.append(input_note)
    
    # Utility methods for phrase manipulation
    
    # Utility method to reverse Phrase.  
    def reverse(self):
        """Utility method to reverse Phrase. 
        
        :return: None, modifys object in place 
        :rtype: None 
        """
        self.phrase.reverse()

    def flip(self):
        """Reverse all intervals in the Phrase.

        :return: None, modifies object in place
        :rtype: None
        """
        first_note = self.phrase[0].get_note()
        for note in self.phrase:
            original_value = note.get_note()
            interval = original_value - first_note
            new_value = first_note - interval
            note.set_note(new_value)

    def unify_prob(self, prob=1.0):
        """Set prob of all notes in phrase to be the same.

        :param prob:    new probablity to be set

        :type prob:     float

        :return:        No return, modifies existing object
        :rtype:         None
        """
        for note in self.phrase:
            note.set_prob(prob)

    # Str representation of Phrase
    def __str__(self):
        """Utility function to print Phrase.
       
        :return: String representation of Phrase
        :rtype: String 
        """
        print("<Note: phrase_length: {}, tempo: {}, debug: {}>".format(
                len(self.phrase), self.tempo, self.debug))
        if self.debug:
            for note in self.phrase:
                print('\t', note)
        return ""
