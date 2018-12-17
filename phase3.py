# Phase 3
# Responsible for changing EM tissue segmentation into a compatible input for the CIVET pipeline
from helpers import runsh

def convert(files, INPUT_FILE_NAME):
	files.setFilePath("CIVET_SURF_PATH", files.CIVET_WORKING_PATH + 'surfaces/')
	files.setFilePath("CIVET_TEMP_PATH", files.CIVET_WORKING_PATH + 'temp/')
	files.setFilePath("SURF_LEFT_WM", files.CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_left_81920.obj')

	files.setFilePath("SURFtoVOL_LEFT", files.SURF_LEFT_WM[:-4] + '.mnc')
	files.setFilePath("SURFtoVOL_LEFT_DIL", files.SURFtoVOL_LEFT[:-4] + '_dil.mnc')
	files.setFilePath("SURFtoVOL_LEFT_DIL_SKEL", files.SURFtoVOL_LEFT_DIL[:-4] + '_skel.mnc')

	runsh("scan_object_to_volume {} {} {}".format(files.CLS_CLEAN, files.SURF_LEFT_WM, files.SURFtoVOL_LEFT) )  	
	runsh("mincmorph -dilation {} {}".format(files.SURFtoVOL_LEFT, files.SURFtoVOL_LEFT_DIL) )
	runsh("skel {} {}".format(files.SURFtoVOL_LEFT_DIL, files.SURFtoVOL_LEFT_DIL_SKEL) )

	files.setFilePath("SURF_RIGHT_WM", files.CIVET_SURF_PATH + 'stx_' + INPUT_FILE_NAME + '_white_surface_right_81920.obj')
	SURFtoVOL_RIGHT = files.SURF_RIGHT_WM[:-4] + '.mnc'
	SURFtoVOL_RIGHT_DIL = SURFtoVOL_RIGHT[:-4] + '_dil.mnc'
	SURFtoVOL_RIGHT_DIL_SKEL = SURFtoVOL_RIGHT_DIL[:-4] + '_skel.mnc'
	runsh("scan_object_to_volume %s %s %s" %(files.CLS_CLEAN, files.SURF_RIGHT_WM, SURFtoVOL_RIGHT) )  	
	runsh("mincmorph -dilation %s %s" %(SURFtoVOL_RIGHT, SURFtoVOL_RIGHT_DIL) )
	runsh("skel %s %s" %(SURFtoVOL_RIGHT_DIL, SURFtoVOL_RIGHT_DIL_SKEL) )

	CLS_CLEAN_COPY = files.CLS_CLEAN[:-4] + '_copy.mnc'
	runsh("mv %s %s" %(files.CLS_CLEAN, CLS_CLEAN_COPY) )
	
	runsh("minccalc -clobber -byte -expr 'if(A[0]>0 || A[1]>0){out=3}else{out=A[2]}' %s %s %s %s" %(files.SURFtoVOL_LEFT_DIL_SKEL, SURFtoVOL_RIGHT_DIL_SKEL, CLS_CLEAN_COPY, files.CLS_CLEAN ) )
	runsh("cp %s %s" %(files.CLS_CLEAN, files.PVE_CLASSIFY) )
	runsh("cp %s %s" %(files.CLS_CLEAN, files.PVE_DISC) )
	runsh("minccalc -clobber -byte -expr 'if(A[0]>2.6 && A[0]<3.4){out=1}else{out=0}' %s %s" %(files.CLS_CLEAN, files.PVE_EXACTWM) )
	runsh("minccalc -clobber -byte -expr 'if(A[0]>1.6 && A[0]<2.4){out=1}else{out=0}' %s %s" %(files.CLS_CLEAN, files.PVE_EXACTGM) )
	runsh("minccalc -clobber -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=1}else{out=0}' %s %s" %(files.CLS_CLEAN, files.PVE_EXACTCSF) )

def execute(STX_INPUT_T1, files, parameters):
	print('''==================================\nBeginning Phase 3\n==================================''')

	# Change EM tissue seg into input for CIVET pipeline
	convert(files, STX_INPUT_T1)

	# RUN CIVET
	CIVET_cmd = "{civet_params} -reset-from surface_classify -reset-to mid_surface_right -spawn -run {input_file} > {log_file}".format(
		        civet_params=parameters.civet, input_file=STX_INPUT_T1, log_file=STX_INPUT_T1+'_log')

	runsh(CIVET_cmd)
