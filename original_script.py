#!/usr/bin/python

## made by SunHyung (email: sunhyung.john.kim@gmail.com)
## 
## Dept. of Psychiatry @ UNC at Chapel Hill, modified 03.07.2017  
## PATH /nas02/home/s/h/shykim/CIVETv2.1/Linux-x86_64/init.csh
## optimized pipeline for IBIS data set
## full csf skel and two iteration for gm surface
## This script came from "Run_CIVETv2.1_CONTEv1.2.py"
## the diferent between v1.1 and v1.2 is input data has already xyflip or not.
######################################################################################################### 

import sys
import os
from optparse import OptionParser

Current_dir = os.getcwd() + '/'

def main(opts, argv):
	
	Current_dir_len = len(Current_dir)
	CIVET_SCRIPT_PATH = '/proj/NIRAL/tools/CIVET/CIVETv2.1-longleaf/Linux-x86_64/CIVET-2.1.0/'
	INPUT_T1 = argv[0]
	INPUT_SEG = argv[1]
	INPUT_SUB = argv[2]

	INPUT_T1_XYFLIP = argv[0][:-5] + '_xyFlip.nrrd'
	INPUT_SEG_XYFLIP = argv[1][:-5] + '_xyFlip.nrrd'
	INPUT_SUB_XYFLIP = argv[2][:-5] + '_xyFlip.nrrd'


	## version v1.2.py
	os.system("itk_convert %s %s --inv-x --inv-y" %(INPUT_T1, INPUT_T1_XYFLIP) )
	os.system("itk_convert %s %s --inv-x --inv-y" %(INPUT_SEG, INPUT_SEG_XYFLIP) )
	os.system("itk_convert %s %s --inv-x --inv-y" %(INPUT_SUB, INPUT_SUB_XYFLIP) )
	INPUT_T1 = INPUT_T1_XYFLIP
	INPUT_SEG = INPUT_SEG_XYFLIP
	INPUT_SUB = INPUT_SUB_XYFLIP


	## version v1.1.py
	#Transform_MonkeyToHuman = '/nas02/home/s/h/shykim/21-MONKEY/MonkeyToHuman_rigid.txt'
	#Human_Template = '/nas02/home/s/h/shykim/21-MONKEY/mni_target.nrrd' ## MNI 0.5mm iso template 

	## version v1.2.py 
	Transform_MonkeyToHuman = '/nas/longleaf/home/shykim/21-MONKEY/new_MonkeyToHuman.txt'
	Human_Template = '/nas/longleaf/home/shykim/21-MONKEY/mni_target_xyflip.nrrd' ## MNI 0.5mm iso template 

	LikeHuman_T1 = INPUT_T1[:-5] + '_LikeHuman.nrrd' 
	LikeHuman_SEG = INPUT_SEG[:-5] + '_LikeHuman.nrrd'
	LikeHuman_SUB = INPUT_SUB[:-5] + '_LikeHuman.nrrd'

	os.system("BRAINSResample --inputVolume %s --outputVolume %s --referenceVolume %s --warpTransform %s --interpolationMode NearestNeighbor" %(INPUT_T1, LikeHuman_T1, Human_Template, Transform_MonkeyToHuman) )
	os.system("BRAINSResample --inputVolume %s --outputVolume %s --referenceVolume %s --warpTransform %s --interpolationMode NearestNeighbor" %(INPUT_SEG, LikeHuman_SEG, Human_Template, Transform_MonkeyToHuman) )
	os.system("BRAINSResample --inputVolume %s --outputVolume %s --referenceVolume %s --warpTransform %s --interpolationMode NearestNeighbor" %(INPUT_SUB, LikeHuman_SUB, Human_Template, Transform_MonkeyToHuman) )
	
	LikeHuman_T1_MINC = LikeHuman_T1[:-5] + '.mnc'
	LikeHuman_SEG_MINC = LikeHuman_SEG[:-5] + '.mnc'
	LikeHuman_SUB_MINC = LikeHuman_SUB[:-5] + '.mnc'	

	## version v1.1.py
	#os.system("itk_convert %s %s --inv-x --inv-y" %(LikeHuman_T1, LikeHuman_T1_MINC) )
	#os.system("itk_convert %s %s --inv-x --inv-y" %(LikeHuman_SEG, LikeHuman_SEG_MINC) )
	#os.system("itk_convert %s %s --inv-x --inv-y" %(LikeHuman_SUB, LikeHuman_SUB_MINC) )

	## version v1.2.py
	os.system("itk_convert %s %s " %(LikeHuman_T1, LikeHuman_T1_MINC) )
	os.system("itk_convert %s %s " %(LikeHuman_SEG, LikeHuman_SEG_MINC) )
	os.system("itk_convert %s %s " %(LikeHuman_SUB, LikeHuman_SUB_MINC) )
	
	#os.system("minc_modify_header %s -delete 'xspace:start' -delete 'yspace:start' -delete 'zspace:start' " %(INPUT_T1_MINC) )
	#os.system("minc_modify_header %s -dappend 'xspace:start= -96 ' -dappend 'yspace:start= -134 ' -dappend 'zspace:start= -72' " %(INPUT_T1_MINC) )

	LikeHuman_SUB_MINC_HIPPO = LikeHuman_SUB_MINC[:-4] + '_Hippo.mnc'
	LikeHuman_SEG_MINC_exHippo = LikeHuman_SEG_MINC[:-4] + '_excludeHippo.mnc'
	# Convert Hippo into WM
	os.system("minccalc -byte -expr 'if(A[0]>0.5 && A[0]<1.5 || A[0]>4.5 && A[0]<5.5 ){out=1}else{out=0}' %s %s" %(LikeHuman_SUB_MINC, LikeHuman_SUB_MINC_HIPPO) )
	os.system("mincmorph -clobber -successive DD %s %s" %(LikeHuman_SUB_MINC_HIPPO, LikeHuman_SUB_MINC_HIPPO) )
	os.system("minccalc -byte -expr 'if(A[0]>0){out=1}else{out=A[1]}' %s %s %s" %(LikeHuman_SUB_MINC_HIPPO, LikeHuman_SEG_MINC, LikeHuman_SEG_MINC_exHippo) )
	# out = wm_label
	#sys.exit(1)
		
  	INPUT_T1 = LikeHuman_T1_MINC
	
	prefix = "stx"
	suffix = "t1.mnc"
	if INPUT_T1.endswith(suffix) and INPUT_T1.startswith(prefix):
		INPUT_FILE_NAME = INPUT_T1[4:-7] 
		
	else:
		ReINPUT_T1 = prefix +'_'+ INPUT_T1[:-4]+'_t1.mnc'
		os.system("cp %s %s" %(INPUT_T1, ReINPUT_T1) )
		INPUT_FILE_NAME = ReINPUT_T1[4:-7] 
	
	# Setting up CIVET processing pipeline
	# Run up till PVE

	os.system("%sCIVET_Processing_Pipeline -input_is_stx -surfreg-model mmuMonkey -prefix %s -sourcedir ./ -targetdir ./ -N3-distance 200 -template 0.50 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -combine-surface -animal -lobe_atlas icbm152nl-2009a -no-calibrate-white -reset-to pve -spawn -run %s > %s" %(CIVET_SCRIPT_PATH, prefix, INPUT_FILE_NAME, INPUT_FILE_NAME+'_log'))

	## Segmentation Setting #####
	#ABC_SEG_NRRD = argv[1]
	#ABC_SEG_MINC = ABC_SEG_NRRD[:-5] + '.mnc'
	#os.system("ImageMathv1.3.3 %s -cleanComp 1,10 -outfile %s" %(ABC_SEG_NRRD, ABC_SEG_NRRD) )
	#os.system("itk_convert %s %s --inv-x --inv-y" %(ABC_SEG_NRRD, ABC_SEG_MINC) )
	#os.system("minc_modify_header %s -delete 'xspace:start' -delete 'yspace:start' -delete 'zspace:start' " %(ABC_SEG_MINC) )
	#os.system("minc_modify_header %s -dappend 'xspace:start= -96 ' -dappend 'yspace:start= -134 ' -dappend 'zspace:start= -72' " %(ABC_SEG_MINC) )

	ABC_SEG_MINC = LikeHuman_SEG_MINC_exHippo

	CIVET_WORKING_PATH = Current_dir +  INPUT_FILE_NAME + '/'
	CIVET_CLASSIFY_PATH = CIVET_WORKING_PATH + 'classify/'
	CIVET_MINC_FINAL_PATH = CIVET_WORKING_PATH + 'final/'
	CIVET_TRANSFORM_LINEAR = CIVET_WORKING_PATH + 'transforms/linear/'
	CIVET_MASK_PATH = CIVET_WORKING_PATH + 'mask/'
	RSL_ABC_SEG  = CIVET_CLASSIFY_PATH + 'temp.mnc'
	RSL_ABC_SEG2  = CIVET_CLASSIFY_PATH + 'temp2.mnc'
	CLS_CLEAN    = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_cls_clean.mnc'
	PVE_CLASSIFY = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_classify.mnc'
	PVE_DISC     = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_disc.mnc'
	PVE_EXACTCSF = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactcsf.mnc'
	PVE_EXACTGM  = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactgm.mnc'
	PVE_EXACTWM  = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactwm.mnc'
	
	# Cleaning up any existing output files
	os.system("rm %s %s %s %s %s" %(CLS_CLEAN, PVE_CLASSIFY, PVE_DISC , PVE_EXACTGM , PVE_EXACTWM) )

	REFERENCE_MINC = CIVET_MINC_FINAL_PATH + 'stx_' + INPUT_FILE_NAME + '_t1_final.mnc'
	TAL_XFM = CIVET_TRANSFORM_LINEAR + 'stx_' + INPUT_FILE_NAME + '_t1_tal.xfm'
	
	# Build Macaque PVE

	os.system("mincresample -nearest -byte -like %s %s %s -transform %s" %(REFERENCE_MINC, ABC_SEG_MINC, RSL_ABC_SEG, TAL_XFM) )
	os.system("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=3}else if(A[0]>1.6 && A[0]<2.4){out=2}else if(A[0]>2.6 && A[0]<3.4){out=1}else if(A[0]>3.8 && A[0]<4.2){out=2}else{out=0}' %s %s" %(RSL_ABC_SEG, RSL_ABC_SEG2) )
	TEMP_CSF = CIVET_CLASSIFY_PATH + 'tmp_exactCSF.mnc' 	
	CSF_BIN = PVE_EXACTCSF[:-4] + '_binary.mnc'
	CSF_BIN_DIL = CSF_BIN[:-4] + '_dil.mnc'
	CSF_BIN_SKEL = CSF_BIN[:-4] + '_skel.mnc'
	CSF_BIN_SKEL_DEF = CSF_BIN_SKEL[:-4] + '_defrag.mnc'
	PVE_CG = CIVET_CLASSIFY_PATH + 'pve'
	# Remove noise
	# ACTUAL PROB VALUES USED HERE
	os.system("minccalc -byte -expr 'if(A[0]>0.0 && A[1]>0){out=1}else{out=0}' %s %s %s" %(PVE_EXACTCSF, RSL_ABC_SEG2 ,CSF_BIN) )
	os.system("mincmorph -dilation %s %s" %(CSF_BIN, CSF_BIN_DIL) )
	os.system("skel %s %s" %(CSF_BIN_DIL, CSF_BIN_SKEL) )
	os.system("minccalc -byte -expr 'if( (A[0]>0.8 && A[0]<1.2) || A[1]>0){out=1}else{out=0}' %s %s %s" %(RSL_ABC_SEG2, CSF_BIN_SKEL, TEMP_CSF) )
	os.system("mincdefrag %s %s 1 27" %(TEMP_CSF, CSF_BIN_SKEL_DEF) )
	os.system("minccalc -byte -expr 'if(A[0]>0 && A[1]==2){out=1}else{out=A[1]}' %s %s %s" %(CSF_BIN_SKEL_DEF, RSL_ABC_SEG2, CLS_CLEAN) )
	os.system("rm %s" %(PVE_EXACTCSF) )
	os.system("cp %s %s" %(CLS_CLEAN,PVE_CLASSIFY) )
	os.system("cp %s %s" %(CLS_CLEAN,PVE_DISC) )
	os.system("minccalc -byte -expr 'if(A[0]>2.6 && A[0]<3.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTWM) )
	os.system("minccalc -byte -expr 'if(A[0]>1.6 && A[0]<2.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTGM) )
	os.system("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTCSF) )

	# Phase 2 = Change EM seg into civet pipeline
	os.system("%sCIVET_Processing_Pipeline -input_is_stx -surfreg-model mmuMonkey -prefix %s -sourcedir ./ -targetdir ./ -N3-distance 200 -template 0.50 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -combine-surface -animal -lobe_atlas icbm152nl-2009a -no-calibrate-white -reset-from cortical_masking -reset-to extract_white_surface_right -spawn -run %s > %s" %(CIVET_SCRIPT_PATH, prefix, INPUT_FILE_NAME, INPUT_FILE_NAME+'_log'))

	############## END OF PHASE 2 ##########################
	
	CIVET_SURF_PATH = CIVET_WORKING_PATH + 'surfaces/'
	CIVET_TEMP_PATH = CIVET_WORKING_PATH + 'temp/'
	SURF_LEFT_WM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_left_81920.obj'
	######SURF_LEFT_WM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_left_327680.obj'
	SURFtoVOL_LEFT = SURF_LEFT_WM[:-4] + '.mnc'
	SURFtoVOL_LEFT_DIL = SURFtoVOL_LEFT[:-4] + '_dil.mnc'
	SURFtoVOL_LEFT_DIL_SKEL = SURFtoVOL_LEFT_DIL[:-4] + '_skel.mnc'
	os.system("scan_object_to_volume %s %s %s" %(CLS_CLEAN, SURF_LEFT_WM, SURFtoVOL_LEFT) )  	
	os.system("mincmorph -dilation %s %s" %(SURFtoVOL_LEFT, SURFtoVOL_LEFT_DIL) )
	os.system("skel %s %s" %(SURFtoVOL_LEFT_DIL, SURFtoVOL_LEFT_DIL_SKEL) )

	SURF_RIGHT_WM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_right_81920.obj'
	######SURF_RIGHT_WM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_right_327680.obj'
	SURFtoVOL_RIGHT = SURF_RIGHT_WM[:-4] + '.mnc'
	SURFtoVOL_RIGHT_DIL = SURFtoVOL_RIGHT[:-4] + '_dil.mnc'
	SURFtoVOL_RIGHT_DIL_SKEL = SURFtoVOL_RIGHT_DIL[:-4] + '_skel.mnc'
	os.system("scan_object_to_volume %s %s %s" %(CLS_CLEAN, SURF_RIGHT_WM, SURFtoVOL_RIGHT) )  	
	os.system("mincmorph -dilation %s %s" %(SURFtoVOL_RIGHT, SURFtoVOL_RIGHT_DIL) )
	os.system("skel %s %s" %(SURFtoVOL_RIGHT_DIL, SURFtoVOL_RIGHT_DIL_SKEL) )

	#os.system("rm %s %s" %(SURF_LEFT_WM, SURF_RIGHT_WM) )
	CLS_CLEAN_COPY = CLS_CLEAN[:-4] + '_copy.mnc'
	os.system("mv %s %s" %(CLS_CLEAN, CLS_CLEAN_COPY) )
	
	os.system("minccalc -clobber -byte -expr 'if(A[0]>0 || A[1]>0){out=3}else{out=A[2]}' %s %s %s %s" %(SURFtoVOL_LEFT_DIL_SKEL, SURFtoVOL_RIGHT_DIL_SKEL, CLS_CLEAN_COPY, CLS_CLEAN ) )
	os.system("cp %s %s" %(CLS_CLEAN,PVE_CLASSIFY) )
	os.system("cp %s %s" %(CLS_CLEAN,PVE_DISC) )
	os.system("minccalc -clobber -byte -expr 'if(A[0]>2.6 && A[0]<3.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTWM) )
	os.system("minccalc -clobber -byte -expr 'if(A[0]>1.6 && A[0]<2.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTGM) )
	os.system("minccalc -clobber -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTCSF) )
		
	#os.system("rm %s" %(CIVET_TEMP_PATH + '*') )

	#os.system("%sCIVET_Processing_Pipeline -prefix %s -sourcedir ./ -targetdir ./ -N3-distance 200 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -combine-surface -animal -lobe_atlas icbm152nl-2009a -no-calibrate-white -reset-from cortical_masking -reset-to mid_surface_right -spawn -run %s > %s" %(CIVET_SCRIPT_PATH, prefix, INPUT_FILE_NAME, INPUT_FILE_NAME+'_log'))


	# Change EM tissue seg into input for CIVET pipeline

	os.system("%sCIVET_Processing_Pipeline -input_is_stx -surfreg-model mmuMonkey -prefix %s -sourcedir ./ -targetdir ./ -N3-distance 200 -template 0.50 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -combine-surface -animal -lobe_atlas icbm152nl-2009a -no-calibrate-white -reset-from surface_classify -reset-to mid_surface_right -spawn -run %s > %s" %(CIVET_SCRIPT_PATH, prefix, INPUT_FILE_NAME, INPUT_FILE_NAME+'_log'))

	###### Beginning of Phase 3 ################
	###### Expand GM to CSF boundary ###########


	### --> TEST
	##### 2nd iteration for GM surface from GM surface
	TEMPORAL_TIP_MASK_PATH = '/proj/NIRAL/tools/CIVET/CIVETv2.1/Linux-x86_64/share/mni-models/'
	TEMPORAL_TIP_MASK = TEMPORAL_TIP_MASK_PATH + 'TEMPORAL_MASK_avg152lin.mnc'
	MID_LINE_MASK = TEMPORAL_TIP_MASK_PATH + 'UNC_MiddleLine_Mask_Monkey.mnc'
	######SURF_LEFT_GM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_left_327680.obj'	
	######SURF_RIGHT_GM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_right_327680.obj'
	SURF_LEFT_GM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_left_81920.obj'	
	SURF_RIGHT_GM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_right_81920.obj'
	SURF_LEFT_GM_1st = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_left_1st_81920.obj'	
	SURF_RIGHT_GM_1st = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_right_1st_81920.obj'
	os.system("cp %s %s" %(SURF_LEFT_GM, SURF_LEFT_GM_1st) )
	os.system("cp %s %s" %(SURF_RIGHT_GM, SURF_RIGHT_GM_1st) )
	SURF_LEFT_MID = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_mid_surface_left_81920.obj'
	SURF_RIGHT_MID = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_mid_surface_right_81920.obj'	
	
	TEMP_FINAL_CLASSIFY = CIVET_TEMP_PATH + 'stx_' + INPUT_FILE_NAME + '_final_classify.mnc'
	TEMP_SUB_MASK = CIVET_TEMP_PATH + 'stx_' + INPUT_FILE_NAME + '_subcortical_mask.mnc'
	TEMP_FINAL_CALLOSUM = CIVET_TEMP_PATH + 'stx_' + INPUT_FILE_NAME + '_final_callosum.mnc'
	TEMP_CSF_SKEL = CIVET_TEMP_PATH + 'stx_' + INPUT_FILE_NAME + '_csf_skel.mnc'
	TEMP_PATH_2nd = CIVET_TEMP_PATH + '2nd/'
	os.system("mkdir %s" %(TEMP_PATH_2nd) )
	ORIG_CSF = TEMP_PATH_2nd + 'orig_csf.mnc'
	OUT_FIELD = TEMP_PATH_2nd + 'Out_Field.mnc'
	CLS_2ND = TEMP_PATH_2nd + 'CLS_2ND.mnc'
	
	ORIG_WM = TEMP_PATH_2nd + 'orig_wm.mnc'
	ORIG_WM_DILATION5 = TEMP_PATH_2nd + 'orig_wm_dil5.mnc'	
	ORIG_GM = TEMP_PATH_2nd + 'orig_gm.mnc'
	ORIG_GM_DILATION3_EROSION3 = TEMP_PATH_2nd + 'orig_gm_dil3_ero3.mnc'

	SPHERE = TEMP_PATH_2nd + 'sphere.obj'
	os.system("create_tetra %s 0 -20 10 70 100 80 20480" %(SPHERE) )
	R_TRAN = TEMP_PATH_2nd + 'x25_R.xfm'
	L_TRAN = TEMP_PATH_2nd + 'x25_L.xfm'
	TEMP_GM_LEFT = TEMP_PATH_2nd + 'gm_left.mnc'
	TEMP_GM_RIGHT = TEMP_PATH_2nd + 'gm_right.mnc'
	CENTER_GM_LEFT = TEMP_PATH_2nd + 'centered_gm_left.mnc'
	CENTER_GM_RIGHT = TEMP_PATH_2nd + 'centered_gm_right.mnc'
	os.system("param2xfm -translation -25 0 0 %s" %(R_TRAN) )
	os.system("param2xfm -translation 25 0 0 %s" %(L_TRAN) )
	os.system("scan_object_to_volume %s %s %s" %(REFERENCE_MINC, SURF_LEFT_GM_1st, TEMP_GM_LEFT) )
	os.system("scan_object_to_volume %s %s %s" %(REFERENCE_MINC, SURF_RIGHT_GM_1st, TEMP_GM_RIGHT) )

	os.system("mincresample -nearest -like %s %s %s -transform %s" %(REFERENCE_MINC, TEMP_GM_LEFT, CENTER_GM_LEFT, L_TRAN) )
	os.system("mincresample -nearest -like %s %s %s -transform %s" %(REFERENCE_MINC, TEMP_GM_RIGHT, CENTER_GM_RIGHT, R_TRAN) )

	LEFT_HULL_CENTER =  TEMP_PATH_2nd + 'Hull_left_centered.obj'
	RIGHT_HULL_CENTER =  TEMP_PATH_2nd + 'Hull_right_centered.obj'
	os.system("deform_surface %s none 0 0 0 %s %s none 10 1 -1 0.5 %s -0.8 0.8 0.1 0.1 100 0 1 1 3 0 0 0 1000 0.1 0.0" %(CENTER_GM_LEFT, SPHERE, LEFT_HULL_CENTER, SURF_LEFT_GM_1st) )
	os.system("deform_surface %s none 0 0 0 %s %s none 10 1 -1 0.5 %s -0.8 0.8 0.1 0.1 100 0 1 1 3 0 0 0 1000 0.1 0.0" %(CENTER_GM_RIGHT, SPHERE, RIGHT_HULL_CENTER, SURF_RIGHT_GM_1st) )

	LEFT_HULL =  TEMP_PATH_2nd + 'Hull_left.obj'
	RIGHT_HULL =  TEMP_PATH_2nd + 'Hull_right.obj'
	LEFT_HULL_MINC =  TEMP_PATH_2nd + 'Hull_left.mnc'
	RIGHT_HULL_MINC =  TEMP_PATH_2nd + 'Hull_right.mnc'
	os.system("transform_objects %s %s %s" %(LEFT_HULL_CENTER, R_TRAN, LEFT_HULL) )
	os.system("transform_objects %s %s %s" %(RIGHT_HULL_CENTER, L_TRAN, RIGHT_HULL) )
	os.system("scan_object_to_volume %s %s %s" %(REFERENCE_MINC, LEFT_HULL, LEFT_HULL_MINC) )
	os.system("scan_object_to_volume %s %s %s" %(REFERENCE_MINC, RIGHT_HULL, RIGHT_HULL_MINC) )

	LEFT_HULL_MINC_DILATION =  LEFT_HULL_MINC[:-4] + '_dil.mnc'
	RIGHT_HULL_MINC_DILATION =  RIGHT_HULL_MINC[:-4] + '_dil.mnc'
	os.system("mincmorph -dilation %s %s" %(LEFT_HULL_MINC, LEFT_HULL_MINC_DILATION) )
	os.system("mincmorph -dilation %s %s" %(RIGHT_HULL_MINC, RIGHT_HULL_MINC_DILATION) )
####
	WMGM = TEMP_PATH_2nd + 'wmgm.mnc'
	WMGM_DDDEEE = WMGM[:-4] + '_DDDEEE.mnc'
	WMGM_DDDEEEEEEEE = WMGM[:-4] + '_DDDEEEEEEEE.mnc'
	THIN_MASK = TEMP_PATH_2nd + 'thin_mask.mnc'
	os.system("minccalc -expr 'if(A[0]>1.8){out=1}else{out=0}' %s %s" %(TEMP_FINAL_CLASSIFY,WMGM) ) 
	os.system("mincmorph -successive DDDEEE %s %s" %(WMGM, WMGM_DDDEEE) )	
	os.system("mincmorph -successive DDDEEEEEEEE %s %s" %(WMGM, WMGM_DDDEEEEEEEE) ) 
	os.system("minccalc -byte -expr 'out=A[0]-A[1]' %s %s %s" %(WMGM_DDDEEE, WMGM_DDDEEEEEEEE, THIN_MASK) )
###
	DEEP = TEMP_PATH_2nd + 'deep.mnc'
	os.system("minccalc -byte -expr 'if( (A[0]==0 && A[1]>0) || (A[2]==0 && A[3]>0) ){out=1}else{out=0}' %s %s %s %s %s" %(LEFT_HULL_MINC_DILATION, TEMP_GM_LEFT, RIGHT_HULL_MINC_DILATION, TEMP_GM_RIGHT, DEEP ) )
	DEEP_DEFRAG = DEEP[:-4] + '_defrag.mnc'
	os.system("mincdefrag %s %s 1 27 10" %(DEEP, DEEP_DEFRAG) )

	CLS_2ND_TEMP = TEMP_PATH_2nd + 'CSL_2ND_temp.mnc'
	CLS_2ND_TEMP2 = TEMP_PATH_2nd + 'CSL_2ND_temp2.mnc'
	CLS_2ND_TEMP3 = TEMP_PATH_2nd + 'CSL_2ND_temp3.mnc'
	CLS_2ND_TEMP4 = TEMP_PATH_2nd + 'CSL_2ND_temp4.mnc'
	os.system("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=3}else if(A[0]>1.6 && A[0]<2.4){out=1}else if(A[0]>2.6 && A[0]< 5.4){out=3}else if(A[1]>0 && A[2]==1){out=1}else{out=A[3]}' %s %s %s %s %s" %(TEMP_SUB_MASK, DEEP_DEFRAG, TEMP_FINAL_CLASSIFY, RSL_ABC_SEG2,  CLS_2ND_TEMP) )

	#PARC_AUTOSEG_NRRD = argv[2]
	#PARC_AUTOSEG_MINC = TEMP_PATH_2nd + 'Parc_AutoSeg.mnc'
	#os.system("itk_convert %s %s --inv-x --inv-y" %(PARC_AUTOSEG_NRRD, PARC_AUTOSEG_MINC) )
	#os.system("minc_modify_header %s -delete 'xspace:start' -delete 'yspace:start' -delete 'zspace:start' " %(PARC_AUTOSEG_MINC) )	
	#os.system("minc_modify_header %s -dappend 'xspace:start= -96 ' -dappend 'yspace:start= -134 ' -dappend 'zspace:start= -72' " %(PARC_AUTOSEG_MINC) )
	
	#PARC_AUTOSEG_MINC_RSL = PARC_AUTOSEG_MINC[:-4] + '_rsl.mnc'
	#os.system("mincresample -byte -nearest -like %s %s %s -transform %s " %(REFERENCE_MINC, PARC_AUTOSEG_MINC, PARC_AUTOSEG_MINC_RSL, TAL_XFM) )
	
	#INSULA_MASK = TEMP_PATH_2nd + 'insula_mask.mnc'
	#os.system("minccalc -byte -expr 'if( (A[0]>5.5 && A[0]<6.5) || (A[0]>13.5 && A[0]<14.5) ){out=1}else{out=0}' %s %s" %(PARC_AUTOSEG_MINC_RSL, INSULA_MASK) )
	
	#os.system("minccalc -byte -expr 'if(A[0]>0 && A[1]>0){out=2}else if(A[2]>0 ){out=A[3]}else if(A[5]>0 && A[1]>0){out=2}else{out=A[4]}' %s %s %s %s %s %s %s" %(THIN_MASK, TEMP_CSF_SKEL, INSULA_MASK,  RSL_ABC_SEG2, CLS_2ND_TEMP,  TEMPORAL_TIP_MASK, CLS_2ND_TEMP2) )
	#os.system("minccalc -byte -expr 'if(A[0]>0 && A[1]>0){out=2}else if(A[2]>0 ){out=A[3]}else{out=A[4]}' %s %s %s %s %s %s" %(THIN_MASK, TEMP_CSF_SKEL, INSULA_MASK,  RSL_ABC_SEG2, CLS_2ND_TEMP, CLS_2ND_TEMP2) )
	os.system("minccalc -byte -expr 'if(A[0]>0 && A[1]>0){out=2}else{out=A[2]}' %s %s %s %s" %(THIN_MASK, TEMP_CSF_SKEL, CLS_2ND_TEMP, CLS_2ND_TEMP2) )
	
	WM_2ND_LEFT = TEMP_PATH_2nd + 'wm_2nd_mask_left.mnc'
	WM_2ND_RIGHT = TEMP_PATH_2nd + 'wm_2nd_mask_right.mnc'
	WM_2ND_LEFT_DD = TEMP_PATH_2nd + 'wm_2nd_mask_left_DD.mnc'
	WM_2ND_RIGHT_DD = TEMP_PATH_2nd + 'wm_2nd_mask_right_DD.mnc'
	WM_2ND =  TEMP_PATH_2nd + 'WM.mnc'
	WM_2ND_DD =  TEMP_PATH_2nd + 'WM_DD.mnc'
	os.system("surface_mask2 -binary_mask %s %s %s" %(CLS_2ND_TEMP2, SURF_LEFT_MID, WM_2ND_LEFT) )
	os.system("surface_mask2 -binary_mask %s %s %s" %(CLS_2ND_TEMP2, SURF_RIGHT_MID, WM_2ND_RIGHT) )
	os.system("mincmorph -successive DD %s %s" %(WM_2ND_LEFT, WM_2ND_LEFT_DD) )
	os.system("mincmorph -successive DD %s %s" %(WM_2ND_RIGHT, WM_2ND_RIGHT_DD) )
	os.system("minccalc -byte -expr 'if(A[0]>0 || A[1]>0){out=1}else{out=0}' %s %s %s" %(WM_2ND_LEFT, WM_2ND_RIGHT, WM_2ND) )
	os.system("minccalc -byte -expr 'if(A[0]>0 || A[1]>0){out=1}else{out=0}' %s %s %s" %(WM_2ND_LEFT_DD, WM_2ND_RIGHT_DD, WM_2ND_DD) )
	
	os.system("minccalc -byte -expr 'if(A[0]>0){out=3}else if(A[1]>0 && A[2]==1){out=1}else if(A[2]==2){out=2}else if(A[3]>0){out=2}else{out=A[2]}' %s %s %s %s %s" %(WM_2ND, WM_2ND_DD, CLS_2ND_TEMP2,WMGM_DDDEEE, CLS_2ND_TEMP3) )  

	os.system("minccalc -byte -expr 'if(A[0]>0 && A[1]==1){out=1}else{out=A[2]}' %s %s %s %s" %(MID_LINE_MASK, CLS_2ND_TEMP2, CLS_2ND_TEMP3, CLS_2ND_TEMP4) )
	CLS_2ND_TEMP2_CSF = CLS_2ND_TEMP2[:-4] + '_CSF.mnc'
	CLS_2ND_TEMP2_CSF_ED = CLS_2ND_TEMP2_CSF[:-4] + '_ED.mnc'
	os.system("minccalc -byte -expr 'if(A[0]>0 && A[0]<1.2){out=1}else{out=0}' %s %s" %(CLS_2ND_TEMP2, CLS_2ND_TEMP2_CSF) )
	os.system("mincmorph -successive ED %s %s" %(CLS_2ND_TEMP2_CSF, CLS_2ND_TEMP2_CSF_ED) )	
	os.system("minccalc -byte -expr 'if(A[0]>0){out=1}else{out=A[1]}' %s %s %s" %(CLS_2ND_TEMP2_CSF_ED, CLS_2ND_TEMP4, CLS_2ND) )

	###### make laplace grid ########
	CLS_2ND_CSF = TEMP_PATH_2nd + 'CLS_2ND_CSF.mnc'
	CLS_2ND_CSF_SKEL = TEMP_PATH_2nd + 'CLS_2ND_CSF_SKEL.mnc'
	SKULL_MASK = TEMP_PATH_2nd + 'skull_mask.mnc'
	PVE_GM_2ND = TEMP_PATH_2nd + 'pve_gm.mnc'
	os.system("minccalc -byte -expr 'if(A[0]==1){out=1}else{out=0}' %s %s" %(CLS_2ND, CLS_2ND_CSF) )
	os.system("skel %s %s" %(CLS_2ND_CSF, CLS_2ND_CSF_SKEL) )
	os.system("minccalc -byte -expr 'if(A[0]>0){out=1}else{out=0}' %s %s" %(CLS_2ND, SKULL_MASK) )
	os.system("minccalc -byte -expr 'if(A[0]>1.5 && A[0]<2.5){out=1}else{out=0}' %s %s" %(CLS_2ND, PVE_GM_2ND) )
	#os.system("make_asp_grid %s %s %s %s %s %s %s %s" %(REFERENCE_MINC, CLS_2ND_CSF_SKEL, SURF_LEFT_MID, SURF_RIGHT_MID, CLS_2ND, WM_2ND, TEMP_FINAL_CALLOSUM, OUT_FIELD ) )
	os.system("make_asp_grid %s %s %s %s %s %s %s %s %s %s" %(REFERENCE_MINC, SKULL_MASK, CLS_2ND_CSF_SKEL,  SURF_LEFT_MID, SURF_RIGHT_MID, CLS_2ND, PVE_GM_2ND, CLS_2ND, TEMP_FINAL_CALLOSUM, OUT_FIELD ) )
	

	######
	START_2nd_SURF_LEFT = CIVET_SURF_PATH + 'start_2nd_surf_left_81920.obj'
	START_2nd_SURF_RIGHT = CIVET_SURF_PATH + 'start_2nd_surf_right_81920.obj'
	OUT_SURF_TEST_LEFT = CIVET_SURF_PATH + 'out_left.obj'
	OUT_SURF_TEST_RIGHT = CIVET_SURF_PATH + 'out_right.obj'
	
	os.system("cp %s %s" %(SURF_LEFT_GM,START_2nd_SURF_LEFT) )
	os.system("cp %s %s" %(SURF_RIGHT_GM,START_2nd_SURF_RIGHT) )

	os.system("expand_from_white_2nd -left -init %s %s %s %s" %(START_2nd_SURF_LEFT, START_2nd_SURF_LEFT, OUT_SURF_TEST_LEFT, OUT_FIELD) )
	os.system("expand_from_white_2nd -right -init %s %s %s %s" %(START_2nd_SURF_RIGHT, START_2nd_SURF_RIGHT, OUT_SURF_TEST_RIGHT, OUT_FIELD) )

	OUT_SURF_TEST_LEFT = CIVET_SURF_PATH + 'out_left_81920.obj'
	OUT_SURF_TEST_RIGHT = CIVET_SURF_PATH + 'out_right_81920.obj'

	##### subdivide polygons #####
	
	HR_SURF_LEFT_WM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_left_327680.obj'
	HR_SURF_LEFT_GM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_left_327680.obj'	

	SURF_RIGHT_GM_FLIP = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_right_81920_flip.obj'
	SURF_RIGHT_WM_FLIP = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_right_81920_flip.obj'

	HR_SURF_RIGHT_WM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_right_327680.obj'
	HR_SURF_RIGHT_GM = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_right_327680.obj'
	HR_SURF_RIGHT_WM_FLIP = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_right_327680.obj'
	HR_SURF_RIGHT_GM_FLIP = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_right_327680.obj'


	FLIP_XFM = CIVET_SURF_PATH + 'flip.xfm'
	os.system("param2xfm -clobber -scales -1 1 1 %s" %(FLIP_XFM) )

	os.system("subdivide_polygons %s %s 327680" %(SURF_LEFT_WM, HR_SURF_LEFT_WM) )
	os.system("subdivide_polygons %s %s 327680" %(OUT_SURF_TEST_LEFT, HR_SURF_LEFT_GM) )

	os.system("transform_objects %s %s %s" %(SURF_RIGHT_WM, FLIP_XFM, SURF_RIGHT_WM_FLIP) )
	os.system("subdivide_polygons %s %s 327680" %(SURF_RIGHT_WM_FLIP, HR_SURF_RIGHT_WM) )
	os.system("transform_objects %s %s %s" %(HR_SURF_RIGHT_WM, FLIP_XFM, HR_SURF_RIGHT_WM) )

	os.system("transform_objects %s %s %s" %(OUT_SURF_TEST_RIGHT, FLIP_XFM, SURF_RIGHT_GM_FLIP) )
	os.system("subdivide_polygons %s %s 327680" %(SURF_RIGHT_GM_FLIP, HR_SURF_RIGHT_GM) )
	os.system("transform_objects %s %s %s" %(HR_SURF_RIGHT_GM, FLIP_XFM, HR_SURF_RIGHT_GM) )

	MID_LEFT = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_mid_surface_left_327680.obj'
	MID_RIGHT = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_mid_surface_right_327680.obj'
	os.system("average_surfaces %s none none 2 %s %s" %(MID_LEFT, HR_SURF_LEFT_WM, HR_SURF_LEFT_GM ) )
	os.system("average_surfaces %s none none 2 %s %s" %(MID_RIGHT, HR_SURF_RIGHT_WM, HR_SURF_RIGHT_GM) )

	FULL_GRAY = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface.obj'
	FULL_WHITE = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface.obj'
	FULL_MID = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_mid_surface.obj'

	os.system("objconcat %s %s none none %s none" %(MID_LEFT, MID_RIGHT, FULL_MID) )
	os.system("objconcat %s %s none none %s none" %(HR_SURF_LEFT_WM, HR_SURF_RIGHT_WM, FULL_WHITE) )
	os.system("objconcat %s %s none none %s none" %(HR_SURF_LEFT_GM, HR_SURF_RIGHT_GM, FULL_GRAY) )
##########  STOP GM Laplacian correction #########
	LOG_PATH = CIVET_WORKING_PATH + 'logs/'
	LOG_GRAY_SURF_LEFT_HIRES = LOG_PATH + INPUT_FILE_NAME + '.gray_surface_left_hires.log'
	LOG_GRAY_SURF_LEFT_HIRES_FIN = LOG_PATH + INPUT_FILE_NAME + '.gray_surface_left_hires.finished'
	LOG_GRAY_SURF_RIGHT_HIRES = LOG_PATH + INPUT_FILE_NAME + '.gray_surface_right_hires.log'
	LOG_GRAY_SURF_RIGHT_HIRES_FIN = LOG_PATH + INPUT_FILE_NAME + '.gray_surface_right_hires.finished'
	LOG_MID_SURF_LEFT = LOG_PATH + INPUT_FILE_NAME + '.mid_surface_left.log'
	LOG_MID_SURF_LEFT_FIN = LOG_PATH + INPUT_FILE_NAME + '.mid_surface_left.finished'
	LOG_MID_SURF_RIGHT =LOG_PATH + INPUT_FILE_NAME + '.mid_surface_right.log'
	LOG_MID_SURF_RIGHT_FIN = LOG_PATH + INPUT_FILE_NAME + '.mid_surface_right.finished'
	LOG_MID_FULL = LOG_PATH + INPUT_FILE_NAME + '.mid_surface_full.log'
	LOG_MID_FULL_FIN = LOG_PATH + INPUT_FILE_NAME + '.mid_surface_full.finished'
	LOG_WHITE_FULL = LOG_PATH + INPUT_FILE_NAME + '.white_surface_full.log'
	LOG_WHITE_FULL_FIN = LOG_PATH + INPUT_FILE_NAME + '.white_surface_full.finished'
	LOG_GRAY_FULL  = LOG_PATH + INPUT_FILE_NAME + '.gray_surface_full.log'
	LOG_GRAY_FULL_FIN  = LOG_PATH + INPUT_FILE_NAME + '.gray_surface_full.finished'

	UNC_EMPTY_LOG_FILE = TEMPORAL_TIP_MASK_PATH + 'UNC_empty_logfile.log'
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_LEFT_HIRES) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_LEFT_HIRES_FIN) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_RIGHT_HIRES) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_RIGHT_HIRES_FIN) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_LEFT) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_LEFT_FIN) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_RIGHT) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_RIGHT_FIN) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_MID_FULL) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_MID_FULL_FIN) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_WHITE_FULL) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_WHITE_FULL_FIN) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_GRAY_FULL) )
	os.system("cp %s %s" %(UNC_EMPTY_LOG_FILE,LOG_GRAY_FULL_FIN) )		

	######## Resuming civet pipeline --> surface registration  ########### 
	os.system("%sCIVET_Processing_Pipeline -input_is_stx -surfreg-model mmuMonkey -prefix %s -sourcedir ./ -targetdir ./ -N3-distance 200 -template 0.50 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -VBM -combine-surface -animal -lobe_atlas icbm152nl-2009a -hi-res-surfaces -no-calibrate-white -reset-after cls_volumes -spawn -run %s > %s" %(CIVET_SCRIPT_PATH, prefix, INPUT_FILE_NAME, INPUT_FILE_NAME+'_log'))
	######## Beginning of (Optional) Phase 4 #############
	######## Transform back to original space ###########

	TAL_XFM_INVERT = TAL_XFM[:-4] + '_invert.xfm'
	os.system("xfminvert %s %s" %(TAL_XFM, TAL_XFM_INVERT) )
	
	MID_LEFT_RSL = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_mid_surface_rsl_left_327680.obj'
	HR_SURF_LEFT_WM_RSL = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_rsl_left_327680.obj'
	HR_SURF_LEFT_GM_RSL = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_rsl_left_327680.obj'
	MID_RIGHT_RSL = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_mid_surface_rsl_right_327680.obj'
	HR_SURF_RIGHT_WM_RSL = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_rsl_right_327680.obj'
	HR_SURF_RIGHT_GM_RSL = CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_gray_surface_rsl_right_327680.obj'

	MID_LEFT_RSL_NATIVE = MID_LEFT_RSL[:-4] + '_native.obj'
	HR_SURF_LEFT_WM_RSL_NATIVE = HR_SURF_LEFT_WM_RSL[:-4] + '_native.obj'
	HR_SURF_LEFT_GM_RSL_NATIVE = HR_SURF_LEFT_GM_RSL[:-4] + '_native.obj'
	MID_RIGHT_RSL_NATIVE = MID_RIGHT_RSL[:-4] + '_native.obj'
	HR_SURF_RIGHT_WM_RSL_NATIVE = HR_SURF_RIGHT_WM_RSL[:-4] + '_native.obj'
	HR_SURF_RIGHT_GM_RSL_NATIVE = HR_SURF_RIGHT_GM_RSL[:-4] + '_native.obj'

	os.system("transform_objects %s %s %s" %(MID_LEFT_RSL ,TAL_XFM_INVERT, MID_LEFT_RSL_NATIVE) )
	os.system("transform_objects %s %s %s" %(HR_SURF_LEFT_WM_RSL ,TAL_XFM_INVERT, HR_SURF_LEFT_WM_RSL_NATIVE) )
	os.system("transform_objects %s %s %s" %(HR_SURF_LEFT_GM_RSL ,TAL_XFM_INVERT, HR_SURF_LEFT_GM_RSL_NATIVE) )
	os.system("transform_objects %s %s %s" %(MID_RIGHT_RSL ,TAL_XFM_INVERT, MID_RIGHT_RSL_NATIVE) )
	os.system("transform_objects %s %s %s" %(HR_SURF_RIGHT_WM_RSL ,TAL_XFM_INVERT, HR_SURF_RIGHT_WM_RSL_NATIVE) )
	os.system("transform_objects %s %s %s" %(HR_SURF_RIGHT_GM_RSL ,TAL_XFM_INVERT, HR_SURF_RIGHT_GM_RSL_NATIVE) )
	
	#if INPUT_T1.endswith(suffix) and INPUT_T1.startswith(prefix):
	#	os.system("rm %s" %(ABC_SEG_MINC) )
	#else:
	#	os.system("rm %s %s" %(ABC_SEG_MINC,ReINPUT_T1) )
		
	
