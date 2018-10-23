### Second Phase of the processing pipeline
import os
Current_dir = os.getcwd() + '/'

'''
Wrapper for the run function in the subprocess module
Will run the input string command as is in the shell
@Input: String to execute
'''
class FileNames(object):
	"""docstring for FileNames"""
	def __init__(self):
		self.CIVET_WORKING_PATH = None
		self.CIVET_CLASSIFY_PATH = None
		self.CIVET_MINC_FINAL_PATH = None
		self.CIVET_TRANSFORM_LINEAR = None
		self.CIVET_MASK_PATH = None
		self.RSL_ABC_SEG  = None
		self.RSL_ABC_SEG2 = None 
		self.CLS_CLEAN    = None
		self.PVE_CLASSIFY = None
		self.PVE_DISC     = None
		self.PVE_EXACTCSF = None
		self.PVE_EXACTGM  = None
		self.PVE_EXACTWM  = None

	def __str__(self):
		return "Parent Directory: {}".format(self.CIVET_WORKING_PATH)

def runsh(exec_str, **kwargs):
	run(exec_str, **kwargs, shell=True)


def buildFileNames(INPUT_FILE_NAME):

	files = FileNames() 

	files.CIVET_WORKING_PATH = Current_dir +  INPUT_FILE_NAME + '/'
	files.CIVET_CLASSIFY_PATH = files.CIVET_WORKING_PATH + 'classify/'
	files.CIVET_MINC_FINAL_PATH = files.CIVET_WORKING_PATH + 'final/'
	# files.CIVET_TRANSFORM_LINEAR = CIVET_WORKING_PATH + 'transforms/linear/'
	# files.CIVET_MASK_PATH = CIVET_WORKING_PATH + 'mask/'
	# files.RSL_ABC_SEG  = CIVET_CLASSIFY_PATH + 'temp.mnc'
	# files.RSL_ABC_SEG2  = CIVET_CLASSIFY_PATH + 'temp2.mnc'
	# files.CLS_CLEAN    = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_cls_clean.mnc'
	# files.PVE_CLASSIFY = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_classify.mnc'
	# files.PVE_DISC     = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_disc.mnc'
	# files.PVE_EXACTCSF = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactcsf.mnc'
	# files.PVE_EXACTGM  = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactgm.mnc'
	# files.PVE_EXACTWM  = CIVET_CLASSIFY_PATH + 'stx_' + INPUT_FILE_NAME + '_pve_exactwm.mnc'
	
	return files

def cleanupFiles(files):
	
	# Cleaning up any existing output files
	runsh("rm %s %s %s %s %s" %(files.CLS_CLEAN, files.PVE_CLASSIFY, 
								files.PVE_DISC , files.PVE_EXACTGM , files.PVE_EXACTWM) )


def macaquePVE():
	REFERENCE_MINC = CIVET_MINC_FINAL_PATH + 'stx_' + INPUT_FILE_NAME + '_t1_final.mnc'
	TAL_XFM = CIVET_TRANSFORM_LINEAR + 'stx_' + INPUT_FILE_NAME + '_t1_tal.xfm'
	
	os.system("mincresample -nearest -byte -like %s %s %s -transform %s" %(REFERENCE_MINC, ABC_SEG_MINC, RSL_ABC_SEG, TAL_XFM) )
	os.system("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=3}else if(A[0]>1.6 && A[0]<2.4){out=2}else if(A[0]>2.6 && A[0]<3.4){out=1}else if(A[0]>3.8 && A[0]<4.2){out=2}else{out=0}' %s %s" %(RSL_ABC_SEG, RSL_ABC_SEG2) )
	TEMP_CSF = CIVET_CLASSIFY_PATH + 'tmp_exactCSF.mnc' 	
	CSF_BIN = PVE_EXACTCSF[:-4] + '_binary.mnc'
	CSF_BIN_DIL = CSF_BIN[:-4] + '_dil.mnc'
	CSF_BIN_SKEL = CSF_BIN[:-4] + '_skel.mnc'
	CSF_BIN_SKEL_DEF = CSF_BIN_SKEL[:-4] + '_defrag.mnc'
	PVE_CG = CIVET_CLASSIFY_PATH + 'pve'

def execute(INPUT_T1):
	
	files = buildFileNames(INPUT_T1)
	print(files)

