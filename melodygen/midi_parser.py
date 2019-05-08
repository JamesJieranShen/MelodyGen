import glob
import pickle
import numpy
from music21 import converter, instrument, note, chord


def get_notes():
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    notes = []
    for file in glob.glob("midi_songs/cosmo.mid"):
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
                notes.append(element)
                # notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                pass
                # notes.append(".".join(str(n) for n in element.normalOrder))

    # with open('data/notes', 'wb') as filepath:
    #     pickle.dump(notes, filepath)

    for asdf in notes[:5]:
        print("pitch", asdf.pitch.midi)
        print("offset", asdf.offset)
        print("length", asdf.quarterLength)


get_notes()
