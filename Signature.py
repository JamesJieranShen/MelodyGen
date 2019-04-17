#!/usr/bin/env python3
"""
.. module:: Signature
   :platform: Mac, Unix, Windows
   :synopsis: Signature object for MelodyGen 

.. moduleauthor:: James Shen 


"""
from fractions import Fraction
import Constants as const

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
        if Signature is not None 
            and isinstance(Signature, classinfo = Signature):
            self.num_beats = Signature.num_beats
            self.beat = Signature.beat
            self._accents = Signature.get_accents()
        else:
            self.num_beats = num_beats
            self.beat = Fraction(beat) # Deep Copy
            self._accents = [False] * num_beats
        
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
            print("CATASTROPHIC FAILURE: {0} is not a valid location".
                    format(location))
            return False
        self._accents[location] = False
        return self._accents[location]

    def isValid(self):
        # TODO
        pass

    def __str____(self):
        return """<Signature: %s  accents: [%s]>""" 
                % ( Fraction(self.num_beats * self.beat)
                    " ".join(str(x) for x in self._accents
                )



