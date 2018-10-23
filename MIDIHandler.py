#!/usr/bin/env python3
"""
.. module:: MIDIHandler
   :platform: Mac, Unix, Windows
   :synopsis: MIDIHandler object for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import time
import mido

# Object to handle playing MIDI data
class MIDIHandler():
    # Constants
    DEBUG_ON = False
    PRINT_NOTES = True
    MIDI_CHANNEL_1 = 0x0
    
    def __init__(self, tempo=120, debug=DEBUG_ON):
        """Default constructor for MIDIHandler. 
        
        :param tempo: Tempo of MIDIHandler
        :param debug: Whether or not to display debug info when playing 
        
        :type tempo: int 
        :type debug: boolean 

        :return: Returns a MIDIHandler object
        :rtype: MIDIHandler
        """
        self.tempo = tempo

        # Get inputs/outputs
        self.outputs = mido.get_output_names()
        self.inputs = mido.get_input_names()

        # Define input/output to be used
        self.keyboard_input = mido.open_input(self.inputs[4])
        self.midi_output = mido.open_output(self.outputs[0])
         
        # Print IO info
        self.print_io(debug)

    # Utility method to play slot
    def play_slot(self, slot):
        """Utility method to play slot. 
        
        :param slot: Slot to play
        
        :type slot: Slot 

        :return: No return, plays Slot 
        :rtype: None 
        """
        trig = False
        if (random.random() <= slot.prob):
            trig = True

        if trig: self.note_on(slot)
        time.sleep((240 * slot.length * slot.length_mod) / self.tempo)
        if trig: self.note_off(slot)


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
    def note_on(self, slot, chan=MIDI_CHANNEL_1):
        """Utility method to turn MIDI note on. 
        
        :param slot: Slot to play MIDI from 
        :param chan: MIDI channel to play on 
        
        :type slot: Slot 
        :type chan: Hexidecimal 

        :return: No return, starts playing MIDI note 
        :rtype: None 
        """
        msg = [0] * 3
        msg = [0x90 + chan, slot.note.midi_value, slot.note.vel]

        # Debug print
        if self.DEBUG_ON or self.PRINT_NOTES:
            print(slot.note.note_name, msg)

        self.midi_output.send(self.MSG(msg))

    # Utility method to send a note off signal
    def note_off(self, slot, chan=MIDI_CHANNEL_1):
        """Utility method to turn MIDI note off. 
        
        :param slot: Slot to play MIDI from 
        :param chan: MIDI channel to play on 
        
        :type slot: Slot 
        :type chan: Hexidecimal 

        :return: No return, stops playing MIDI note 
        :rtype: None 
        """
        msg = [0] * 3
        msg = [0x80 + chan, slot.note.midi_value, 127]
        self.midi_output.send(self.MSG(msg))