##############################################################################################################

if (__name__ == "__main__"):
	parser = OptionParser(usage="%prog RAI_t1.nrrd RAI_SEG.nrrd Parcel_RAI_label_2(GM).nrrd ")
	#parser.add_option("-p","--preset",action="store_true", dest="PRESET", help="use the preset filename", default=False)
	#parser.add_option("-c","--stepCIVET",action="store_true", dest="verboseModel", default=False, help="Process CIVET")
	#parser.add_option("-s","--stepSeg",action="store_true", dest="verboseSeg", default=False, help="stx registraion of CIVET and EM Segmenation")
	#parser.add_option("-v",action="store", dest="Visit",type="string", help="Visit (e.g. V12, V24..)",default="")
	#parser.add_option("-m",action="store", dest="MaskName", type="string", help="Change Mask. If you change mask, you have to use option '-b' mask based t1w image", default="")
	#parser.add_option("-b",action="store", dest="MaskBase", type="string", help="Mask T1w based image", default="")
	#parser.add_option("-t",action="store", dest="T1T2Mask",type="string", help="use t1w and t2w bet mask, -t 'operator'(e.g. and,or)" )
	#parser.add_option("-k","--KeepSegAll", action="store_false", dest="verboseErase", default=True, help="keep all the temporay files during IGM-EM segmentation process")
	(opts, argv) = parser.parse_args()	
	if (len(argv)<1):
 		parser.os.system_help()
		sys.exit(0)
	main(opts, argv)