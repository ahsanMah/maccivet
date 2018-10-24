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

	def __init__(self, config_json):
		self.strings = {}
		self.config = config_json


	'''Accepts a type of paramter and builds the corresponding string
	'''
	def buildParamString(self, ptype):
		params = self.config[ptype]
		final_str = ""
		flag_str = ""

		if Parameters.FLAGS in params:
			flag_str = " ".join(params[Parameters.FLAGS])
			params.pop(Parameters.FLAGS, None)

		concat = lambda x,y: "{} {}".format(x, y)
		args = " ".join([concat(p,params[p]) for p in params])

		final_str = "{}/CIVET_Processing_Pipeline {} {}".format(self.config[Parameters.CIVET_PATH], flag_str, args)

		self.strings[ptype] = final_str



'''
Specifies all the arguments that the parser can take

'''
def make_parser():
	parser = argparse.ArgumentParser()

	parser.add_argument("t1_image", help="T1-weighted input image")
	parser.add_argument("seg_label", help="label file that defines all the segmentations")
	parser.add_argument("sub_label", help="label file for subcortical structures like the hippocampus")

	return parser

def verify_file(fname):
	if not os.path.isfile(fname):
		raise FileNotFoundError("File \'{}\' does not exist".format(fname))




if __name__ == "__main__":
	print("Hello there!")
	parser = make_parser()

	args = parser.parse_args()

	config_params = {}
	with open("config.json",'r') as cf:
		config_params = json.load(cf)


	# for param in config_params:
	# 	print(buildParamString(config_params[param]))
	print(config_params)

	params = Parameters(config_params)
	params.buildParamString(Parameters.CIVET)
	print(params.strings)

	# verify_file(args.t1_image)
	# pipeline.execute(args)