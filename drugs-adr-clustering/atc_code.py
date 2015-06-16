import numpy as np
first_level_codes = ['A','B','C','D','G','H','J','L','M','N','P','R','S','V']

def descriptor_length():
	return len(first_level_codes)

'''
	Class that contains information about the atc_code

	Working only with first level but is ready to add more
'''
class Atc_code(object):

	def __init__(self, atc_code):
		try:
			assert len(atc_code) == 7, "atc_code has 7 characters"
			self.code = atc_code
			self.build_levels()
		except(AttributeError, TypeError):
			raise AssertionError("atc_code should be a string")

	'''
		Right now just creating one level
	'''
	def build_levels(self):
		self.levels = []
		self.levels.append(self.code[0])

	'''
		Given the level of the ATC code and and the characterss of the level
		returns the index to the descriptor
	'''
	def get_level_index(self,level,val):
		assert level in range(7)
		return first_level_codes.index(val) # Change for more levels

	'''
		Iterates all atc levels and map to a index
	'''
	def get_atc_indexes(self):
		return [self.get_level_index(level,val) for level, val in enumerate(self.levels)]

	'''
		Returns the descriptor for this atc code
	'''
	def get_descriptor(self):
		descriptor = np.zeros(descriptor_length())
		for i in self.get_atc_indexes():
			descriptor[i] = 1

		return descriptor