import phase1, phase2, phase3, phase4

######
# This file acts as a wrapper to run all the different phases in the pipeline in order.

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
WM = 1
GM = 2

HIPPO_L = 1
HIPPO_R = 5
################


#TODO: Use separate folders for log files and ouput files --> read from param file

def execute(args, params):
	print("------------ Starting CIVET Pipeline -------------")
	Stx_Input_T1, LikeHuman_SEG_MINC_exHippo = phase1.execute(args, params)

	files = phase2.execute(Stx_Input_T1, LikeHuman_SEG_MINC_exHippo, params)

	#phase3.execute(Stx_Input_T1, files, params)
	#phase4.execute(Stx_Input_T1, files, params)



