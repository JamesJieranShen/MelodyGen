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
#from note import Note

# Object to handle playing MIDI data
class MIDIHandler():
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
        self.midi_output = mido.open_output(self.outputs[0])
         
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
        if (random.random() <= note.prob):
            trig = True

        #try:
        if trig: self.note_on(note)
        time.sleep((240 * note.length * note.length_mod) / self.tempo)
        if trig: self.note_off(note)
        #except KeyboardInterrupt:
        #    self.exit_program(note)

    def exit_program(self, note):
        """Utility method to exit program. 
        
        :param note: Note to shut off. 
        
        :type note: Note 

        :return: None. 
        """
        self.panic()
        #self.note_off(note)
        print('\n')
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
    def set_tempo(tempo):
        """Utility method to set tempo of handler. 
        
        :param tempo: Tempo to set handler to 
        
        :type tempo: int 

        :return: No return, modifys existing object 
        :rtype: None 
        """
        self.tempo = tempo

    # Utility method to get tempo of handler
    def get_tempo():
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
