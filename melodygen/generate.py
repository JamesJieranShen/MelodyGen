#!/usr/bin/env python3
"""
.. module:: Generate
   :platform: Mac, Unix, Windows
   :synopsis: Generate module for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import time

# Generate object - takes in type of algorithm and array of params 
class Generate():
    
    def __new__(self, algorithm, params):
        """Constructor for Generate object
        
        :param algorithm: Algorithm to use to generate Phrase 
        :param params: Array of params to pass into generative algorithm 
        
        :type algorithm: String 
        :type debug: List of params - varies per algorithm

        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        ALGORITHM_DICT = {"MapMod" : self.generate_map_mod}

        if algorithm not in ALGORITHM_DICT.keys():
            raise ValueError("Generate algorithm invalid")
        else:
            self.algorithm = algorithm
            self.params = params

        phrase = ALGORITHM_DICT[self.algorithm](self, self.params)
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
    def check_req_params(alg_name, required_params, params):
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
    
    def generate_map_mod(self, params):
        """Generative algorithm that maps numbers to scale degrees
        and scale modulations based on an input file.
        
        :param params: Dictionary of parameters 
        :param params["scales"]: List of Scales to generate notes from
            (and modulate to)
        :param params["input"]: Input file to read from
        :param params["gen_len"]: How long of a phrase to generate
        :param params["start_offset"] How many chars to offset before starting
            (optional)

        :type params: Dictionary 
        :type params["scales"]: List
        :type params["input"]: Text file
        :type params["gen_len"]: int
        :type params["start_offset"] int

        :return: Returns an array of Note objects
        :rtype: List
        """
        # List of required params
        required_params = ["scales", "input", "gen_len"]
        
        # List of optional params
        optional_params = {"start_offset": 0}

        # Error checking for required params
        Generate.check_req_params("MapMod", required_params, params)

        # Assign required params
        for req_param in required_params:
            setattr(self, req_param, params[req_param])

        # Assign optional param
        for opt_param in optional_params:
            if opt_param in params:    
                setattr(self, opt_param, params[opt_param])
            else:
                setattr(self, opt_param, optional_params[opt_param])

        # Local vars to generate phrase
        working_phrase = []
        active_scale = self.scales[0]
        counter = 0

        # Read in one character at a time from file
        with open(self.input) as fileobj:
            for line in fileobj:  
                for ch in line: 

                    # Skip character based on start_offset
                    if self.start_offset > 0:
                        self.start_offset -= 1
                        continue

                    # Check if character is a number
                    if ch.isdigit():
                        ch_int = int(ch)

                        # If digit is between 0-scale length add note
                        if (0 <= ch_int <= len(active_scale)):
                            # Append scale degree of active_scale based on ch
                            working_phrase.append(active_scale.get_scale_degree(
                                int(ch)))

                            # Counter logic to break after desired length
                            counter += 1
                            if counter >= self.gen_len:
                                break

                        # If digit is between scale length-9 change active_scale
                        elif (len(active_scale) < ch_int <= 9):
                            active_scale = random.choice(self.scales)

        return working_phrase 

    # Str representation of Generate
    def __str__(self):
        """Utility function to print Generate.
       
        :return: String representation of Generate 
        :rtype: String 
        """
        return ("<Generate: algorithm: {}, params: {}>".format(
                self.algorithm, self.params))
