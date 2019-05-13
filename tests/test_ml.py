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

X, y, dataX, dataY = gen.ml.preprocess_data("./corpus.song")
# model = gen.ml.build_train_model(X, y, epochs=5)

# gen.ml.generate("./weights/weights-01-0.7092.hdf5", "./corpus.song", X, y, dataX, dataY)
gen.ml.generate(
    "./weights/weights-2_layer-01-0.5931.hdf5", "./corpus.song", X, y, dataX, dataY
)

