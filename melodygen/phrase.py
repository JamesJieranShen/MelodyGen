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
        """Utility method to play thread. 
        
        :return: Plays thread via MIDIHandler
        :rtype: None 
        """
        time.sleep(240 * offset / self.tempo)  # Wait until it's time to play
        # Logic for ending with Ctl-C
        if not self.killed:
            self.handler.play_note(note)

    def clock(self, length):
        time.sleep(240 * length / self.tempo)

    # Utility method to play phrase
    def play(self):
        """Utility method to play Phrase. Utilizes multithreading to play multiple
            notes at once. 
        
        :return: Plays Phrase via MIDIHandler
        :rtype: None 
        """
        # Work clock:
        clock = threading.Thread(target=self.clock, args=(self.length,))
        thread_list = []
        for note, start in self.phrase.items():
            this_thread = threading.Thread(target=self.play_thread, args=(note, start))
            this_thread.daemon = True
            thread_list.append(this_thread)

        # Start all threads
        clock.start()
        for thread in thread_list:
            thread.start()

        # Handle endless
        if self.endless and not self.killed:
            try:
                # Play notes
                clock.join()
                self.play()
            except KeyboardInterrupt:
                # Exit on Ctl-C
                self.killed = True
                self.handler.exit_program(self.phrase)
        else:
            # Exit program on phrase end
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

    # Set length
    def set_length(self, length):
        """Utility method to set Phrase length. 
        
        :param length: Phrase length to set 
        
        :type length: float 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.length = length

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
        # Allows out-of-phrase notes, but shows warning
        if start >= self.length:
            print(
                "Warning: " + str(input_note) + "outside of phrase, will not be played."
            )
        self.phrase[input_note] = start

    # Utility methods for phrase manipulation

    def quantize(self, division=None, sig_div=None, quantize_length=False):
        """Quantize all notes in phrase
        
        :param division: Division to quantize based on
        :param sig_div: Use division of signature.beat
        :param quantize_length: Quantize note length?

        :type division: Fraction / Float
        :type sig_div: Fraction / Float
        :type quantize_length: Boolean

        :return: No return, modifys existing object 
        :rtype: None 
        """
        # Sanity check:
        if division is not None and sig_div is not None:
            print("ERROR:  Only one parameter should be provided")
            return
        if division is None and sig_div is None:
            print("ERROR:  No parameters provided")

        # Init quantization base
        base = 0
        if division is not None:
            base = division
        if sig_div is not None:
            base = self.signature.beat * sig_div

        # Iterate through notes
        for note in self.phrase:
            start = self.phrase[note]
            # round start
            self.phrase[note] = round(start / float(base)) * base
            if quantize_length is True:
                length = note.length
                note.set_length(round(length / float(base)) * base)

    # Utility method to reverse Phrase
    def reverse(self):  # DYSFUNCTIONAL
        """Utility method to reverse Phrase. 
        
        :return: None, modifys object in place 
        :rtype: None 
        """
        self.phrase.reverse()

    # Utility methods to flip intervals of Phrase
    def flip(self):  # DYSFUNCTIONAL
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

    # Utility method to resize phrase length to sum of note lengths
    def resize(self):
        """Utility method to resize phrase length to sum of note lengths.
        
        :return: None, modifys object in place 
        :rtype: None 
        """
        counter = 0
        for note in self.phrase.keys():
            counter += note.length * note.length_mod
        self.set_length(counter)

    def normalize_offset(self):
        """Utility method to normalize offset (set first note's offset to 0
        and subtract that value from the rest).
        
        :return: None, modifys object in place 
        :rtype: None 
        """
        orig_offset = list(self.phrase.values())[0]
        for note, offset in self.phrase.items():
            self.phrase[note] = offset - orig_offset

    def parse_midi(self, file_path):
        """Utility method to parse midi via midi_parser and set phrase.
        
        :param file_path: File path of midi file to parse

        :type file_path: String

        :return: None, modifys object in place 
        :rtype: None 
        """
        notes = handler.parse_midi(file_path)
        for note in notes:
            self.append(
                note[3], Note(note=note[0], vel=note[1], length=note[2], length_mod=1)
            )
        self.resize()
        self.normalize_offset()

    def unify_prob(self, prob=1.0):
        """Set prob of all notes in phrase to be the same.

        :param prob:    new probablity to be set

        :type prob:     float

        :return:        No return, modifies existing object
        :rtype:         None
        """
        for note in self.phrase:
            note.set_prob(prob)

    # Str representation of Phrase.
    def __str__(self):
        """Utility function to print Phrase
       
        :return: String representation of Phrase
        :rtype: String 
        """
        print(
            "<Note: phrase_length: {}, tempo: {}, debug: {}>".format(
                self.length, self.tempo, self.debug
            )
        )
        if self.debug:
            for note, offset in self.phrase.items():
                print("\t", note)
                print("\t   ", "offset", offset)
        return ""
