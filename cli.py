import argparse, os, re
from subprocess import run

import pipeline, json



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


'''
Specifies all the arguments that the parser can take

'''
def make_parser():
	parser = argparse.ArgumentParser()

	parser.add_argument("t1_image", help="T1-weighted input image")
	parser.add_argument("seg_label", help="label file that defines all the segmentations")
	parser.add_argument("sub_label", help="label file for subcortical structures like the hippocampus")

	parser.add_argument("-p","--paramfile", default="config.json", help="path to custom parameter file (default is config.json)")

	return parser

def verify_file(fname):
	if not os.path.isfile(fname):
		raise FileNotFoundError("File \'{}\' does not exist".format(fname))




if __name__ == "__main__":
	print("Initializing...")
	parser = make_parser()

	args = parser.parse_args()

	params = Parameters(args.paramfile)

	print(params.filepaths)

	verify_file(args.t1_image)
	pipeline.execute(args, params)