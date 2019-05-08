import glob
import pickle
import numpy
from fractions import Fraction
from music21 import converter, instrument, note, chord

# Code adapted from https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5
def parse_midi(file_path):
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
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
                        Fraction(element.quarterLength),
                        element.offset,
                    )
                )
                # notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                for n in element:
                    notes.append(
                        (
                            n.pitch.midi,
                            n.volume.velocity,
                            Fraction(n.quarterLength),
                            element.offset,
                        )
                    )

    # with open('data/notes', 'wb') as filepath:
    #     pickle.dump(notes, filepath)

    for n in notes:
        print(n)


parse_midi("midi_songs/cosmo.mid")
