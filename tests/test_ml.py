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

# gen.ml.build_corpus("./midi_songs", "./parsed_songs", "./")

X, y = gen.ml.preprocess_data("./corpus.song")
gen.ml.build_train_model(X, y, epochs=5)
