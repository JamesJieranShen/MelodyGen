#!/usr/bin/env python3
from context import melodygen as gen
from melodygen import (
    Note,
    Scale,
    Phrase,
    MIDIHandler as handler,
    Generate,
    constants as const,
    ml,
)
import mido
import time
import random
import os

gen.ml.build_corpus("./test_midi_songs", "./parsed_songs", "./")
