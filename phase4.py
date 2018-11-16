######################################################################################################### 
### Phase 4
### Expands the gray matter to the CSF boundary to improve results
######################################################################################################### 
from helpers import runsh

##### 2nd iteration	for GM surface from GM surface
def runSecondIter(Stx_Input_T1, files, parameters):

	TEMPORAL_TIP_MASK_PATH = parameters.filepaths.Temporal_Masks_Path
	TEMPORAL_TIP_MASK = TEMPORAL_TIP_MASK_PATH + parameters.filepaths.Temporal_Tip_Mask
	MID_LINE_MASK = TEMPORAL_TIP_MASK_PATH + parameters.filepaths.Midline_Mask
	
	SURF_LEFT_GM = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_left_81920.obj'	
	SURF_RIGHT_GM = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_right_81920.obj'
	SURF_LEFT_GM_1st = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_left_1st_81920.obj'	
	SURF_RIGHT_GM_1st = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_right_1st_81920.obj'
	runsh("cp {} {}".format(SURF_LEFT_GM, SURF_LEFT_GM_1st) )
	runsh("cp {} {}".format(SURF_RIGHT_GM, SURF_RIGHT_GM_1st) )
	SURF_LEFT_MID = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_left_81920.obj'
	SURF_RIGHT_MID = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_right_81920.obj'	
	
	TEMP_FINAL_CLASSIFY = files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_final_classify.mnc'
	TEMP_SUB_MASK = files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_subcortical_mask.mnc'
	TEMP_FINAL_CALLOSUM = files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_final_callosum.mnc'
	TEMP_CSF_SKEL = files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_csf_skel.mnc'
	TEMP_PATH_2nd = files.CIVET_TEMP_PATH + '2nd/'
	runsh("mkdir {}".format(TEMP_PATH_2nd) )
	ORIG_CSF = TEMP_PATH_2nd + 'orig_csf.mnc'
	OUT_FIELD = TEMP_PATH_2nd + 'Out_Field.mnc'
	CLS_2ND = TEMP_PATH_2nd + 'CLS_2ND.mnc'
	
	ORIG_WM = TEMP_PATH_2nd + 'orig_wm.mnc'
	ORIG_WM_DILATION5 = TEMP_PATH_2nd + 'orig_wm_dil5.mnc'	
	ORIG_GM = TEMP_PATH_2nd + 'orig_gm.mnc'
	ORIG_GM_DILATION3_EROSION3 = TEMP_PATH_2nd + 'orig_gm_dil3_ero3.mnc'

	SPHERE = TEMP_PATH_2nd + 'sphere.obj'
	runsh("create_tetra {} 0 -20 10 70 100 80 20480".format(SPHERE) )
	R_TRAN = TEMP_PATH_2nd + 'x25_R.xfm'
	L_TRAN = TEMP_PATH_2nd + 'x25_L.xfm'
	TEMP_GM_LEFT = TEMP_PATH_2nd + 'gm_left.mnc'
	TEMP_GM_RIGHT = TEMP_PATH_2nd + 'gm_right.mnc'
	CENTER_GM_LEFT = TEMP_PATH_2nd + 'centered_gm_left.mnc'
	CENTER_GM_RIGHT = TEMP_PATH_2nd + 'centered_gm_right.mnc'
	runsh("param2xfm -translation -25 0 0 {}".format(R_TRAN) )
	runsh("param2xfm -translation 25 0 0 {}".format(L_TRAN) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, SURF_LEFT_GM_1st, TEMP_GM_LEFT) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, SURF_RIGHT_GM_1st, TEMP_GM_RIGHT) )

	runsh("mincresample -nearest -like {} {} {} -transform {}".format(files.REFERENCE_MINC, TEMP_GM_LEFT, CENTER_GM_LEFT, L_TRAN) )
	runsh("mincresample -nearest -like {} {} {} -transform {}".format(files.REFERENCE_MINC, TEMP_GM_RIGHT, CENTER_GM_RIGHT, R_TRAN) )

	LEFT_HULL_CENTER =  TEMP_PATH_2nd + 'Hull_left_centered.obj'
	RIGHT_HULL_CENTER =  TEMP_PATH_2nd + 'Hull_right_centered.obj'
	runsh("deform_surface {} none 0 0 0 {} {} none 10 1 -1 0.5 {} -0.8 0.8 0.1 0.1 100 0 1 1 3 0 0 0 1000 0.1 0.0".format(CENTER_GM_LEFT, SPHERE, LEFT_HULL_CENTER, SURF_LEFT_GM_1st) )
	runsh("deform_surface {} none 0 0 0 {} {} none 10 1 -1 0.5 {} -0.8 0.8 0.1 0.1 100 0 1 1 3 0 0 0 1000 0.1 0.0".format(CENTER_GM_RIGHT, SPHERE, RIGHT_HULL_CENTER, SURF_RIGHT_GM_1st) )

	LEFT_HULL =  TEMP_PATH_2nd + 'Hull_left.obj'
	RIGHT_HULL =  TEMP_PATH_2nd + 'Hull_right.obj'
	LEFT_HULL_MINC =  TEMP_PATH_2nd + 'Hull_left.mnc'
	RIGHT_HULL_MINC =  TEMP_PATH_2nd + 'Hull_right.mnc'
	runsh("transform_objects {} {} {}".format(LEFT_HULL_CENTER, R_TRAN, LEFT_HULL) )
	runsh("transform_objects {} {} {}".format(RIGHT_HULL_CENTER, L_TRAN, RIGHT_HULL) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, LEFT_HULL, LEFT_HULL_MINC) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, RIGHT_HULL, RIGHT_HULL_MINC) )

	LEFT_HULL_MINC_DILATION =  LEFT_HULL_MINC[:-4] + '_dil.mnc'
	RIGHT_HULL_MINC_DILATION =  RIGHT_HULL_MINC[:-4] + '_dil.mnc'
	runsh("mincmorph -dilation {} {}".format(LEFT_HULL_MINC, LEFT_HULL_MINC_DILATION) )
	runsh("mincmorph -dilation {} {}".format(RIGHT_HULL_MINC, RIGHT_HULL_MINC_DILATION) )
