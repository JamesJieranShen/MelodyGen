#!/usr/bin/env python3
"""
.. module:: Signature
   :platform: Mac, Unix, Windows
   :synopsis: Signature object for MelodyGen 

.. moduleauthor:: James Shen 


"""
from fractions import Fraction
import constants as const

# This object describes a musical signature.
class Signature():

    def __init__(self, num_beats = 1, beat = Fraction('1/4'), 
            Signature = None):
        """ Default ctor. Creates a 1/4 signature with no inputs.
        :param num_beats:   number of beats in a measure.
        :param beat:        the value of one beat.
        :param Sinature:    Act as copy ctor when signarure is not None.
        
        :type num_beats:    int
        :type beat:         Fraction
        :type Signature     Signature

        :return:            Returns a Signature object
        :rtype:             Signature
        """
        if Signature is not None and isinstance(Signature, 
                classinfo = Signature):
            self.num_beats = Signature.num_beats
            self.beat = Signature.beat
            self._accents = Signature.get_accents()
        else:
            self.num_beats = num_beats
            self.beat = Fraction(beat) # Deep Copy
            self._accents = [False] * num_beats

    def isValid(self):
        """Validity checker for Signature.
        :param:     NONE

        :return:    True if signature is valid.
        :rtype:     Boolean
        """
        if self.num_beats != len(self._accents): 
            return False
        return True;

# Methods related to accents

    def get_accents(self, location = 1):
        """ Getter for _accents.
        :param location:    Location of the beat in the measure.
        :type location:     int

        :return:            True if is accented, false if otherwise.
        :rtype:             boolean
        """
        if location > self.num_beats or location < 1:
            print("CATASTROPHIC FAILURE: {0} is not a valid location".
                    format(location))
            return False

        return self._accents[location - 1]

    def toggle_accent(self, location):
        """Set accent to True if False, False if True
        :param location:    Location of the beat in the measure.
        :type location:     int

        :return:            True if is now accented, false if otherwise.
        :rtype:             boolean
        """
        if location > self._num_beats or location < 1:
            print("CATASTROPHIC FAILURE: {0} is not a valid location".
                    format(location))
            return False
        
        _accents[location] = not _accents[location]
        return _accents[location]
    
    def accent(self, location):
        """Set accent to True.
        :param location:    Location of the beat in the measure.
        :type location:     int

        :return:            Current state of location
        :rtype:             boolean
        """
        
        if location > self.num_beats or location < 1:
            print("CATASTROPHIC FAILURE: {0} is not a valid location".
                    format(location))
            return False
        self._accents[location] = True
        return self._accents[location]


    def unaccent(self, location):
        """Set accent to False.
        :param location:    Location of the beat in the measure.
        :type location:     int

        :return:            Current state of location
        :rtype:             boolean
        """
        
        if location > self.num_beats or location < 1:
            print("CATASTROPHIC FAILURE: {0} is not a valid location.".
             format(location))
            return False
        self._accents[location] = False
        return self._accents[location]
    def set_accent(self, accent_list):
        """Set accent according to accent_list
        :param accent_list:    List specifying accents. True is accent.
        :type accent_list:     list of boolean.

        :return:                True for success
        :rtype:                 boolean
        """
        if len(accent_list) != self.num_beats:
            print("CATASTROPHIC FAILURE: list is not valid.")
            return False
        for i in range(accent_list):
            self._accents[i] = accent_list[i]
        return True

# Other Setters and Getters
    def get_beat(self):
        return Fraction(self.beat)

    def get_num_beats(self):
        return self.num_beats

    def set_beat(self, beat):
        self.beat = Fraction(beat)

    def set_num_beats(self, num_beats):
        self.num_beats = num_beats
    
    def set_signature(self, num_beats, beatValue):
        self.num_beats = num_beats
        if isinstance(beatValue, int):
            self.beat = Fraction(1/beatValue)
        else:
            self.beat = Fraction(beatValue)

    def __str__(self):
        return "<Signature: %s  accents: [%s]>" % ( Fraction(self.num_beats * 
            self.beat), " ".join(str(x) for x in self._accents))



