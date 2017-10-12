# USAGE : please add the 2 following lines below to your sikuli script 
# if not 'd:\Tools\alstom' in sys.path:sys.path.append('d:\Tools\alstom')
# import alstom
# --------------------- Enjoy !

import time
from sikuli import *

class ControlHMI:
	"""Sikuli operations for Validation Level 1
	   The goal is to operate like human beeing and
	   validate the image on HMI corresponds to what
	   we are waiting for
	
	"""
	def __init__(self, imagePath, graphicFunctionsCLass, ReportClass ):
		# Warning : please imagePath is the path where images are stored
		self.imagePath = imagePath
		self.GF = graphicFunctionsCLass # Grphic Functions
		self.report = ReportClass		# HTML Report
		print "ControlHMI started v0.0.1 11/10/2017 (dd/mm/yyyy)"
	
	def controlLift(self, objectRegion):
		"""This function to control a lift with these oprations
			Start
			- click on the object then a window appear
			- clic on Start button
			- click on Execute button
			- click on Close button
			- verify the image leftOn.png

			Stop
			- click on the object then a window appear
			- clic on Stop button
			- click on Confirm button
			- click on Execute button
			- click on Close button
			- verify the image leftOn.png
			 """
		
		for x in range(1,3):
			click(objectRegion)	# Click on LIFT 
			wait(1)
 
			# Click on Start ----- 1 = Start / 2 = Stop
			self.report.addLine('Test LIFT Start' + str(x))
			if x == 1:
				click(Region(1056,511,146,27))
			else:
				click(Region(1056,533,146,27))
				click(Region(1201,386,79,24)) # Click on Confirm	
			wait(1)

			# Click on Execute 
			click(Region(1077,651,102,27))
			wait(1)

			# Click on Close 
			click(Region(1198,841,99,27))
			wait(1)
			if x==1:
				self.report.addLine('Test LIFT Start')
				self.GF.findImageInRegionAndReport(objectRegion, 'c:\\pastisDrive\\HMI\\LiftStart.png',1,self.report)
			else:
				self.report.addLine('Test LIFT Stop')
				self.GF.findImageInRegionAndReport(objectRegion, 'c:\\pastisDrive\\HMI\\LiftStop.png',1,self.report)

class GraphicFunctions:
	"""Graphic Functions to do some operations using Sikuli"""
	#----------------------------------------------------------------------
	# v0.0.1 October 2017 - first delivery POC - mutualize graphic functions
	#----------------------------------------------------------------------
	
	def __init__(self):
		# define some things to do at the init
		print "GF started v0.0.01 10/10/2017"
		
	def findImageInRegion(self, region, imagePath, imageSimilarity):
		""" This function to find an image in a region
			input : region, 
					imagePath to find 
					similarity (todo)      
			return 
				True if the image is found in the region
				False in other case
		"""
		try:
			match = region.find(imagePath)
			return True
		except:
			return False

	def findImageInRegionAndReport(self, region, imagePath, imageSimilarity, report):
		""" This function to find an image in a region
			input : region, 
					imagePath to find 
					similarity (todo)     
					report is a class report from alstom.py module
			return 
				True if the image is found in the region and add a line in HTML Report image found
				False in other case and ad a line in the HTML Report Error Image not found
				
		
		"""	
		try:
			match = region.find(imagePath)
			report.addLine(" - Image found " + imagePath )
			return True
		except:
			report.addLine("<font color=red> - ERROR ! Image not found " + imagePath  + " on region " + str(region) + "</font>")
			return False

			

class HTMLReport:
    """HTML Report Generator Class """
	#----------------------------------------------------------------------
	# v0.0.3 11-10-2017 added date to time in the first line of the rapport
	# v0.0.2 10-10-2017 bug corrections
	# v0.0.1 October 2017 - first delivery POC
	#----------------------------------------------------------------------
	
    def __init__(self, pathReport):
		# define some things to do at the init
		# WARNING : please use / to declare pathReport instead of \
		print "HTMLReport class started v0.0.3 10/10/2017"
		self.html_str = "<hr>"
		self.html_str = self.html_str + "<b>Automagically test tarting at </b>" + time.strftime('%d-%m-%Y %H:%M:%S')
		self.html_str = self.html_str + "<hr>"
		self.pathReport = pathReport
		
    def addLine(self, stringToAdd):
        try:
			self.html_str = self.html_str + time.strftime('%H:%M:%S') + ' - '  + stringToAdd + "<br>"
        except:
			self.html_str = self.html_str + time.strftime('%H:%M:%S') + " error trying addLine"  

    def writeReport(self):
        print "writeReport OK"
        self.html_file = open(self.pathReport,'w+')
        self.html_file.write (self.html_str)
        self.html_file.close()