####
	WMGM = TEMP_PATH_2nd + 'wmgm.mnc'
	WMGM_DDDEEE = WMGM[:-4] + '_DDDEEE.mnc'
	WMGM_DDDEEEEEEEE = WMGM[:-4] + '_DDDEEEEEEEE.mnc'
	THIN_MASK = TEMP_PATH_2nd + 'thin_mask.mnc'
	runsh("minccalc -expr 'if(A[0]>1.8){{out=1}}else{{out=0}}' {} {}".format(TEMP_FINAL_CLASSIFY,WMGM) ) 
	runsh("mincmorph -successive DDDEEE {} {}".format(WMGM, WMGM_DDDEEE) )	
	runsh("mincmorph -successive DDDEEEEEEEE {} {}".format(WMGM, WMGM_DDDEEEEEEEE) ) 
	runsh("minccalc -byte -expr 'out=A[0]-A[1]' {} {} {}".format(WMGM_DDDEEE, WMGM_DDDEEEEEEEE, THIN_MASK) )
###
	DEEP = TEMP_PATH_2nd + 'deep.mnc'
	runsh("minccalc -byte -expr 'if( (A[0]==0 && A[1]>0) || (A[2]==0 && A[3]>0) ){{out=1}}else{{out=0}}' {} {} {} {} {}".format(LEFT_HULL_MINC_DILATION, TEMP_GM_LEFT, RIGHT_HULL_MINC_DILATION, TEMP_GM_RIGHT, DEEP ) )
	DEEP_DEFRAG = DEEP[:-4] + '_defrag.mnc'
	runsh("mincdefrag {} {} 1 27 10".format(DEEP, DEEP_DEFRAG) )

	CLS_2ND_TEMP = TEMP_PATH_2nd + 'CSL_2ND_temp.mnc'
	CLS_2ND_TEMP2 = TEMP_PATH_2nd + 'CSL_2ND_temp2.mnc'
	CLS_2ND_TEMP3 = TEMP_PATH_2nd + 'CSL_2ND_temp3.mnc'
	CLS_2ND_TEMP4 = TEMP_PATH_2nd + 'CSL_2ND_temp4.mnc'
	runsh("minccalc -byte -expr 'if(A[0]>0.6 && A[0]<1.4){out=3}else if(A[0]>1.6 && A[0]<2.4){{out=1}}else if(A[0]>2.6 && A[0]< 5.4){{out=3}}else if(A[1]>0 && A[2]==1){{out=1}}else{{out=A[3]}}' {} {} {} {} {}".format(TEMP_SUB_MASK, DEEP_DEFRAG, TEMP_FINAL_CLASSIFY, RSL_ABC_SEG2,  CLS_2ND_TEMP) )
	runsh("minccalc -byte -expr 'if(A[0]>0 && A[1]>0){{out=2}}else{{out=A[2]}}' {} {} {} {}".format(THIN_MASK, TEMP_CSF_SKEL, CLS_2ND_TEMP, CLS_2ND_TEMP2) )
	
	WM_2ND_LEFT = TEMP_PATH_2nd + 'wm_2nd_mask_left.mnc'
	WM_2ND_RIGHT = TEMP_PATH_2nd + 'wm_2nd_mask_right.mnc'
	WM_2ND_LEFT_DD = TEMP_PATH_2nd + 'wm_2nd_mask_left_DD.mnc'
	WM_2ND_RIGHT_DD = TEMP_PATH_2nd + 'wm_2nd_mask_right_DD.mnc'
	WM_2ND =  TEMP_PATH_2nd + 'WM.mnc'
	WM_2ND_DD =  TEMP_PATH_2nd + 'WM_DD.mnc'
	runsh("surface_mask2 -binary_mask {} {} {}".format(CLS_2ND_TEMP2, SURF_LEFT_MID, WM_2ND_LEFT) )
	runsh("surface_mask2 -binary_mask {} {} {}".format(CLS_2ND_TEMP2, SURF_RIGHT_MID, WM_2ND_RIGHT) )
	runsh("mincmorph -successive DD {} {}".format(WM_2ND_LEFT, WM_2ND_LEFT_DD) )
	runsh("mincmorph -successive DD {} {}".format(WM_2ND_RIGHT, WM_2ND_RIGHT_DD) )
	runsh("minccalc -byte -expr 'if(A[0]>0 || A[1]>0){out=1}else{out=0}' {} {} {}".format(WM_2ND_LEFT, WM_2ND_RIGHT, WM_2ND) )
	runsh("minccalc -byte -expr 'if(A[0]>0 || A[1]>0){out=1}else{out=0}' {} {} {}".format(WM_2ND_LEFT_DD, WM_2ND_RIGHT_DD, WM_2ND_DD) )
	
	runsh("minccalc -byte -expr 'if(A[0]>0){out=3}else if(A[1]>0 && A[2]==1){out=1}else if(A[2]==2){out=2}else if(A[3]>0){out=2}else{out=A[2]}' {} {} {} {} {}".format(WM_2ND, WM_2ND_DD, CLS_2ND_TEMP2,WMGM_DDDEEE, CLS_2ND_TEMP3) )  

	runsh("minccalc -byte -expr 'if(A[0]>0 && A[1]==1){out=1}else{out=A[2]}' {} {} {} {}".format(MID_LINE_MASK, CLS_2ND_TEMP2, CLS_2ND_TEMP3, CLS_2ND_TEMP4) )
	CLS_2ND_TEMP2_CSF = CLS_2ND_TEMP2[:-4] + '_CSF.mnc'
	CLS_2ND_TEMP2_CSF_ED = CLS_2ND_TEMP2_CSF[:-4] + '_ED.mnc'
	runsh("minccalc -byte -expr 'if(A[0]>0 && A[0]<1.2){out=1}else{out=0}' {} {}".format(CLS_2ND_TEMP2, CLS_2ND_TEMP2_CSF) )
	runsh("mincmorph -successive ED {} {}".format(CLS_2ND_TEMP2_CSF, CLS_2ND_TEMP2_CSF_ED) )	
	runsh("minccalc -byte -expr 'if(A[0]>0){out=1}else{out=A[1]}' {} {} {}".format(CLS_2ND_TEMP2_CSF_ED, CLS_2ND_TEMP4, CLS_2ND) )



