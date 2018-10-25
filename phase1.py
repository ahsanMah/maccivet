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


import argparse, os, re
from subprocess import run

#### Labels ####
# WM = 1
# GM = 2

# HIPPO_L = 1
# HIPPO_R = 5
################


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

	LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC = list(map(warpMonkeyImage, [INPUT_T1, INPUT_SEG, INPUT_SUB] ))

	return LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC

'''
Warps the Macaque brain image to the human template
'''
def warpMonkeyImage(Input_Img):
	##### TODO: SHOULD BE MADE AVILABLE VIA PARAMETER FILE ######
	Transform_MonkeyToHuman = PARAMS.filepaths["Transform_MonkeyToHuman"]
	Human_Template = PARAMS.filepaths["Human_Template"] ## MNI 0.5mm iso template 

	LikeHuman = Input_Img.replace(".nrrd", '_LikeHuman.nrrd' )
	runsh("BRAINSResample --inputVolume {} --outputVolume {} --referenceVolume {} --warpTransform {} --interpolationMode NearestNeighbor".format(Input_Img, LikeHuman, Human_Template, Transform_MonkeyToHuman) )

	## CIVET accepts MINC files so we need one last conversion
	LikeHuman_MINC = LikeHuman.replace(".nrrd", '.mnc')

	runsh("itk_convert {} {}".format(LikeHuman, LikeHuman_MINC) )
	return LikeHuman_MINC

def excludeHippo(LikeHuman_SUB_MINC, LikeHuman_SEG_MINC):
	LikeHuman_SUB_MINC_HIPPO = LikeHuman_SUB_MINC.replace(".mnc", '_Hippo.mnc')
	LikeHuman_SEG_MINC_exHippo = LikeHuman_SEG_MINC.replace(".mnc", '_excludeHippo.mnc')
	# Convert Hippo into WM
	# Note that the values (0.5,1.5,etc.) correspond to label values
	# # so they can vary and should be predefined by user in param file 1=WM label in seg_minc
	# runsh("minccalc -byte -expr 'if(A[0]>0.5 && A[0]<1.5 || A[0]>4.5 && A[0]<5.5 ){out=1}else{out=0}' %s %s" %(LikeHuman_SUB_MINC, LikeHuman_SUB_MINC_HIPPO) )
	# runsh("mincmorph -clobber -successive DD {} {}".format(LikeHuman_SUB_MINC_HIPPO, LikeHuman_SUB_MINC_HIPPO) )
	
	# # If label is 1, in Hippo file, then it is WM in exHippo
	# # o/w just label according to normal segemntation
	# runsh("minccalc -byte -expr 'if(A[0]>0){out=1}else{out=A[1]}' {} {} {}".format(LikeHuman_SUB_MINC_HIPPO, LikeHuman_SEG_MINC, LikeHuman_SEG_MINC_exHippo) )

	return LikeHuman_SUB_MINC_HIPPO, LikeHuman_SEG_MINC_exHippo


'''
Entry point for executing the modified CIVET pipeline
'''
def execute(args, param_obj):

	global PARAMS 
	PARAMS = param_obj

	LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC = convertToHuman(args.t1_image, args.seg_label, args.sub_label)
	# print(convertToHuman(args.t1_image, args.seg_label, args.sub_label))
	print(LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC)
	LikeHuman_SUB_MINC_HIPPO, LikeHuman_SEG_MINC_exHippo  = excludeHippo(LikeHuman_SUB_MINC, LikeHuman_SEG_MINC)

	INPUT_T1 = LikeHuman_T1_MINC
	
	# Build stx file if it doesn't exist
	prefix = "stx_"
	suffix = "_t1.mnc"
	if INPUT_T1.endswith(suffix) and INPUT_T1.startswith(prefix):
		exp = "^({})(.*)({})$".format(prefix, suffix)
		INPUT_FILE_NAME = re.match(exp, INPUT_T1).group(2)
	else:
		exp = "(.*)(\.mnc)$"
		INPUT_FILE_NAME = re.match(exp, INPUT_T1).group(1)
		ReINPUT_T1 = prefix + INPUT_FILE_NAME + suffix
		runsh("cp %s %s" %(INPUT_T1, ReINPUT_T1) )

	# RUN CIVET
	CIVET_Config = "{0} -prefix {1} -reset-to pve -spawn -run {2} > {3}".format(PARAMS.civet, prefix, INPUT_FILE_NAME, INPUT_FILE_NAME+'_log') 
	# runsh("%sCIVET_Processing_Pipeline -input_is_stx -surfreg-model mmuMonkey -prefix %s -sourcedir ./ -targetdir ./ -N3-distance 200 -template 0.50 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -combine-surface -animal -lobe_atlas icbm152nl-2009a -no-calibrate-white -reset-to pve -spawn -run %s > %s" %(CIVET_SCRIPT_PATH, prefix, INPUT_FILE_NAME, INPUT_FILE_NAME+'_log'))
	print(CIVET_Config)
	return INPUT_FILE_NAME, LikeHuman_SEG_MINC_exHippo
