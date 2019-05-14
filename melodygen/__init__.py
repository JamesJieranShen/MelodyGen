# Init.py
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import constants
import ml
from note import Note
from scale import Scale
from phrase import Phrase
from generate import Generate
from signature import Signature
from midi_handler import MIDIHandler
