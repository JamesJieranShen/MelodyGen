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

gen.ml.build_corpus(
    "./data/midi_songs", "./data/parsed_songs", "./data/corpus", "corpus.song"
)

# X, y, dataX, dataY = gen.ml.preprocess_data("./data/corpus/tiny_corpus.song")
"""
dense_layers = [1]
layer_sizes = [256]
lstm_layers = [2]

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for lstm_layer in lstm_layers:
            gen.ml.build_train_model(
                X,
                y,
                epochs=1,
                layer_size=layer_size,
                lstm_layers=lstm_layer,
                dense_layers=dense_layer,
            )

# gen.ml.generate("./weights/weights-01-0.7092.hdf5", "./corpus.song", X, y, dataX, dataY)
# gen.ml.generate(
#     "./weights/weights-2_layer-01-0.5931.hdf5", "./corpus.song", X, y, dataX, dataY
# )
"""
