######################################################################################################### 
### Second Phase of the processing pipeline
### It is mainly responsible for calculating PVEs specific to Macaque brains
######################################################################################################### 

import os
from helpers import runsh
from helpers import FileNames


def buildFileNames(INPUT_FILE_NAME):

	Current_dir = os.getcwd() + '/'
	files = FileNames() 

	files.CIVET_WORKING_PATH = Current_dir +  INPUT_FILE_NAME + '/'
	files.CIVET_CLASSIFY_PATH = files.CIVET_WORKING_PATH + 'classify/'
	files.CIVET_MINC_FINAL_PATH = files.CIVET_WORKING_PATH + 'final/'
	files.CIVET_TRANSFORM_LINEAR = files.CIVET_WORKING_PATH + 'transforms/linear/'
	files.CIVET_MASK_PATH = files.CIVET_WORKING_PATH + 'mask/'
	files.RSL_ABC_SEG  = files.CIVET_CLASSIFY_PATH + 'temp.mnc'
	files.RSL_ABC_SEG2 = files.CIVET_CLASSIFY_PATH + 'temp2.mnc'
	files.CLS_CLEAN    = files.CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_cls_clean.mnc'
	files.PVE_CLASSIFY = files.CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_classify.mnc'
	files.PVE_DISC     = files.CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_disc.mnc'
	files.PVE_EXACTCSF = files.CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactcsf.mnc'
	files.PVE_EXACTGM  = files.CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactgm.mnc'
	files.PVE_EXACTWM  = files.CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactwm.mnc'
	
	files.setFileName("REFERENCE_MINC", files.CIVET_MINC_FINAL_PATH + 'stx_' + INPUT_FILE_NAME + '_t1_final.mnc')
	files.setFileName("TAL_XFM", files.CIVET_TRANSFORM_LINEAR + 'stx_' + INPUT_FILE_NAME + '_t1_tal.xfm')

	return files

def cleanupFiles(files):
	
	# Cleaning up any existing output files
	runsh("rm {} {} {} {} {}".format(files.CLS_CLEAN, files.PVE_CLASSIFY, 
								files.PVE_DISC , files.PVE_EXACTGM , files.PVE_EXACTWM) )

def recalculatePVE(LikeHuman_SEG_MINC_exHippo,files):
	
	ABC_SEG_MINC = LikeHuman_SEG_MINC_exHippo
    runsh("mincresample -nearest_neighbour -byte -like {} {} {} -transformation {}".format(
            files.REFERENCE_MINC, ABC_SEG_MINC, files.RSL_ABC_SEG, files.TAL_XFM) )


    minc_cmd = "minccalc -byte -expr 'if(A[0]>{wm_low} && A[0]<{wm_high}){{out=3}}else if(A[0]>{gm_low} && A[0]<{gm_high}){{out=2}}else if(A[0]>{csf_low} && A[0]<{csf_high}){{out=1}}else if(A[0]>{thal_low} && A[0]<{thal_high}){{out=2}}else{{out=0}}' {input_file} {output_file}".format(
                    wm_low    = labels.WM - 0.4,
                    wm_high   = labels.WM + 0.4,
                    csf       = labels.CSF,
                    gm_low    = labels.GM - 0.4,
                    gm_high   = labels.GM + 0.4,
                    gm        = labels.GM,
                    csf_low   = labels.CSF - 0.4,
                    csf_high  = labels.CSF + 0.4,
                    thal_low  = labels.Thal - 0.2,
                    thal_high = labels.Thal + 0.2,
                    input_file = files.RSL_ABC_SEG,
                    output_file =  files.RSL_ABC_SEG2)
    runsh(minc_cmd)
	
	TEMP_CSF = files.CIVET_CLASSIFY_PATH + 'tmp_exactCSF.mnc' 	
	CSF_BIN = files.PVE_EXACTCSF[:-4] + '_binary.mnc'
	CSF_BIN_DIL = CSF_BIN[:-4] + '_dil.mnc'
	CSF_BIN_SKEL = CSF_BIN[:-4] + '_skel.mnc'
	CSF_BIN_SKEL_DEF = CSF_BIN_SKEL[:-4] + '_defrag.mnc'
	PVE_CG = files.CIVET_CLASSIFY_PATH + 'pve'

	# Remove noise
	runsh("minccalc -byte -expr 'if(A[0]>0.0 && A[1]>0){{out=1}}else{{out=0}}' {} {} {}".format(files.PVE_EXACTCSF, files.RSL_ABC_SEG2, CSF_BIN) )
	runsh("mincmorph -dilation {} {}".format(CSF_BIN, CSF_BIN_DIL) )
	runsh("skel {} {}".format(CSF_BIN_DIL, CSF_BIN_SKEL) )
	runsh("minccalc -byte -expr 'if( (A[0]>0.8 && A[0]<1.2) || A[1]>0){{out=1}}else{{out=0}}' {} {} {}".format(files.RSL_ABC_SEG2, CSF_BIN_SKEL, TEMP_CSF) )
	runsh("mincdefrag {} {} 1 27".format(TEMP_CSF, CSF_BIN_SKEL_DEF) )
	runsh("minccalc -byte -expr 'if(A[0]>0 && A[1]==2){{out=1}}else{{out=A[1]}}' {} {} {}".format(CSF_BIN_SKEL_DEF, files.RSL_ABC_SEG2, files.CLS_CLEAN) )
	runsh("rm {}".format(files.PVE_EXACTCSF) )
	runsh("cp {} {}".format(files.CLS_CLEAN, files.PVE_CLASSIFY) )
	runsh("cp {} {}".format(files.CLS_CLEAN, files.PVE_DISC) )
	runsh("minccalc -byte -expr 'if(A[0]>2.6 && A[0]<3.4){{out=1}}else{{out=0}}' {} {}".format(files.CLS_CLEAN, files.PVE_EXACTWM) )
	runsh("minccalc -byte -expr 'if(A[0]>1.6 && A[0]<2.4){{out=1}}else{{out=0}}' {} {}".format(files.CLS_CLEAN, files.PVE_EXACTGM) )
	runsh("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){{out=1}}else{{out=0}}' {} {}".format(files.CLS_CLEAN, files.PVE_EXACTCSF) )

def execute(INPUT_T1, LikeHuman_SEG_MINC_exHippo, parameters):
	print('''==================================\nBeginning Phase 2\n==================================''')

	global labels
	labels = parameters.labels

	files = buildFileNames(INPUT_T1)
	print(files)

	cleanupFiles(files)
	recalculatePVE(LikeHuman_SEG_MINC_exHippo,files)

	# RUN CIVET
	CIVET_cmd = "{civet_params} -reset-from cortical_masking -reset-to extract_white_surface_right -spawn -run {input_file} > {log_file}".format(
		        civet_params=parameters.civet, input_file=INPUT_T1, log_file=INPUT_T1+'_log')
	
	runsh(CIVET_cmd)
	# print(parameters.civet)
	return files

