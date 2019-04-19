#!/usr/bin/env python3
"""
.. module:: Generate
   :platform: Mac, Unix, Windows
   :synopsis: Generate module for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import time
import Note
import Scale
import Phrase

# Generate object - takes in type of algorithm and array of params 
class Generate():
    
    def __new__(cls, algorithm, params):
        """Constructor for Generate object
        
        :param algorithm: Algorithm to use to generate Phrase 
        :param params: Array of params to pass into generative algorithm 
        
        :type algorithm: String 
        :type debug: List of params - varies per algorithm

        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        ALGORITHM_DICT = {"MapMod" : cls.generate_map_mod}

        if algorithm not in ALGORITHM_DICT.keys():
            raise ValueError("Generate algorithm invalid")
        else:
            cls.algorithm = algorithm
            cls.params = params

        phrase = ALGORITHM_DICT[cls.algorithm](cls.params)
        return phrase

    # Copy ctor for Generate
    @staticmethod
    def copy_ctor(old_generate):
        """Static copy constructor for Generate. 
        
        :param old_phrase: Generate object to copy 
        
        :type old_phrase: Generate 

        :return: Returns a Generate object, copy of old_generate 
        :rtype: Generate
        """
        return Generate(old_generate.algorithm, old_generate.params) 

    def generate_map_mod(params):
        """Generative algorithm that maps numbers to scale degrees
        and scale modulations based on an input file.
        
        :param params: Dictionary of parameters 
        :param params["scales"]: List of Scales to generate notes from (and
        modulate to)
        :param params["input"]: Input file to read from
        :param params["gen_len"]: How long of a phrase to generate

        :type params: Dictionary 
        :type params["scales"]: List
        :type params["input"]: Text file
        :type params["gen_len"]: int

        :return: Returns an array of Note objects
        :rtype: List
        """
        return params["scale"].notes

    # Str representation of Generate
    def __str__(self):
        """Utility function to print Generate.
       
        :return: String representation of Generate 
        :rtype: String 
        """
        return ("<Generate: algorithm: {}, params: {}>".format(
                self.algorithm, self.params))
