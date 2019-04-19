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
    def __init__(self, algorithm, params):
        """Constructor for Generate object
        
        :param algorithm: Algorithm to use to generate Phrase 
        :param params: Array of params to pass into generative algorithm 
        
        :type algorithm: String 
        :type debug: List of params - varies per algorithm

        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        self.algorithm = algorithm
        self.params = params
   
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

    # Str representation of Generate
    def __str__(self):
        """Utility function to print Generate.
       
        :return: String representation of Generate 
        :rtype: String 
        """
        return ("<Generate: algorithm: {}, params: {}>".format(
                self.algorithm, self.params))
