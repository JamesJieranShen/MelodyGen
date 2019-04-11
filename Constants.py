"""
.. module:: Constants
   :platform: Mac, Unix, Windows
   :synopsis: List of constants for MelodyGen 

.. moduleauthor:: Nicholas Schenone 

"""

# Constant note/octave dictionaries
NOTE_DICT_NUMKEY = [ 0,   1,    2,   3,    4,   5,   6,    7,   8,    9,   10,   11]
"""
"""
NOTE_DICT_SHARPS = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]
"""
"""
NOTE_DICT_FLATS  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
"""
"""
OCTAVES = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
"""
"""

# Order of sharps/flats
ORDER_OF_SHARPS = ["F", "C", "G", "D", "A", "E", "B"]
"""
"""
ORDER_OF_FLATS  = ["B", "E", "A", "D", "G", "C", "F"]
"""
"""
SCALE_DICT = {'MAJOR':        [2, 2, 1, 2, 2, 2, 1],
              'IONIAN':       [2, 2, 1, 2, 2, 2, 1],
              'DORIAN':       [2, 1, 2, 2, 2, 1, 2],
              'PHRYGIAN':     [1, 2, 2, 2, 1 ,2, 2],
              'LYDIAN':       [2, 2, 2, 1, 2, 2, 1],
              'MIXOLYDIAN':   [2, 2, 1, 2, 2, 1, 2],
              'MINOR':        [2, 1, 2, 2, 1, 2, 2],
              'AEOLIAN':      [2, 1, 2, 2, 1, 2, 2],
              'LOCRIAN':      [1, 2, 2, 1, 2, 2, 2],
              'CHROMATIC':    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              'HARM_MINOR':   [2, 1, 2, 2, 1, 3, 1],
              'MAJOR_PENT':   [2, 2, 3, 2, 3],
              'MINOR_PENT':   [3, 2, 2, 3, 2],
              'BLUES':        [3, 2, 1, 1, 3, 2]}
"""
"""
MAJOR_MODE_DICT = ['MAJOR', 'IONIAN', 'LYDIAN', 'MIXOLYDIAN', 'CHROMATIC', 'MAJOR_PENT']
"""
"""
MINOR_MODE_DICT = ['MINOR', 'DORIAN', 'PHRYGIAN', 'AEOLIAN', 'LOCRIAN', 'MINOR_PENT', 'BLUES']
"""
"""
MAJOR_SHARP_FLAT_DICT = {'C': 'n', 'Cs': 's', 'Db': 'b', 'D': 's', 'Ds': 's', 'Eb': 'b',
                        'E': 's', 'F': 'b', 'Fs': 's', 'Gb': 'b', 'G': 's', 'Gs': 's',
                        'Ab': 'b', 'A': 's', 'As': 's', 'Bb': 'b', 'B': 's'}
"""
"""
MINOR_SHARP_FLAT_DICT = {'C': 'b', 'Cs': 's', 'Db': 'b', 'D': 'b', 'Ds': 's', 'Eb': 'b',
                        'E': 's', 'F': 'b', 'Fs': 's', 'Gb': 'b', 'G': 'b', 'Gs': 's',
                        'Ab': 'b', 'A': 'n', 'As': 's', 'Bb': 'b', 'B': 's'}
"""
"""
# Constant note length dictionaries
NOTE_TYPE_DICT = ["NOTE", "REST"]
"""
"""
NOTE_LEN_DICT = [1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1, 2]
"""
"""
NOTE_LEN_MOD_DICT = {"NONE": 1, "TRIPLET": 2/3, "DOTTED": 1.5}
"""
""" 
