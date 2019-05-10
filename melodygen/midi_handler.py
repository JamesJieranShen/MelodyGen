#!/usr/bin/env python3
"""
.. module:: midi_handler
   :platform: Mac, Unix, Windows
   :synopsis: MIDIHandler object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import time
import mido
import os
import gc
import glob
import pickle
import numpy
from fractions import Fraction
from music21 import converter, instrument, note, chord

# Object to handle playing MIDI data
class MIDIHandler:
    # Constants
    DEBUG_ON = False
    PRINT_NOTES = False
    MIDI_CHANNEL_1 = 0x0

    def __init__(self, tempo=120, print_notes=PRINT_NOTES, debug=DEBUG_ON):
        """Default constructor for MIDIHandler. 
        
        :param tempo: Tempo of MIDIHandler
        :param debug: Whether or not to display debug info when playing 
        
        :type tempo: int 
        :type debug: boolean 

        :return: Returns a MIDIHandler object
        :rtype: MIDIHandler
        """
        self.tempo = tempo
        self.print_notes = print_notes
        self.debug = debug

        # Get inputs/outputs
        self.outputs = mido.get_output_names()
        self.inputs = mido.get_input_names()

        # Define input/output to be used
        self.keyboard_input = mido.open_input(self.inputs[0])
        self.midi_output = mido.open_output(self.outputs[0], autoreset=True)

        # Print IO info
        self.print_io(debug)

    # Utility method to play note
    def play_note(self, note):
        """Utility method to play note. 
        
        :param slot: Note to play
        
        :type slot: Note 

        :return: No return, plays Note 
        :rtype: None 
        """
        trig = False
        if random.random() <= note.prob:
            trig = True

        if trig:
            self.note_off(note)
            self.note_on(note)
        time.sleep((240 * note.length * note.length_mod * 0.95) / self.tempo)
        if trig:
            self.note_off(note)

    # Code adapted from https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5
    @staticmethod
    def parse_midi(file_path):
        """Utility method to parse midi file. 
        
        :param file_path: Path to midi file to parse
        
        :type file_path: String 

        :return: Tuple of note pitch, velocity, length, offset
        :rtype: Tuple 
        """
        notes = []
        for file in glob.glob(file_path):
            midi = converter.parse(file)

            print("Parsing %s" % file)

            notes_to_parse = None

            try:  # file has instrument parts
                s2 = instrument.partitionByInstrument(midi)
                notes_to_parse = s2.parts[0].recurse()
            except:  # file has notes in a flat structure
                notes_to_parse = midi.flat.notes

            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(
                        (
                            element.pitch.midi,
                            element.volume.velocity,
                            max(
                                float(
                                    Fraction(
                                        element.quarterLength / 4
                                    ).limit_denominator()
                                ),
                                1 / 64,
                            ),
                            element.offset / 4,
                        )
                    )
                    # notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    for n in element:
                        notes.append(
                            (
                                n.pitch.midi,
                                n.volume.velocity,
                                max(
                                    float(
                                        Fraction(
                                            n.quarterLength / 4
                                        ).limit_denominator()
                                    ),
                                    1 / 64,
                                ),
                                element.offset / 4,
                            )
                        )

        return notes

    def exit_program(self, notes):
        """Utility method to exit program. 
       
        :return: None. 
        """
        for note in notes.keys():
            self.note_off(note)
        print("\n")
        gc.collect(generation=2)
        os._exit(0)

    def print_io(self, debug):
        """Utility method to print input/output debug info. 
        
        :param debug: Whether or not to display debug info when playing 
        
        :type debug: boolean 

        :return: Input/output debug info 
        :rtype: String
        """
        # Print input/output debug info
        if debug:
            print("MIDI Inputs")
            for index, item in enumerate(self.inputs):
                print("[%d] %s" % (index, item))

            print("MIDI Outputs")
            for index, item in enumerate(self.outputs):
                print("[%d] %s" % (index, item))

    # Utility method to set tempo of handler
    def set_tempo(self, tempo):
        """Utility method to set tempo of handler. 
        
        :param tempo: Tempo to set handler to 
        
        :type tempo: int 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.tempo = tempo

    # Utility method to get tempo of handler
    def get_tempo(self):
        """Utility method to get tempo of handler. 
        
        :return: Tempo of handler 
        :rtype: int 
        """
        return self.tempo

    # Utility method to turn bytes into MIDI
    def MSG(self, msg):
        """Utility method to turn bytes into MIDI. 
        
        :param msg: Byte string to be converted into MIDI 
        
        :type msg: bytes 

        :return: MIDI message from byte string 
        :rtype: MIDI 
        """
        return mido.Message.from_bytes(msg)

    # Utility method to send a note on signal
    def note_on(self, note, chan=MIDI_CHANNEL_1):
        """Utility method to turn MIDI note on. 
        
        :param slot: Note to play MIDI from 
        :param chan: MIDI channel to play on 
        
        :type slot: Note 
        :type chan: Hexidecimal 

        :return: No return, starts playing MIDI note 
        :rtype: None 
        """
        msg = [0] * 3
        msg = [0x90 + chan, note.note, note.vel]

        # Debug print
        if self.print_notes:
            print(note)

        self.midi_output.send(self.MSG(msg))

    # Utility method to send a note off signal
    def note_off(self, note, chan=MIDI_CHANNEL_1):
        """Utility method to turn MIDI note off. 
        
        :param slot: Note to play MIDI from 
        :param chan: MIDI channel to play on 
        
        :type slot: Note 
        :type chan: Hexidecimal 

        :return: No return, stops playing MIDI note 
        :rtype: None 
        """
        msg = [0] * 3
        msg = [0x80 + chan, note.note, 127]
        self.midi_output.send(self.MSG(msg))