def execute(Stx_Input_T1, files, parameters):
	print('''==================================\nBeginning Phase 4\n==================================''')
	
	global labels
	labels = parameters.labels
	
	runSecondIter(Stx_Input_T1, files, parameters)
	
	###### make laplace grid ########
	CLS_2ND_CSF = TEMP_PATH_2nd + 'CLS_2ND_CSF.mnc'
	CLS_2ND_CSF_SKEL = TEMP_PATH_2nd + 'CLS_2ND_CSF_SKEL.mnc'
	SKULL_MASK = TEMP_PATH_2nd + 'skull_mask.mnc'
	PVE_GM_2ND = TEMP_PATH_2nd + 'pve_gm.mnc'
	runsh("minccalc -byte -expr 'if(A[0]==1){out=1}else{out=0}' {} {}".format(CLS_2ND, CLS_2ND_CSF) )
	runsh("skel {} {}".format(CLS_2ND_CSF, CLS_2ND_CSF_SKEL) )
	runsh("minccalc -byte -expr 'if(A[0]>0){out=1}else{out=0}' {} {}".format(CLS_2ND, SKULL_MASK) )
	runsh("minccalc -byte -expr 'if(A[0]>1.5 && A[0]<2.5){out=1}else{out=0}' {} {}".format(CLS_2ND, PVE_GM_2ND) )
	#runsh("make_asp_grid {} {} {} {} {} {} {} {}".format(files.REFERENCE_MINC, CLS_2ND_CSF_SKEL, SURF_LEFT_MID, SURF_RIGHT_MID, CLS_2ND, WM_2ND, TEMP_FINAL_CALLOSUM, OUT_FIELD ) )
	runsh("make_asp_grid {} {} {} {} {} {} {} {} {} {}".format(files.REFERENCE_MINC, SKULL_MASK, CLS_2ND_CSF_SKEL,  SURF_LEFT_MID, SURF_RIGHT_MID, CLS_2ND, PVE_GM_2ND, CLS_2ND, TEMP_FINAL_CALLOSUM, OUT_FIELD ) )
	

	######
	START_2nd_SURF_LEFT = files.CIVET_SURF_PATH + 'start_2nd_surf_left_81920.obj'
	START_2nd_SURF_RIGHT = files.CIVET_SURF_PATH + 'start_2nd_surf_right_81920.obj'
	OUT_SURF_TEST_LEFT = files.CIVET_SURF_PATH + 'out_left.obj'
	OUT_SURF_TEST_RIGHT = files.CIVET_SURF_PATH + 'out_right.obj'
	
	runsh("cp {} {}".format(SURF_LEFT_GM,START_2nd_SURF_LEFT) )
	runsh("cp {} {}".format(SURF_RIGHT_GM,START_2nd_SURF_RIGHT) )

	runsh("expand_from_white_2nd -left -init {} {} {} {}".format(START_2nd_SURF_LEFT, START_2nd_SURF_LEFT, OUT_SURF_TEST_LEFT, OUT_FIELD) )
	runsh("expand_from_white_2nd -right -init {} {} {} {}".format(START_2nd_SURF_RIGHT, START_2nd_SURF_RIGHT, OUT_SURF_TEST_RIGHT, OUT_FIELD) )

	OUT_SURF_TEST_LEFT = files.CIVET_SURF_PATH + 'out_left_81920.obj'
	OUT_SURF_TEST_RIGHT = files.CIVET_SURF_PATH + 'out_right_81920.obj'

	##### subdivide polygons #####
	
	HR_SURF_LEFT_WM = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_white_surface_left_327680.obj'
	HR_SURF_LEFT_GM = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_left_327680.obj'	

	SURF_RIGHT_GM_FLIP = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_right_81920_flip.obj'
	SURF_RIGHT_WM_FLIP = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_white_surface_right_81920_flip.obj'

	HR_SURF_RIGHT_WM = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_white_surface_right_327680.obj'
	HR_SURF_RIGHT_GM = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_right_327680.obj'
	HR_SURF_RIGHT_WM_FLIP = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_white_surface_right_327680.obj'
	HR_SURF_RIGHT_GM_FLIP = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_right_327680.obj'


	FLIP_XFM = files.CIVET_SURF_PATH + 'flip.xfm'
	runsh("param2xfm -clobber -scales -1 1 1 {}".format(FLIP_XFM) )

	runsh("subdivide_polygons {} {} 327680".format(SURF_LEFT_WM, HR_SURF_LEFT_WM) )
	runsh("subdivide_polygons {} {} 327680".format(OUT_SURF_TEST_LEFT, HR_SURF_LEFT_GM) )

	runsh("transform_objects {} {} {}".format(SURF_RIGHT_WM, FLIP_XFM, SURF_RIGHT_WM_FLIP) )
	runsh("subdivide_polygons {} {} 327680".format(SURF_RIGHT_WM_FLIP, HR_SURF_RIGHT_WM) )
	runsh("transform_objects {} {} {}".format(HR_SURF_RIGHT_WM, FLIP_XFM, HR_SURF_RIGHT_WM) )

	runsh("transform_objects {} {} {}".format(OUT_SURF_TEST_RIGHT, FLIP_XFM, SURF_RIGHT_GM_FLIP) )
	runsh("subdivide_polygons {} {} 327680".format(SURF_RIGHT_GM_FLIP, HR_SURF_RIGHT_GM) )
	runsh("transform_objects {} {} {}".format(HR_SURF_RIGHT_GM, FLIP_XFM, HR_SURF_RIGHT_GM) )

	MID_LEFT = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_left_327680.obj'
	MID_RIGHT = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_right_327680.obj'
	runsh("average_surfaces {} none none 2 {} {}".format(MID_LEFT, HR_SURF_LEFT_WM, HR_SURF_LEFT_GM ) )
	runsh("average_surfaces {} none none 2 {} {}".format(MID_RIGHT, HR_SURF_RIGHT_WM, HR_SURF_RIGHT_GM) )

	FULL_GRAY = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface.obj'
	FULL_WHITE = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_white_surface.obj'
	FULL_MID = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface.obj'

	runsh("objconcat {} {} none none {} none".format(MID_LEFT, MID_RIGHT, FULL_MID) )
	runsh("objconcat {} {} none none {} none".format(HR_SURF_LEFT_WM, HR_SURF_RIGHT_WM, FULL_WHITE) )
	runsh("objconcat {} {} none none {} none".format(HR_SURF_LEFT_GM, HR_SURF_RIGHT_GM, FULL_GRAY) )
