######################################################################################################### 
### Phase 4
### Expands the gray matter to the CSF boundary to improve results
######################################################################################################### 
from helpers import runsh

##### 2nd iteration	for GM surface from GM surface
def runSecondIter(Stx_Input_T1, files, parameters):

	TEMPORAL_TIP_MASK_PATH = parameters.filepaths.Temporal_Masks_Path
	TEMPORAL_TIP_MASK = TEMPORAL_TIP_MASK_PATH + "/" + parameters.masks.Temporal_Tip_Mask
	MID_LINE_MASK = TEMPORAL_TIP_MASK_PATH + "/" + parameters.masks.Midline_Mask
	
	files.setFileName("SURF_LEFT_GM", files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_left_81920.obj')
	files.setFileName("SURF_RIGHT_GM", files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_right_81920.obj')
	
	SURF_LEFT_GM_1st = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_left_1st_81920.obj'	
	SURF_RIGHT_GM_1st = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_right_1st_81920.obj'
	runsh("cp {} {}".format(files.SURF_LEFT_GM, SURF_LEFT_GM_1st) )
	runsh("cp {} {}".format(files.SURF_RIGHT_GM, SURF_RIGHT_GM_1st) )
	
	files.setFileName("SURF_LEFT_MID", files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_left_81920.obj')
	files.setFileName("SURF_RIGHT_MID", files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_right_81920.obj')
	
	TEMP_FINAL_CLASSIFY = files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_final_classify.mnc'
	TEMP_SUB_MASK = files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_subcortical_mask.mnc'
	files.setFileName("TEMP_FINAL_CALLOSUM", files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_final_callosum.mnc')
	TEMP_CSF_SKEL = files.CIVET_TEMP_PATH + 'stx_' + Stx_Input_T1 + '_csf_skel.mnc'
	files.setFileName("TEMP_PATH_2nd", files.CIVET_TEMP_PATH + '2nd/')
	runsh("mkdir {}".format(files.TEMP_PATH_2nd) )
	
	ORIG_CSF = files.TEMP_PATH_2nd + 'orig_csf.mnc'
	files.setFileName("OUT_FIELD", files.TEMP_PATH_2nd + 'Out_Field.mnc')
	files.setFileName("CLS_2ND", files.TEMP_PATH_2nd + 'CLS_2ND.mnc')
	
	ORIG_WM = files.TEMP_PATH_2nd + 'orig_wm.mnc'
	ORIG_WM_DILATION5 = files.TEMP_PATH_2nd + 'orig_wm_dil5.mnc'	
	ORIG_GM = files.TEMP_PATH_2nd + 'orig_gm.mnc'
	ORIG_GM_DILATION3_EROSION3 = files.TEMP_PATH_2nd + 'orig_gm_dil3_ero3.mnc'
	
	SPHERE = files.TEMP_PATH_2nd + 'sphere.obj'
	runsh("create_tetra {} 0 -20 10 70 100 80 20480".format(SPHERE) )
	
	R_TRAN = files.TEMP_PATH_2nd + 'x25_R.xfm'
	L_TRAN = files.TEMP_PATH_2nd + 'x25_L.xfm'
	TEMP_GM_LEFT = files.TEMP_PATH_2nd + 'gm_left.mnc'
	TEMP_GM_RIGHT = files.TEMP_PATH_2nd + 'gm_right.mnc'
	CENTER_GM_LEFT = files.TEMP_PATH_2nd + 'centered_gm_left.mnc'
	CENTER_GM_RIGHT = files.TEMP_PATH_2nd + 'centered_gm_right.mnc'
	
	runsh("param2xfm -translation -25 0 0 {}".format(R_TRAN) )
	runsh("param2xfm -translation 25 0 0 {}".format(L_TRAN) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, SURF_LEFT_GM_1st, TEMP_GM_LEFT) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, SURF_RIGHT_GM_1st, TEMP_GM_RIGHT) )

	runsh("mincresample -nearest -like {} {} {} -transform {}".format(files.REFERENCE_MINC, TEMP_GM_LEFT, CENTER_GM_LEFT, L_TRAN) )
	runsh("mincresample -nearest -like {} {} {} -transform {}".format(files.REFERENCE_MINC, TEMP_GM_RIGHT, CENTER_GM_RIGHT, R_TRAN) )

	LEFT_HULL_CENTER =  files.TEMP_PATH_2nd + 'Hull_left_centered.obj'
	RIGHT_HULL_CENTER =  files.TEMP_PATH_2nd + 'Hull_right_centered.obj'
	runsh("deform_surface {} none 0 0 0 {} {} none 10 1 -1 0.5 {} -0.8 0.8 0.1 0.1 100 0 1 1 3 0 0 0 1000 0.1 0.0".format(CENTER_GM_LEFT, SPHERE, LEFT_HULL_CENTER, SURF_LEFT_GM_1st) )
	runsh("deform_surface {} none 0 0 0 {} {} none 10 1 -1 0.5 {} -0.8 0.8 0.1 0.1 100 0 1 1 3 0 0 0 1000 0.1 0.0".format(CENTER_GM_RIGHT, SPHERE, RIGHT_HULL_CENTER, SURF_RIGHT_GM_1st) )

	LEFT_HULL =  files.TEMP_PATH_2nd + 'Hull_left.obj'
	RIGHT_HULL =  files.TEMP_PATH_2nd + 'Hull_right.obj'
	LEFT_HULL_MINC =  files.TEMP_PATH_2nd + 'Hull_left.mnc'
	RIGHT_HULL_MINC =  files.TEMP_PATH_2nd + 'Hull_right.mnc'
	runsh("transform_objects {} {} {}".format(LEFT_HULL_CENTER, R_TRAN, LEFT_HULL) )
	runsh("transform_objects {} {} {}".format(RIGHT_HULL_CENTER, L_TRAN, RIGHT_HULL) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, LEFT_HULL, LEFT_HULL_MINC) )
	runsh("scan_object_to_volume {} {} {}".format(files.REFERENCE_MINC, RIGHT_HULL, RIGHT_HULL_MINC) )

	LEFT_HULL_MINC_DILATION =  LEFT_HULL_MINC[:-4] + '_dil.mnc'
	RIGHT_HULL_MINC_DILATION =  RIGHT_HULL_MINC[:-4] + '_dil.mnc'
	runsh("mincmorph -dilation {} {}".format(LEFT_HULL_MINC, LEFT_HULL_MINC_DILATION) )
	runsh("mincmorph -dilation {} {}".format(RIGHT_HULL_MINC, RIGHT_HULL_MINC_DILATION) )
####
	WMGM = files.TEMP_PATH_2nd + 'wmgm.mnc'
	WMGM_DDDEEE = WMGM[:-4] + '_DDDEEE.mnc'
	WMGM_DDDEEEEEEEE = WMGM[:-4] + '_DDDEEEEEEEE.mnc'
	THIN_MASK = files.TEMP_PATH_2nd + 'thin_mask.mnc'
	runsh("minccalc -expr 'if(A[0]>{gm}){{out=1}}else{{out=0}}' {} {}".format(
		  TEMP_FINAL_CLASSIFY, WMGM, gm=labels.GM - 0.2 ) ) 
	runsh("mincmorph -successive DDDEEE {} {}".format(WMGM, WMGM_DDDEEE) )	
	runsh("mincmorph -successive DDDEEEEEEEE {} {}".format(WMGM, WMGM_DDDEEEEEEEE) ) 
	runsh("minccalc -byte -expr 'out=A[0]-A[1]' {} {} {}".format(WMGM_DDDEEE, WMGM_DDDEEEEEEEE, THIN_MASK) )
###
	DEEP = files.TEMP_PATH_2nd + 'deep.mnc'
	runsh("minccalc -byte -expr 'if( (A[0]==0 && A[1]>0) || (A[2]==0 && A[3]>0) ){{out=1}}else{{out=0}}' {} {} {} {} {}".format(LEFT_HULL_MINC_DILATION, TEMP_GM_LEFT, RIGHT_HULL_MINC_DILATION, TEMP_GM_RIGHT, DEEP ) )
	DEEP_DEFRAG = DEEP[:-4] + '_defrag.mnc'
	runsh("mincdefrag {} {} 1 27 10".format(DEEP, DEEP_DEFRAG) )

	files.CLS_2ND_TEMP = files.TEMP_PATH_2nd + 'CSL_2ND_temp.mnc'
	files.CLS_2ND_TEMP2 = files.TEMP_PATH_2nd + 'CSL_2ND_temp2.mnc'
	files.CLS_2ND_TEMP3 = files.TEMP_PATH_2nd + 'CSL_2ND_temp3.mnc'
	files.CLS_2ND_TEMP4 = files.TEMP_PATH_2nd + 'CSL_2ND_temp4.mnc'
	runsh("minccalc -byte -expr 'if(A[0]>{wm_low} && A[0]<{wm_high}){{out=3}}else if(A[0]>{gm_low} && A[0]<{gm_high}){{out=1}}else if(A[0]>{csf} && A[0]< {gp}){{out=3}}else if(A[1]>0 && A[2]==1){{out=1}}else{{out=A[3]}}' {} {} {} {} {}".format(
		   TEMP_SUB_MASK, DEEP_DEFRAG, TEMP_FINAL_CLASSIFY, files.RSL_ABC_SEG2,  files.CLS_2ND_TEMP,
		   wm_low  = labels.WM-0.4,
		   wm_high = labels.WM+0.4,
		   gm_low  = labels.GM-0.4,
		   gm_high = labels.GM+0.4,
		   csf     = labels.CSF-0.4,
		   gp      = labels.GP+0.4
		   ) )
	runsh("minccalc -byte -expr 'if(A[0]>0 && A[1]>0){{out=2}}else{{out=A[2]}}' {} {} {} {}".format(THIN_MASK, TEMP_CSF_SKEL, files.CLS_2ND_TEMP, files.CLS_2ND_TEMP2) )
	
	WM_2ND_LEFT = files.TEMP_PATH_2nd + 'wm_2nd_mask_left.mnc'
	WM_2ND_RIGHT = files.TEMP_PATH_2nd + 'wm_2nd_mask_right.mnc'
	WM_2ND_LEFT_DD = files.TEMP_PATH_2nd + 'wm_2nd_mask_left_DD.mnc'
	WM_2ND_RIGHT_DD = files.TEMP_PATH_2nd + 'wm_2nd_mask_right_DD.mnc'
	WM_2ND =  files.TEMP_PATH_2nd + 'WM.mnc'
	WM_2ND_DD =  files.TEMP_PATH_2nd + 'WM_DD.mnc'
	runsh("surface_mask2 -binary_mask {} {} {}".format(files.CLS_2ND_TEMP2, files.SURF_LEFT_MID, WM_2ND_LEFT) )
	runsh("surface_mask2 -binary_mask {} {} {}".format(files.CLS_2ND_TEMP2, files.SURF_RIGHT_MID, WM_2ND_RIGHT) )
	runsh("mincmorph -successive DD {} {}".format(WM_2ND_LEFT, WM_2ND_LEFT_DD) )
	runsh("mincmorph -successive DD {} {}".format(WM_2ND_RIGHT, WM_2ND_RIGHT_DD) )
	runsh("minccalc -byte -expr 'if(A[0]>0 || A[1]>0){{out=1}}else{{out=0}}' {} {} {}".format(WM_2ND_LEFT, WM_2ND_RIGHT, WM_2ND) )
	runsh("minccalc -byte -expr 'if(A[0]>0 || A[1]>0){{out=1}}else{{out=0}}' {} {} {}".format(WM_2ND_LEFT_DD, WM_2ND_RIGHT_DD, WM_2ND_DD) )
	
	runsh("minccalc -byte -expr 'if(A[0]>0){{out=3}}else if(A[1]>0 && A[2]==1){{out=1}}else if(A[2]==2){{out=2}}else if(A[3]>0){{out=2}}else{{out=A[2]}}' {} {} {} {} {}".format(WM_2ND, WM_2ND_DD, files.CLS_2ND_TEMP2,WMGM_DDDEEE, files.CLS_2ND_TEMP3) )  

	runsh("minccalc -byte -expr 'if(A[0]>0 && A[1]==1){{out=1}}else{{out=A[2]}}' {} {} {} {}".format(MID_LINE_MASK, files.CLS_2ND_TEMP2, files.CLS_2ND_TEMP3, files.CLS_2ND_TEMP4) )
	files.CLS_2ND_TEMP2_CSF = files.CLS_2ND_TEMP2[:-4] + '_CSF.mnc'
	files.CLS_2ND_TEMP2_CSF_ED = files.CLS_2ND_TEMP2_CSF[:-4] + '_ED.mnc'
	runsh("minccalc -byte -expr 'if(A[0]>0 && A[0]<1.2){{out=1}}else{{out=0}}' {} {}".format(files.CLS_2ND_TEMP2, files.CLS_2ND_TEMP2_CSF) )
	runsh("mincmorph -successive ED {} {}".format(files.CLS_2ND_TEMP2_CSF, files.CLS_2ND_TEMP2_CSF_ED) )	
	runsh("minccalc -byte -expr 'if(A[0]>0){{out=1}}else{{out=A[1]}}' {} {} {}".format(files.CLS_2ND_TEMP2_CSF_ED, files.CLS_2ND_TEMP4, files.CLS_2ND) )
	print(MID_LINE_MASK)


def laplacianCorrection(Stx_Input_T1, files):
###### make laplace grid ########
	files.CLS_2ND_CSF = files.TEMP_PATH_2nd + 'files.CLS_2ND_CSF.mnc'
	files.CLS_2ND_CSF_SKEL = files.TEMP_PATH_2nd + 'files.CLS_2ND_CSF_SKEL.mnc'
	SKULL_MASK = files.TEMP_PATH_2nd + 'skull_mask.mnc'
	PVE_GM_2ND = files.TEMP_PATH_2nd + 'pve_gm.mnc'
	runsh("minccalc -byte -expr 'if(A[0]==1){{out=1}}else{{out=0}}' {} {}".format(files.CLS_2ND, files.CLS_2ND_CSF) )
	runsh("skel {} {}".format(files.CLS_2ND_CSF, files.CLS_2ND_CSF_SKEL) )
	runsh("minccalc -byte -expr 'if(A[0]>0){{out=1}}else{{out=0}}' {} {}".format(files.CLS_2ND, SKULL_MASK) )
	runsh("minccalc -byte -expr 'if(A[0]>1.5 && A[0]<2.5){{out=1}}else{{out=0}}' {} {}".format(files.CLS_2ND, PVE_GM_2ND) )
	runsh("make_asp_grid {} {} {} {} {} {} {} {} {} {}".format(files.REFERENCE_MINC, SKULL_MASK, files.CLS_2ND_CSF_SKEL,  files.SURF_LEFT_MID, files.SURF_RIGHT_MID, files.CLS_2ND, PVE_GM_2ND, files.CLS_2ND, files.TEMP_FINAL_CALLOSUM, files.OUT_FIELD ) )
	

	######
	START_2nd_SURF_LEFT = files.CIVET_SURF_PATH + 'start_2nd_surf_left_81920.obj'
	START_2nd_SURF_RIGHT = files.CIVET_SURF_PATH + 'start_2nd_surf_right_81920.obj'
	OUT_SURF_TEST_LEFT = files.CIVET_SURF_PATH + 'out_left.obj'
	OUT_SURF_TEST_RIGHT = files.CIVET_SURF_PATH + 'out_right.obj'
	
	runsh("cp {} {}".format(files.SURF_LEFT_GM,START_2nd_SURF_LEFT) )
	runsh("cp {} {}".format(files.SURF_RIGHT_GM,START_2nd_SURF_RIGHT) )

	runsh("expand_from_white_2nd -left -init {} {} {} {}".format(START_2nd_SURF_LEFT, START_2nd_SURF_LEFT, OUT_SURF_TEST_LEFT, files.OUT_FIELD) )
	runsh("expand_from_white_2nd -right -init {} {} {} {}".format(START_2nd_SURF_RIGHT, START_2nd_SURF_RIGHT, OUT_SURF_TEST_RIGHT, files.OUT_FIELD) )

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

	runsh("subdivide_polygons {} {} 327680".format(files.SURF_LEFT_WM, HR_SURF_LEFT_WM) )
	runsh("subdivide_polygons {} {} 327680".format(OUT_SURF_TEST_LEFT, HR_SURF_LEFT_GM) )

	runsh("transform_objects {} {} {}".format(files.SURF_RIGHT_WM, FLIP_XFM, SURF_RIGHT_WM_FLIP) )
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

def clearLogFiles(Stx_Input_T1, files):
	LOG_PATH = files.CIVET_WORKING_PATH + 'logs/'
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

	UNC_EMPTY_LOG_FILE = parameters.filepaths.Temporal_Masks_Path + 'UNC_empty_logfile.log'
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

def transformBack(Stx_Input_T1, files):
	######## Transform back to original space ###########

	TAL_XFM_INVERT = files.TAL_XFM[:-4] + '_invert.xfm'
	runsh("xfminvert %s %s" %(files.TAL_XFM, TAL_XFM_INVERT) )
	
	MID_LEFT_RSL = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_rsl_left_327680.obj'
	HR_SURF_LEFT_WM_RSL = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_white_surface_rsl_left_327680.obj'
	HR_SURF_LEFT_GM_RSL = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_rsl_left_327680.obj'
	MID_RIGHT_RSL = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_mid_surface_rsl_right_327680.obj'
	HR_SURF_RIGHT_WM_RSL = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_white_surface_rsl_right_327680.obj'
	HR_SURF_RIGHT_GM_RSL = files.CIVET_SURF_PATH + 'stx_' + Stx_Input_T1 + '_gray_surface_rsl_right_327680.obj'

	MID_LEFT_RSL_NATIVE = MID_LEFT_RSL[:-4] + '_native.obj'
	HR_SURF_LEFT_WM_RSL_NATIVE = HR_SURF_LEFT_WM_RSL[:-4] + '_native.obj'
	HR_SURF_LEFT_GM_RSL_NATIVE = HR_SURF_LEFT_GM_RSL[:-4] + '_native.obj'
	MID_RIGHT_RSL_NATIVE = MID_RIGHT_RSL[:-4] + '_native.obj'
	HR_SURF_RIGHT_WM_RSL_NATIVE = HR_SURF_RIGHT_WM_RSL[:-4] + '_native.obj'
	HR_SURF_RIGHT_GM_RSL_NATIVE = HR_SURF_RIGHT_GM_RSL[:-4] + '_native.obj'

	runsh("transform_objects %s %s %s" %(MID_LEFT_RSL ,TAL_XFM_INVERT, MID_LEFT_RSL_NATIVE) )
	runsh("transform_objects %s %s %s" %(HR_SURF_LEFT_WM_RSL ,TAL_XFM_INVERT, HR_SURF_LEFT_WM_RSL_NATIVE) )
	runsh("transform_objects %s %s %s" %(HR_SURF_LEFT_GM_RSL ,TAL_XFM_INVERT, HR_SURF_LEFT_GM_RSL_NATIVE) )
	runsh("transform_objects %s %s %s" %(MID_RIGHT_RSL ,TAL_XFM_INVERT, MID_RIGHT_RSL_NATIVE) )
	runsh("transform_objects %s %s %s" %(HR_SURF_RIGHT_WM_RSL ,TAL_XFM_INVERT, HR_SURF_RIGHT_WM_RSL_NATIVE) )
	runsh("transform_objects %s %s %s" %(HR_SURF_RIGHT_GM_RSL ,TAL_XFM_INVERT, HR_SURF_RIGHT_GM_RSL_NATIVE) )



def execute(Stx_Input_T1, files, parameters):
	print('''==================================\nBeginning Phase 4\n==================================''')
	
	global labels
	labels = parameters.labels

	runSecondIter(Stx_Input_T1, files, parameters)
	laplacianCorrection(Stx_Input_T1,files)

	######## Resuming civet pipeline --> surface registration  ########### 
	runsh("{civet_params} -VBM -combine-surface -animal -lobe_atlas icbm152nl-2009a -hi-res-surfaces -no-calibrate-white -reset-after cls_volumes -spawn -run {input_file} > {log_file}".format(civet_params=parameters.civet, input_file=Stx_Input_T1, log_file=Stx_Input_T1+'_log'))

	transformBack(Stx_Input_T1, files)
	