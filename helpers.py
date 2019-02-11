import os, json
from subprocess import run

'''
Wrapper for the run function in the subprocess module
Will run the input string command as is in the shell
@Input: String to execute
'''

def runsh(exec_str, **kwargs):
	run(exec_str, **kwargs, shell=True)

class Labels(object):
	"""
	Stores label values for common brain regions as defined by the configuration file
	IMPORTANT: The names of the variables will reflect those read from the configuration file
	If a label is not declared below but is present in the config file, 
	it will be dynamically added to this class with the same name as that in the config file 
	"""
	def __init__(self, labels_dict):
		self.WM, self.GM, self.CSF = None, None, None
		self.Hippo_L, self.Hippo_R = None, None
		self.setLabels(labels_dict)
	
	#### If the label names change, update here ####
	def setLabels(self, labels):
		for region in labels:
			label = int(labels[region])
			setattr(self,region,label)

class FilePaths(object):
	"""
	Stores path names stored on config file
	"""
	def __init__(self, filepaths):
		for path in filepaths:
			setattr(self,path, os.path.abspath(filepaths[path]))

class Masks(object):
	"""Holds filenames for 	custom masks"""
	def __init__(self, masks):
		for path in masks:
			setattr(self,path, masks[path])

class ConfigParser(object):
	"""This class will read a JSON parameter file and build the necessary strings
	   to be run in the command line.
	   Parameters given as command-line arguments take precedence.
	"""

	# Expected keys in the parameter files - could be changed
	FLAGS = "flags"
	CIVET = "CIVET"
	CIVET_PATH = "CIVET_Path"
	FILEPATHS = "file_paths"
	LABELS = "labels"
	INPUT_DIR = "-sourcedir"
	TARGET_DIR = "-targetdir"
	MASKS = "masks"

	def __init__(self, args):
		
		# Dictionary of the parameters adn their values
		self.config = {}
		# The CIVET command line arguments
		self.civet = {}
		# Paths to various files used by the pipeline
		self.filepaths = None
		# Names for the mask files that will be used in the script
		self.masks = {}

		self.cwd = None
		self.input_dir = None

		configfile = args.paramfile
		with open(configfile,'r') as cf:
			self.config = json.load(cf)

		# Build filepath object
		self.filepaths = FilePaths(self.config[ConfigParser.FILEPATHS])
		
		# Get file names for masks
		self.masks = Masks(self.config[ConfigParser.MASKS])


		# Update if user provided dirs
		if args.outputdir:
			self.cwd = os.path.abspath(args.outputdir)
		elif hasattr(self.filepaths, "outputdir"):
			self.cwd = self.filepaths.outputdir
		else:
		 raise FileNotFoundError("Please provide an output directory either on the command line or the parameter file!")
		

		if args.inputdir:
			self.input_dir = os.path.abspath(args.inputdir)
		elif hasattr(self.filepaths, "inputdir"):
			self.input_dir = self.filepaths.inputdir
		else:
			raise FileNotFoundError("Please provide an input directory either on the command line or the parameter file!")

		# Build labels
		self.labels = Labels(self.config[ConfigParser.LABELS])

		self.buildCivetParams()



	'''Accepts a type of paramter and builds the corresponding string
	'''
	def buildCivetParams(self):
		params = self.config[ConfigParser.CIVET]
		params[ConfigParser.INPUT_DIR] = self.cwd
		params[ConfigParser.TARGET_DIR] = self.cwd

		final_str = ""
		flag_str = ""

		if ConfigParser.FLAGS in params:
			flag_str = " ".join(params[ConfigParser.FLAGS])
			params.pop(ConfigParser.FLAGS, None)

		concat = lambda x,y: "{} {}".format(x, y)
		args = " ".join([concat(p,params[p]) for p in params])

		final_str = "{}/CIVET_Processing_Pipeline {} {}".format(
			self.filepaths.CIVET_Path, flag_str, args)

		self.civet = final_str


class FileNames(object):
	"""List of all the filenames to be used across phases
	"""
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

	def setFileName(self,filename, path):
		setattr(self,filename, path)

	def __str__(self):
		return "Parent Directory: {}".format(self.CIVET_WORKING_PATH)








