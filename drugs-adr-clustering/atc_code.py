import numpy as np
first_level_codes = ['A','B','C','D','G','H','J','L','M','N','P','R','S','V']

def descriptor_length():
    return len(first_level_codes)

"""
    Class that contains information about the atc_code

    Working only with first level but is ready to add more
"""

class Atc_code(object):

    def __init__(self, atc_code):
        try:
            assert len(atc_code) == 7, "atc_code has 7 characters"
            self.code = atc_code
            self.build_levels()
        except(AttributeError, TypeError):
            raise AssertionError("atc_code should be a string")

    def build_levels(self):
        """ Right now just creating one level """

        self.levels = []
        self.levels.append(self.code[0])


    def get_level_index(self,level,val):
        """ Given the level of the ATC code and and the characterss of the level
            returns the index to the descriptor """

        assert level in range(7)
        return first_level_codes.index(val) # Change for more levels

    def get_atc_indexes(self):
        """ Iterates all atc levels and map to a index """

        return [self.get_level_index(level,val) for level, val in enumerate(self.levels)]

    def get_descriptor(self):
        """ Returns the descriptor for this atc code """

        descriptor = np.zeros(descriptor_length())
        for i in self.get_atc_indexes():
            descriptor[i] = 1

        return descriptor