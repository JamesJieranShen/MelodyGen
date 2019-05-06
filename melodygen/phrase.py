#!/usr/bin/env python3
"""
.. module:: phrase
   :platform: Mac, Unix, Windows
   :synopsis: Phrase object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import time
import mido
from note import Note
from generate import Generate
from midi_handler import MIDIHandler as handler
import threading

# Phrase object. Is a dictionary of Notes.
class Phrase:
    def __init__(self, tempo=120, debug=False, endless=False, length=4):
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
        self.phrase = {}
        self.tempo = tempo
        self.debug = debug
        self.signature = None
        self.length = length
        self.handler = handler(tempo, debug)
        self.killed = False
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

    # Threading function for triggering multiple notes at the same time
    def play_thread(self, note, offset):
        time.sleep(240 * offset / self.tempo)  # Wait until it's time to play
        if not self.killed:
            self.handler.play_note(note)

    def clock(self, length):
        time.sleep(240 * length / self.tempo)

    # Utility method to play phrase
    def play(self):
        """Utility method to play Phrase. 
        
        :return: Plays Phrase via MIDIHandler
        :rtype: None 
        """
        # work clock:
        clock = threading.Thread(target=self.clock, args=(self.length,))
        thread_list = []
        for note, start in self.phrase.items():
            this_thread = threading.Thread(target=self.play_thread, args=(note, start))
            this_thread.daemon = True
            thread_list.append(this_thread)

        # start all threads
        clock.start()
        for thread in thread_list:
            thread.start()

        # handle endless
        if self.endless and not self.killed:
            try:
                clock.join()
                self.play()
            except KeyboardInterrupt:
                self.killed = True
                self.handler.exit_program(self.phrase)
        else:
            for thread in thread_list:
                thread.join()
            clock.join()
            self.handler.exit_program(self.phrase)

    # Build phrase
    def generate_phrase(self, algorithm, params):
        """Class method to generate Phrase - delegates to Generate. 
       
        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        self.set_phrase(Generate(algorithm, params).phrase)

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
        for old_note, start in old_phrase.phrase.items():
            new_note = copy_note(old_note)
            new_phrase.phrase[new_note] = start
        return new_phrase

    # Append to Phrase
    def append(self, start, input_note):
        """Utility method to append a Note to a Phrase
        
        :param input_slot:  Note to append 
        :param start:       start time stamp for the note
        
        :type input_slot:   Note 
        :type start:        Fraction

        :return: No return, modifys existing object 
        :rtype: None 
        """
        input_note = Note.copy_note(input_note)
        # allows out-of-phrase notes, but show warning.
        if start >= self.length:
            print(
                "Warning: "
                + input_note.__str__
                + "outside of phrase, will not be played."
            )

        self.phrase[input_note] = start

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
        for note in self.set_phrase:
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
        print(
            "<Note: phrase_length: {}, tempo: {}, debug: {}>".format(
                self.length, self.tempo, self.debug
            )
        )
        if self.debug:
            for note in self.phrase:
                print("\t", note)
        return ""
