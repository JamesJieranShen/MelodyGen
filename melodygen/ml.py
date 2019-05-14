#!/usr/bin/env python3
"""
.. module:: ml
   :platform: Mac, Unix, Windows
   :synopsis: Machine learning module for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import os.path

import glob
import sys
import numpy

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import CuDNNLSTM
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.utils import np_utils
from keras import backend as K

import tensorflow as tf
from tensorflow.python.client import device_lib

from phrase import Phrase

# Code adapted from https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/
def preprocess_data(corpus_path, seq_length=100):
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
    seq_length = seq_length
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

    return (X, y, dataX, dataY)


def build_train_model(
    X,
    y,
    epochs=20,
    batch_size=128,
    layer_size=256,
    lstm_layers=2,
    dense_layers=1,
    weights_path="./data/weights",
):
    # GPU settings
    print(device_lib.list_local_devices())
    K.tensorflow_backend._get_available_gpus()

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    # device_name = tf.test.gpu_device_name()
    # if device_name != "/device:GPU:0":
    #     raise SystemError("GPU not found")
    # print("Found GPU at {}".format(device_name))

    with tf.device("/cpu:0"):
        # define model
        model = Sequential()

        # Add LSTM layers
        model.add(
            LSTM(
                layer_size,
                input_shape=(X.shape[1:]),
                activation="relu",
                return_sequences=True,
            )
        )
        model.add(Dropout(0.2))

        for l in range(lstm_layers - 1):
            model.add(LSTM(layer_size))
            model.add(Dropout(0.2))

        # Add dense layers
        for l in range(dense_layers - 1):
            model.add(Dense(layer_size))
            model.add(Activation("relu"))

        model.add(Dense(y.shape[1], activation="softmax"))

        # Compile model
        model.compile(loss="categorical_crossentropy", optimizer="adam")

        # define the checkpoint
        filepath = (
            weights_path
            + "/weights-layer_size-{}-lstm_layers-{}-dense_layers-{}-epoch-{}-loss-{}.hdf5".format(layer_size, lstm_layers, dense_layers, epoch:02d, loss:.4f)
        )
        checkpoint = ModelCheckpoint(
            filepath, monitor="loss", verbose=1, save_best_only=True, mode="min"
        )

        # Set up tensorboard
        tensorboard = TensorBoard(
            log_dir=weights_path
            + "/logs/{}".format(
                "weights-layer_size-{}-lstm_layers-{}-dense_layers-{}".format(
                    layer_size, lstm_layers, dense_layers
                )
            )
        )

        callbacks_list = [checkpoint, tensorboard]

        model.fit(X, y, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)


def generate(weights_path, corpus_path, X, y, dataX, dataY):
    # load ascii text and covert to lowercase
    corpus_filename = corpus_path
    raw_text = open(corpus_filename).read()
    raw_text = raw_text.lower()
    # create mapping of unique chars to integers, and a reverse mapping
    chars = sorted(list(set(raw_text)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_char = dict((i, c) for i, c in enumerate(chars))
    # summarize the loaded data
    n_chars = len(raw_text)
    n_vocab = len(chars)

    # define model
    model = Sequential()

    model.add(
        LSTM(256, input_shape=(X.shape[1:]), activation="relu", return_sequences=True)
    )
    model.add(Dropout(0.2))

    model.add(LSTM(256), activation="relu")
    model.add(Dropout(0.2))

    model.add(Dense(y.shape[1], activation="softmax"))

    # load the network weights
    filename = weights_path
    model.load_weights(filename)
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    # pick a random seed
    start = numpy.random.randint(0, len(dataX) - 1)
    pattern = dataX[start]
    print("Seed:")
    print('"', "".join([int_to_char[value] for value in pattern]), '"')
    # generate characters
    for i in range(500):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_char[index]
        seq_in = [int_to_char[value] for value in pattern]
        sys.stdout.write(result)
        pattern.append(index)
        pattern = pattern[1 : len(pattern)]
    print("\nDone.")


def build_corpus(midi_path, parsed_path, corpus_path, corpus_name="corpus.song", pct=1):
    """Utility method to build corpus for input into ML model.
    
    :param midi_path: Path of midi files to parse 
    :param parsed_path: Path to store parsed (.song) files
    :param corpus_path: Path to output final corpus file (corpus.song)
    :param pct: Percent of files in directory to parse

    :type note_name: int
    :type vel: int
    :type length: float 
    :type pct: float

    :return: No return, creates parsed .song files and outputs corpus.song
    :rtype: None 
    """
    # Only parse percent of files
    num_files = int(
        pct * sum(os.path.isfile(f) for f in glob.glob(midi_path + "/*.mid"))
    )
    print("Parsing {} files".format(num_files))

    # Delete all .song files in parsed_songs
    for f in glob.glob(parsed_path + "/*.song"):
        os.remove(f)

    # Counter for parsing percentage of files
    counter = 0
    for f in glob.glob(midi_path + "/*.mid"):
        # Break out of loop if num_files met
        if counter >= num_files:
            break

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

        # Increment counter
        counter += 1

    # Delete phrase object
    del phrase

    # Create output corpus file
    with open(corpus_path + "/" + corpus_name, "wb") as outfile:
        for f in glob.glob(parsed_path + "/*.song"):
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    print("Corpus built at", corpus_path)
    return