##########  STOP GM Laplacian correction #########
	LOG_PATH = CIVET_WORKING_PATH + 'logs/'
	LOG_GRAY_SURF_LEFT_HIRES = LOG_PATH + Stx_Input_T1 + '.gray_surface_left_hires.log'
	LOG_GRAY_SURF_LEFT_HIRES_FIN = LOG_PATH + Stx_Input_T1 + '.gray_surface_left_hires.finished'
	LOG_GRAY_SURF_RIGHT_HIRES = LOG_PATH + Stx_Input_T1 + '.gray_surface_right_hires.log'
	LOG_GRAY_SURF_RIGHT_HIRES_FIN = LOG_PATH + Stx_Input_T1 + '.gray_surface_right_hires.finished'
	LOG_MID_SURF_LEFT = LOG_PATH + Stx_Input_T1 + '.mid_surface_left.log'
	LOG_MID_SURF_LEFT_FIN = LOG_PATH + Stx_Input_T1 + '.mid_surface_left.finished'
	LOG_MID_SURF_RIGHT =LOG_PATH + Stx_Input_T1 + '.mid_surface_right.log'
	LOG_MID_SURF_RIGHT_FIN = LOG_PATH + Stx_Input_T1 + '.mid_surface_right.finished'
	LOG_MID_FULL = LOG_PATH + Stx_Input_T1 + '.mid_surface_full.log'
	LOG_MID_FULL_FIN = LOG_PATH + Stx_Input_T1 + '.mid_surface_full.finished'
	LOG_WHITE_FULL = LOG_PATH + Stx_Input_T1 + '.white_surface_full.log'
	LOG_WHITE_FULL_FIN = LOG_PATH + Stx_Input_T1 + '.white_surface_full.finished'
	LOG_GRAY_FULL  = LOG_PATH + Stx_Input_T1 + '.gray_surface_full.log'
	LOG_GRAY_FULL_FIN  = LOG_PATH + Stx_Input_T1 + '.gray_surface_full.finished'

	UNC_EMPTY_LOG_FILE = TEMPORAL_TIP_MASK_PATH + 'UNC_empty_logfile.log'
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_LEFT_HIRES) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_LEFT_HIRES_FIN) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_RIGHT_HIRES) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_GRAY_SURF_RIGHT_HIRES_FIN) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_LEFT) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_LEFT_FIN) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_RIGHT) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_MID_SURF_RIGHT_FIN) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_MID_FULL) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_MID_FULL_FIN) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_WHITE_FULL) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_WHITE_FULL_FIN) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_GRAY_FULL) )
	runsh("cp {} {}".format(UNC_EMPTY_LOG_FILE,LOG_GRAY_FULL_FIN) )		

	######## Resuming civet pipeline --> surface registration  ########### 
	runsh("{}CIVET_Processing_Pipeline -input_is_stx -surfreg-model mmuMonkey -prefix {} -sourcedir ./ -targetdir ./ -N3-distance 200 -template 0.50 -lsq12 -resample-surfaces -thickness tlaplace:tfs:tlink 30:20 -VBM -combine-surface -animal -lobe_atlas icbm152nl-2009a -hi-res-surfaces -no-calibrate-white -reset-after cls_volumes -spawn -run {} > {}".format(CIVET_SCRIPT_PATH, prefix, Stx_Input_T1, Stx_Input_T1+'_log'))
