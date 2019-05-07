#!/usr/bin/env python3
"""
.. module:: generate
   :platform: Mac, Unix, Windows
   :synopsis: Generate module for MelodyGen 

.. moduleauthor:: Nicholas Schenone 


"""
import random
import time

# Generate object - takes in type of algorithm and array of params
class Generate:
    def __init__(self, algorithm, params):
        """Constructor for Generate object
        
        :param algorithm: Algorithm to use to generate Phrase 
        :param params: Array of params to pass into generative algorithm 
        
        :type algorithm: String 
        :type debug: List of params - varies per algorithm

        :return: Returns a Phrase object
        :rtype: Phrase 
        """
        ALGORITHM_DICT = {"MapMod": self.generate_map_mod}

        if algorithm not in ALGORITHM_DICT.keys():
            raise ValueError("Generate algorithm invalid")
        else:
            self.algorithm = algorithm
            self.params = params

        self.phrase = ALGORITHM_DICT[self.algorithm](self.params)

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
                raise ValueError(
                    "Generate {}: {} not specified".format(alg_name, param)
                )

    def generate_map_mod(self, params):
        """Generative algorithm that maps numbers to scale degrees
        and scale modulations based on an input file.
        
        :param params: Dictionary of parameters 
        :param params["scales"]: List of Scales to generate notes from
            (and modulate to)
        :param params["input_file"]: Input file to read from
        :param params["gen_len"]: How long of a phrase to generate
        :param params["file_offset"]: How many chars to offset before starting
            (optional)

        :type params: Dictionary 
        :type params["scales"]: List
        :type params["input_file"]: Text file
        :type params["gen_len"]: int
        :type params["file_offset"]: int

        :return: Returns an array of Note objects
        :rtype: List
        """
        # List of required params
        required_params = ["scales", "input_file", "gen_len"]

        # List of optional params
        optional_params = {"file_offset": 0, "note_len": 1 / 4, "note_len_mod": 1}

        # Error checking for required params
        Generate.check_req_params("MapMod", required_params, params)

        # Assign required params
        self.set_req_params(required_params, params)

        # Assign optional param
        self.set_opt_params(optional_params, params)

        # Local vars to generate phrase
        working_phrase = {}
        active_scale = self.scales[0]
        counter = 0  # Used to determine phrase end
        clock = 0  # Used to add note offset based on length

        # Read in one character at a time from file
        with open(self.input_file) as fileobj:
            for line in fileobj:
                for ch in line:

                    # Skip character based on file_offset
                    if self.file_offset > 0:
                        self.file_offset -= 1
                        continue

                    # Check if character is a number
                    if ch.isdigit():
                        ch_int = int(ch)
                        scale_thres = (
                            len(active_scale) - 1
                        ) / active_scale.num_octaves + 1

                        # If digit is between 0-scale length add note
                        if 0 <= ch_int <= scale_thres:
                            # Get note based on scale degree
                            note = active_scale.get_scale_degree(int(ch))
                            note.set_length(self.note_len)
                            note.set_length_mod(self.note_len_mod)

                            # Append scale degree of active_scale based on ch
                            working_phrase.update({note: clock})

                            # Update clock
                            clock += note.length * note.length_mod

                            # Counter logic to break after desired length
                            counter += 1
                            if counter >= self.gen_len:
                                break

                        # If digit is between scale length-9 change active_scale
                        elif scale_thres < ch_int <= 9:
                            active_scale = random.choice(self.scales)
        return working_phrase

    # Utility method to set required attributes
    def set_req_params(self, required_params, params):
        """Utility function to set required attributes 
       
        :param required_params: List of required parameters
        :param params: Dict of inputted parameters

        :type required_params: List
        :type params: Dict

        :return: None 
        """
        for req_param in required_params:
            setattr(self, req_param, params[req_param])

    # Utility method to set optional attributes
    def set_opt_params(self, optional_params, params):
        """Utility function to set optional attributes 
       
        :param optional_params: Dict of optional parameters
        :param params: Dict of inputted parameters

        :type optional_params: List
        :type params: Dict

        :return: None 
        """
        for opt_param in optional_params:
            if opt_param in params:
                setattr(self, opt_param, params[opt_param])
            else:
                setattr(self, opt_param, optional_params[opt_param])

    # Str representation of Generate
    def __str__(self):
        """Utility function to print Generate.
       
        :return: String representation of Generate 
        :rtype: String 
        """
        return "<Generate: algorithm: {}, params: {}>".format(
            self.algorithm, self.params
        )
