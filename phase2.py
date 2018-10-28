### Second Phase of the processing pipeline
import os, helpers
Current_dir = os.getcwd() + '/'

'''
Wrapper for the run function in the subprocess module
Will run the input string command as is in the shell
@Input: String to execute
'''

def runsh(exec_str, **kwargs):
	run(exec_str, **kwargs, shell=True)


def buildFileNames(INPUT_FILE_NAME):

	files = helpers.FileNames() 

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
	
	return files

def cleanupFiles(files):
	
	# Cleaning up any existing output files
	runsh("rm {} {} {} {} {}".format(files.CLS_CLEAN, files.PVE_CLASSIFY, 
								files.PVE_DISC , files.PVE_EXACTGM , files.PVE_EXACTWM) )

def recalculatePVE():
	REFERENCE_MINC = CIVET_MINC_FINAL_PATH + 'stx_' + INPUT_FILE_NAME + '_t1_final.mnc'
	TAL_XFM = CIVET_TRANSFORM_LINEAR + 'stx_' + INPUT_FILE_NAME + '_t1_tal.xfm'
	
	runsh("mincresample -nearest -byte -like %s %s %s -transform %s" %(REFERENCE_MINC, ABC_SEG_MINC, RSL_ABC_SEG, TAL_XFM) )
	runsh("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=3}else if(A[0]>1.6 && A[0]<2.4){out=2}else if(A[0]>2.6 && A[0]<3.4){out=1}else if(A[0]>3.8 && A[0]<4.2){out=2}else{out=0}' %s %s" %(RSL_ABC_SEG, RSL_ABC_SEG2) )
	TEMP_CSF = files.CIVET_CLASSIFY_PATH + 'tmp_exactCSF.mnc' 	
	CSF_BIN = PVE_EXACTCSF[:-4] + '_binary.mnc'
	CSF_BIN_DIL = CSF_BIN[:-4] + '_dil.mnc'
	CSF_BIN_SKEL = CSF_BIN[:-4] + '_skel.mnc'
	CSF_BIN_SKEL_DEF = CSF_BIN_SKEL[:-4] + '_defrag.mnc'
	PVE_CG = CIVET_CLASSIFY_PATH + 'pve'

	# Remove noise
	runsh("minccalc -byte -expr 'if(A[0]>0.0 && A[1]>0){out=1}else{out=0}' %s %s %s" %(PVE_EXACTCSF, RSL_ABC_SEG2 ,CSF_BIN) )
	runsh("mincmorph -dilation %s %s" %(CSF_BIN, CSF_BIN_DIL) )
	runsh("skel %s %s" %(CSF_BIN_DIL, CSF_BIN_SKEL) )
	runsh("minccalc -byte -expr 'if( (A[0]>0.8 && A[0]<1.2) || A[1]>0){out=1}else{out=0}' %s %s %s" %(RSL_ABC_SEG2, CSF_BIN_SKEL, TEMP_CSF) )
	runsh("mincdefrag %s %s 1 27" %(TEMP_CSF, CSF_BIN_SKEL_DEF) )
	runsh("minccalc -byte -expr 'if(A[0]>0 && A[1]==2){out=1}else{out=A[1]}' %s %s %s" %(CSF_BIN_SKEL_DEF, RSL_ABC_SEG2, CLS_CLEAN) )
	runsh("rm %s" %(PVE_EXACTCSF) )
	runsh("cp %s %s" %(CLS_CLEAN,PVE_CLASSIFY) )
	runsh("cp %s %s" %(CLS_CLEAN,PVE_DISC) )
	runsh("minccalc -byte -expr 'if(A[0]>2.6 && A[0]<3.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTWM) )
	runsh("minccalc -byte -expr 'if(A[0]>1.6 && A[0]<2.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTGM) )
	runsh("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=1}else{out=0}' %s %s" %(CLS_CLEAN,PVE_EXACTCSF) )

def execute(INPUT_T1):
	print('''==================================\nBeginning Phase 2\n==================================''')

	files = buildFileNames(INPUT_T1)
	print(files)

