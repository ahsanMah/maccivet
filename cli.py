import argparse, os, re
from subprocess import run

import pipeline, helpers

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

	params = helpers.ConfigParser(args.paramfile)

	# print(params.filepaths)

	verify_file(args.t1_image)
	pipeline.execute(args, params)