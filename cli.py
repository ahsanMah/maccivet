#!/bin/usr/python
import argparse, os, re
import pipeline, helpers

'''
Specifies all the arguments that the parser can take
Note Absolute paths are required for directories
'''
def make_parser():
	parser = argparse.ArgumentParser()

	parser.add_argument("t1_image", help="T1-weighted input image")
	parser.add_argument("seg_label", help="label file that defines all the segmentations")
	parser.add_argument("sub_label", help="label file for subcortical structures like the hippocampus")

	parser.add_argument("-p","--paramfile", default="config.json", help="path to custom parameter file (default is config.json)")

	parser.add_argument("-in", "--inputdir", help="specify the path to the directory containg the input files (takes precedence over values set in parameter file)")

	return parser

def verify_file(fname):
	if not os.path.lexists(fname):
		raise FileNotFoundError("File \'{}\' does not exist".format(fname))


if __name__ == "__main__":
	print("Initializing...")
	parser = make_parser()

	args = parser.parse_args()

	params = helpers.ConfigParser(args.paramfile)

	# print(params.filepaths)
	os.chdir(params.cwd)
	print(os.getcwd())
	
	# Create symbolic links to input files in working directory
	for fname in [args.t1_image, args.seg_label, args.sub_label]:
		src = params.input_dir + "/" + fname
		if os.path.lexists(fname):
			os.unlink(fname) #Remove any pre-existing link
		os.symlink(src,fname)	
		verify_file(fname)

	# pipeline.execute(args, params)
