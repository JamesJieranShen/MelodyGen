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
    
    @staticmethod
    def check_params(alg_name, required_params, params):
        """Static utility method that checks to make sure all required parameters
        were passed in to generative algorithm.
        
        :param alg_name: Name of algorithm 
        :param required_params: Required parameters
        :param params: Parameters passed in 

        :type params: String 
        :type params: List 
        :type params: Dict 

        :return: No return, raises ValueError 
        :rtype: None
        """
        for param in required_params:
            if param not in params.keys():
                raise ValueError("Generate {}: {} not specified".format(alg_name, param))
    
    def generate_map_mod(params):
        """Generative algorithm that maps numbers to scale degrees
        and scale modulations based on an input file.
        
        :param params: Dictionary of parameters 
        :param params["scales"]: List of Scales to generate notes from
            (and modulate to)
        :param params["input"]: Input file to read from
        :param params["gen_len"]: How long of a phrase to generate

        :type params: Dictionary 
        :type params["scales"]: List
        :type params["input"]: Text file
        :type params["gen_len"]: int

        :return: Returns an array of Note objects
        :rtype: List
        """
        # List of required params
        required_params = ["scales", "input", "gen_len"]
        
        # Error checking for params
        Generate.check_params("MapMod", required_params, params)

        # Local vars to generate phrase
        working_phrase = []
        active_scale = params["scales"][0]
        counter = 0

        # Read in one character at a time from file
        with open(params["input"]) as fileobj:
            for line in fileobj:  
                for ch in line: 
                    # Check if character is a number
                    if ch.isdigit():
                        ch_int = int(ch)
                        # If digit is between 0-scale length, add note
                        if (0 <= ch_int <= len(active_scale)):
                            # Append scale degree of active_scale based on ch
                            working_phrase.append(active_scale.get_scale_degree(int(ch)))
                            # Counter logic to break after desired length
                            counter += 1
                            if counter >= params["gen_len"]:
                                break
                        # If digit is between scale length -9, change active_scale
                        elif (len(active_scale) < ch_int <= 9):
                            active_scale = random.choice(params["scales"])

        return working_phrase 

    # Str representation of Generate
    def __str__(self):
        """Utility function to print Generate.
       
        :return: String representation of Generate 
        :rtype: String 
        """
        return ("<Generate: algorithm: {}, params: {}>".format(
                self.algorithm, self.params))
