import phase1, phase2

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


'''
Wrapper for the run function in the subprocess module
Will run the input string command as is in the shell
@Input: String to execute
'''

def runsh(exec_str, **kwargs):
	run(exec_str, **kwargs, shell=True)



def execute(args):
	INPUT_FILE_NAME, LikeHuman_SEG_MINC_exHippo = phase1.execute(args)

	phase2.execute(INPUT_FILE_NAME)
