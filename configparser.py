import json

class Parameters(object):
	"""This class will read a JSON parameter file and build the necessary strings
	   to be run in the command line
	"""

	# Expected keys in the parameter files - could be changed
	FLAGS = "flags"
	CIVET = "CIVET"
	CIVET_PATH = "CIVET_Path"
	FILEPATHS = "file_paths"

	def __init__(self, configfile):
		# Dictionary of the parameters adn their values
		self.config = {}
		# The CIVET command line arguments
		self.civet = {}
		# Paths to various files used by the pipeline
		self.filepaths = {}

		with open(configfile,'r') as cf:
			self.config = json.load(cf)

		self.buildFilePaths()
		self.buildCivetParams()


	'''Accepts a type of paramter and builds the corresponding string
	'''
	def buildCivetParams(self):
		params = self.config[Parameters.CIVET]

		final_str = ""
		flag_str = ""

		if Parameters.FLAGS in params:
			flag_str = " ".join(params[Parameters.FLAGS])
			params.pop(Parameters.FLAGS, None)

		concat = lambda x,y: "{} {}".format(x, y)
		args = " ".join([concat(p,params[p]) for p in params])

		final_str = "{}/CIVET_Processing_Pipeline {} {}".format(
			self.filepaths[Parameters.CIVET_PATH], flag_str, args)

		self.civet = final_str

	def buildFilePaths(self):
		self.filepaths = self.config[Parameters.FILEPATHS]