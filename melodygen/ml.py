#!/usr/bin/env python3
"""
.. module:: ml
   :platform: Mac, Unix, Windows
   :synopsis: Machine learning module for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import glob
import sys
from phrase import Phrase


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

        # Load file from midi
        phrase.parse_midi(f)

        # Save phrase to file
        parsed_file_name = parsed_path + "/" + file_name + ".song"
        phrase.to_file(parsed_file_name)

    # Create output corpus file
    with open(corpus_path + corpus_name, "wb") as outfile:
        for f in glob.glob(parsed_path + "/*.song"):
            with open(f, "rb") as infile:
                outfile.write(infile.read())
    print("Corpus built at", corpus_path)
    return
