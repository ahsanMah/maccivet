#!/usr/bin/python3

## Original script made by SunHyung (email: sunhyung.john.kim@gmail.com)
## 
## Dept. of Psychiatry @ UNC at Chapel Hill, modified 03.07.2017  
## PATH /nas02/home/s/h/shykim/CIVETv2.1/Linux-x86_64/init.csh
## optimized pipeline for IBIS data set
## full csf skel and two iteration for gm surface
## This script came from "Run_CIVETv2.1_CONTEv1.2.py"
## the diferent between v1.1 and v1.2 is input data has already xyflip or not.
######################################################################################################### 


import argparse, os
from subprocess import run


# runsh = lambda x: run(x,shell=True)

'''
Wrapper for the run function in the subprocess module
Will run the input string command as is in the shell
@Input: String to execute
'''

def runsh(exec_str, **kwargs):
	run(exec_str, **kwargs, shell=True)

'''
Warps the Macaque brain image to a human template space
'''
def convertToHuman(INPUT_T1, INPUT_SEG, INPUT_SUB):
	CIVET_SCRIPT_PATH = '/proj/NIRAL/tools/CIVET/CIVETv2.1-longleaf/Linux-x86_64/CIVET-2.1.0/'

	INPUT_T1_XYFLIP  = INPUT_T1.replace(".nrrd", "_xyFlip.nrrd")
	INPUT_SEG_XYFLIP = INPUT_SEG.replace(".nrrd",'_xyFlip.nrrd')
	INPUT_SUB_XYFLIP = INPUT_SUB.replace(".nrrd",'_xyFlip.nrrd')

	## Flip the xy axes if necessary as CIVET accepts LPI..?
	runsh("itk_convert {} {} --inv-x --inv-y".format(INPUT_T1, INPUT_T1_XYFLIP) )
	runsh("itk_convert {} {} --inv-x --inv-y".format(INPUT_SEG, INPUT_SEG_XYFLIP) )
	runsh("itk_convert {} {} --inv-x --inv-y".format(INPUT_SUB, INPUT_SUB_XYFLIP) )
	INPUT_T1 = INPUT_T1_XYFLIP
	INPUT_SEG = INPUT_SEG_XYFLIP
	INPUT_SUB = INPUT_SUB_XYFLIP

	##### TODO: SHOULD BE MADE AVILABLE VIA PARAMETER FILE ######
	Transform_MonkeyToHuman = '/nas/longleaf/home/shykim/21-MONKEY/new_MonkeyToHuman.txt'
	Human_Template = '/nas/longleaf/home/shykim/21-MONKEY/mni_target_xyflip.nrrd' ## MNI 0.5mm iso template 

	LikeHuman_T1 = INPUT_T1.replace(".nrrd", '_LikeHuman.nrrd' )
	LikeHuman_SEG = INPUT_SEG.replace(".nrrd", '_LikeHuman.nrrd')
	LikeHuman_SUB = INPUT_SUB.replace(".nrrd", '_LikeHuman.nrrd')


	runsh("BRAINSResample --inputVolume {} --outputVolume {} --referenceVolume {} --warpTransform {} --interpolationMode NearestNeighbor".format(INPUT_T1, LikeHuman_T1, Human_Template, Transform_MonkeyToHuman) )
	runsh("BRAINSResample --inputVolume {} --outputVolume {} --referenceVolume {} --warpTransform {} --interpolationMode NearestNeighbor".format(INPUT_SEG, LikeHuman_SEG, Human_Template, Transform_MonkeyToHuman) )
	runsh("BRAINSResample --inputVolume {} --outputVolume {} --referenceVolume {} --warpTransform {} --interpolationMode NearestNeighbor".format(INPUT_SUB, LikeHuman_SUB, Human_Template, Transform_MonkeyToHuman) )
	
	## CIVET accepts MINC files so we need one last conversion
	LikeHuman_T1_MINC = LikeHuman_T1.replace(".nrrd", '.mnc')
	LikeHuman_SEG_MINC = LikeHuman_SEG.replace(".nrrd", '.mnc')
	LikeHuman_SUB_MINC = LikeHuman_SUB.replace(".nrrd", '.mnc')

	runsh("itk_convert {} {} ".format(LikeHuman_T1, LikeHuman_T1_MINC) )
	runsh("itk_convert {} {} ".format(LikeHuman_SEG, LikeHuman_SEG_MINC) )
	runsh("itk_convert {} {} ".format(LikeHuman_SUB, LikeHuman_SUB_MINC) )

	return LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC

def warpMonkeyImage(Input_Img, Human_Template):
	##### TODO: SHOULD BE MADE AVILABLE VIA PARAMETER FILE ######
	Transform_MonkeyToHuman = '/nas/longleaf/home/shykim/21-MONKEY/new_MonkeyToHuman.txt'

	LikeHuman = Input_Img.replace(".nrrd", '_LikeHuman.nrrd' )
	runsh("BRAINSResample --inputVolume {} --outputVolume {} --referenceVolume {} --warpTransform {} --interpolationMode NearestNeighbor".format(Input_Img, LikeHuman, Human_Template, Transform_MonkeyToHuman) )

	## CIVET accepts MINC files so we need one last conversion
	LikeHuman_MINC = LikeHuman.replace(".nrrd", '.mnc')

	runsh("itk_convert {} {} ".format(LikeHuman, LikeHuman_MINC) )
	return LikeHuman_MINC


'''
Entry point for executing the modified CIVET pipeline
'''
def execute(args):

	LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC = convertToHuman(args.t1_image, args.seg_label, args.sub_label)

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
	execute(args)
	# print(args)

