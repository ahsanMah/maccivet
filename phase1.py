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


import re
from helpers import runsh

'''
Registers the Macaque brain images to a human template space
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
Warps a Macaque brain image to a human template
'''
def warpMonkeyImage(Input_Img):
	Transform_MonkeyToHuman = Params.filepaths.Transform_MonkeyToHuman
	Human_Template = Params.filepaths.Human_Template ## MNI 0.5mm iso template 

	LikeHuman = Input_Img.replace(".nrrd", '_LikeHuman.nrrd' )
	runsh("BRAINSResample --inputVolume {} --outputVolume {} --referenceVolume {} --warpTransform {} --interpolationMode NearestNeighbor".format(
		   Input_Img, LikeHuman, Human_Template, Transform_MonkeyToHuman) )

	## CIVET accepts MINC files so we need one last conversion
	LikeHuman_MINC = LikeHuman.replace(".nrrd", '.mnc')

	runsh("itk_convert {} {}".format(LikeHuman, LikeHuman_MINC) )
	return LikeHuman_MINC

def excludeHippo(LikeHuman_SUB_MINC, LikeHuman_SEG_MINC):
	LikeHuman_SUB_MINC_HIPPO = LikeHuman_SUB_MINC.replace(".mnc", '_Hippo.mnc')
	LikeHuman_SEG_MINC_exHippo = LikeHuman_SEG_MINC.replace(".mnc", '_excludeHippo.mnc')
	
	# Convert Hippo into WM
	# Note that the values wm_low, wm_high etc. correspond to label values
	# There is a bug in minc where it cannot compare integers, so a range of floats is required instead
	# Recall labels can be predefined by user in configuration file
	minc_cmd = "minccalc -byte -expr 'if(A[0]>{lhippo_low} && A[0]<{lhippo_high} || A[0]>{rhippo_low} && A[0]<{rhippo_high} ){{out=1}}else{{out=0}}'".format(
		        lhippo_low  = labels.Hippo_L-0.5,
		        lhippo_high = labels.Hippo_R+0.5,
		        rhippo_low  = labels.Hippo_R-0.5,
		        rhippo_high = labels.Hippo_R+0.5)
	runsh(minc_cmd+ "{input} {output}".format(input=LikeHuman_SUB_MINC, output=LikeHuman_SUB_MINC_HIPPO) )
	runsh("mincmorph -clobber -successive DD {input} {output}".format(input=LikeHuman_SUB_MINC_HIPPO, output=LikeHuman_SUB_MINC_HIPPO) )
	
	# Create file without the hippocampal region
	runsh("minccalc -byte -expr 'if(A[0]>0){{out={wm}}}else{{out=A[1]}}' {hippo_only} {original_seg} {output}".format(
		   wm=labels.WM, hippo_only=LikeHuman_SUB_MINC_HIPPO, original_seg=LikeHuman_SEG_MINC, output=LikeHuman_SEG_MINC_exHippo) )

	return LikeHuman_SUB_MINC_HIPPO, LikeHuman_SEG_MINC_exHippo


'''
Entry point for executing the modified CIVET pipeline
'''
def execute(args, parameters):
	print('''==================================\nBeginning Phase 1\n==================================''')
	
	global Params, labels
	Params = parameters
	labels = parameters.labels

	LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC = convertToHuman(args.t1_image, args.seg_label, args.sub_label)

	print(LikeHuman_T1_MINC, LikeHuman_SEG_MINC, LikeHuman_SUB_MINC)

	LikeHuman_SUB_MINC_HIPPO, LikeHuman_SEG_MINC_exHippo  = excludeHippo(LikeHuman_SUB_MINC, LikeHuman_SEG_MINC)

	INPUT_T1 = LikeHuman_T1_MINC
	
	# Build stx file if it doesn't exist
	prefix = "stx_"
	suffix = "_t1.mnc"
	if INPUT_T1.endswith(suffix) and INPUT_T1.startswith(prefix):
		exp = "^({})(.*)({})$".format(prefix, suffix)
		stx_input = re.match(exp, INPUT_T1).group(2)
	else:
		exp = "(.*)(\.mnc)$"
		stx_input = re.match(exp, INPUT_T1).group(1)
		ReINPUT_T1 = prefix + stx_input + suffix
		runsh("cp %s %s" %(INPUT_T1, ReINPUT_T1) )

	# RUN CIVET
	CIVET_cmd = "{civet_params} -reset-to pve -spawn -run {input_file} > {log_file}".format(
		        civet_params=parameters.civet, input_file=stx_input, log_file=stx_input+'_log') 

	runsh(CIVET_cmd)
	return stx_input, LikeHuman_SEG_MINC_exHippo
