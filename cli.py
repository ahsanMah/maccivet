#!/usr/bin/python3
import argparse, os
from subprocess import run


# runsh = lambda x: run(x,shell=True)

'''
Wrapper for the run function in the subprocess module 
@Input: String to execute
'''

def runsh(exec_str, **kwargs):
	run(exec_str, **kwargs, shell=True)


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
		print("File \'{}\' does not exist".format(fname))


if __name__ == "__main__":
	print("Hello there!")
	parser = make_parser()

	args = parser.parse_args()


	verify_file(args.t1_image)
	print(runsh("echo {}".format(args.t1_image), check=True))
	# print(args)

