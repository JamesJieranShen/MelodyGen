#!/usr/bin/env python3

import random
import time
import mido
#import Note as note
#import Scale as scale
#import Slot

# Object to handle playing MIDI data
class MIDIHandler():
    # Utility method to play slot
    def play_slot(self, slot):
        '''
        if not isinstance(slot, Slot.Slot):
            print("NOT A SLOT")
        else:
            print(slot.length, slot.length_mod, self.tempo)
        '''
        trig = False
        if (random.random() <= slot.prob):
            trig = True

        if trig: self.note_on(slot)
        time.sleep((240 * slot.length * slot.length_mod) / self.tempo)
        if trig: self.note_off(slot)

    # Constants
    DEBUG_ON = False
    PRINT_NOTES = True
    MIDI_CHANNEL_1 = 0x0

    def __init__(self, tempo=120, debug=DEBUG_ON):
        self.tempo = tempo

        # Get inputs/outputs
        self.outputs = mido.get_output_names()
        self.inputs = mido.get_input_names()

        # Define input/output to be used
        self.keyboard_input = mido.open_input(self.inputs[4])
        self.midi_output = mido.open_output(self.outputs[0])
         
        # Print IO info
        self.print_io(debug)


    def print_io(self, debug):
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
        self.tempo = tempo

    # Utility method to get tempo of handler
    def get_tempo():
        return self.tempo

    # Utility method to turn bytes into MIDI
    def MSG(self, msg):
       return mido.Message.from_bytes(msg)


    # Utility method to send a note on signal
    def note_on(self, slot, chan=MIDI_CHANNEL_1):
        msg = [0] * 3
        msg = [0x90 + chan, slot.note.midi_value, slot.note.vel]

        # Debug print
        if self.DEBUG_ON or self.PRINT_NOTES:
            print(slot.note.note_name, msg)

        self.midi_output.send(self.MSG(msg))

    # Utility method to send a note off signal
    def note_off(self, slot, chan=MIDI_CHANNEL_1):
        msg = [0] * 3
        msg = [0x80 + chan, slot.note.midi_value, 127]
        self.midi_output.send(self.MSG(msg))
