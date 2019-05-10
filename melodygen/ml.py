#!/usr/bin/env python3
"""
.. module:: ml
   :platform: Mac, Unix, Windows
   :synopsis: Machine learning module for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import glob
import sys
import numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

from phrase import Phrase

# Code adapted from https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/
def preprocess_data(corpus_path):
    # load ascii text and covert to lowercase
    filename = corpus_path
    raw_text = open(filename).read()
    raw_text = raw_text.lower()
    # create mapping of unique chars to integers
    chars = sorted(list(set(raw_text)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    # summarize the loaded data
    n_chars = len(raw_text)
    n_vocab = len(chars)
    print("Total Characters: ", n_chars)
    print("Total Vocab: ", n_vocab)

    # prepare the dataset of input to output pairs encoded as integers
    seq_length = 100
    dataX = []
    dataY = []
    for i in range(0, n_chars - seq_length, 1):
        seq_in = raw_text[i : i + seq_length]
        seq_out = raw_text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])
    n_patterns = len(dataX)
    print("Total Patterns: ", n_patterns)
    # reshape X to be [samples, time steps, features]
    X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
    # normalize
    X = X / float(n_vocab)
    # one hot encode the output variable
    y = np_utils.to_categorical(dataY)

    return (X, y)


def build_train_model(X, y, epochs=1, batch_size=128, weights_path="./weights"):
    # define the LSTM model
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    # define the checkpoint
    filepath = weights_path + "/weights-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(
        filepath, monitor="loss", verbose=1, save_best_only=True, mode="min"
    )
    callbacks_list = [checkpoint]

    model.fit(X, y, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)


def build_corpus(midi_path, parsed_path, corpus_path, corpus_name="corpus.song"):
    """Utility method to build corpus for input into ML model.
    
    :param midi_path: Path of midi files to parse 
    :param parsed_path: Path to store parsed (.song) files
    :param corpus_path: Path to output final corpus file (corpus.song)

    :type note_name: int
    :type vel: int
    :type length: float 

    :return: No return, creates parsed .song files and outputs corpus.song
    :rtype: None 
    """
    for f in glob.glob(midi_path + "/*.mid"):
        # Initalize phrase and filename
        phrase = Phrase(tempo=120, debug=False, endless=False, length=500)
        file_name = str(f.split("/")[-1].split(".mid")[0])

        try:
            # Load file from midi
            phrase.parse_midi(f)
        except:
            # Continue to next file on error
            print(file_name + " not parsed")
            continue

        # Save phrase to file
        parsed_file_name = parsed_path + "/" + file_name + ".song"
        phrase.to_file(parsed_file_name)

    # Delete phrase object
    del phrase

    # Create output corpus file
    with open(corpus_path + corpus_name, "wb") as outfile:
        for f in glob.glob(parsed_path + "/*.song"):
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    print("Corpus built at", corpus_path)
    return
