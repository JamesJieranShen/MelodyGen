#!/usr/bin/env python3
from context import melodygen as gen
from melodygen import Note, Scale, Phrase, MIDIHandler as handler, Generate, constants as const
import mido
import time
import random

phrase = gen.Phrase(length = 1, debug=True, endless=True)
phrase.append(0, gen.Note(note = 60, length = 1/4, length_mod=1))
phrase.append(0, gen.Note(note = 64, length = 1/4, length_mod=1))
phrase.append(0, gen.Note(note = 67, length = 1/4, length_mod=1))
phrase.append(1/8, gen.Note(note = 71, length = 1/8, length_mod=1))
phrase.append(1/4, gen.Note(note = 76, length = 1/4, length_mod=1))
phrase.play()

