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
import Note
import Scale
import MIDIHandler as handler

# Phrase object. Is an array of Notes.
class Phrase():
    def __init__(self, tempo=120, debug=False):
        """Default constructor for Phrase. 
        
        :param tempo: Tempo of phrase 
        :param debug: Whether or not to display debug info when playing 
        
        :type tempo: int 
        :type debug: boolean 

        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        self.phrase = []
        self.tempo = tempo
        self.debug = debug
        self.handler = handler.MIDIHandler(tempo, debug)
    
    # Utility method to play phrase
    def play(self):
        """Utility method to play Phrase. 
        
        :return: Plays Phrase via MIDIHandler
        :rtype: None 
        """
        for note in self.phrase:
            self.handler.play_note(note)
        print('\n')
    

    # Build phrase
    def generate_phrase(self):
        """WORK IN PROGRESS - Class method to generate Phrase. 
       
        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        ## Manual phrase building
        #phrase1 = []
        #phrase2 = []
        #print("run")
        #test_note = note.Note("C")
        #scale = scale.Scale("A", 'HARM_MINOR', 3)
        #handler = handler.MIDIHandler(100)

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
        input_note = Note.Note.copy_note(input_note)
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
        return ("<Note: phrase_length: {}, tempo: {}, debug: {}>".format(
                len(self.phrase), self.tempo, self.debug))
