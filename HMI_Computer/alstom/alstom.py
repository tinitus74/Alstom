# USAGE : please add the 2 following lines below to your sikuli script 
# if not 'd:\Tools\alstom' in sys.path:sys.path.append('d:\Tools\alstom')
# import alstom
# --------------------- Enjoy !

import time
import os
from sikuli import *

class ControlHMI:
	"""Sikuli operations for Validation Level 1
	   The goal is to operate like human beeing and
	   validate image on HMI corresponds to what
	   we are waiting for
	"""
	#---------------------------------------------------------------------------------
	# V0.0.3 24 Oct 2017 - add Tag check function
	# v0.0.2 19 Oct 2017 - check if imagePath exists
	# v0.0.1 Oct. 2017   - first delivery POC - mutualize graphic control functions
	#---------------------------------------------------------------------------------
	def __init__(self, imagePath, graphicFunctionsCLass, ReportClass ):
		# Warning : please imagePath is the path where images are stored
		self.imagePath = imagePath
		self.GF = graphicFunctionsCLass # Grphic Functions
		self.report = ReportClass		# HTML Report
		print "ControlHMI started v0.0.1 11/10/2017 (dd/mm/yyyy)"
		if os.path.isdir(imagePath):
			print ("image path exists")
		else:print (" alstom.ControlHMI = error : image path does not exist: " + imagePath )
	
	def controlEscalator(self, objectRegion):
		"""This function to control an Escalator 
			Forward on 
			Forward OFF
			Reverse on
			Reverse Of
			 """
		
		for x in range(1,5):
			click(objectRegion)	# Click on Escalator
			wait(1)	
			if x ==1:
				# ECP_Forward On
				click(Region(1053,491,146,27))
				imgMyImage = self.imagePath + '\\ECP_FON.png'
			elif x ==2:
				# ECP_Forward Off
				click(Region(1053,524,146,27))	
				imgMyImage = self.imagePath + '\\ECP_OFF.png'
			elif x ==3:
				# ECP_Reverse On
				click(Region(1053,557,146,27))
				imgMyImage = self.imagePath + '\\ECP_ROn.png'
			elif x ==4:
				# ECP_Reverse Off
				click(Region(1053,590,146,27))
				imgMyImage = self.imagePath + '\\ECP_OFF.png'

			# Click Exectue and Close then check image
			click(Region(1078,665,101,27))  # Execute
			click(Region(1198,841,99,27))	# Close
			#wait(1)
			if x==2 or x== 4:
				self.GF.findImageInRegionAndReport(objectRegion, imgMyImage,1,self.report)
			else:
				self.GF.findImageInRegionAndReport(objectRegion, imgMyImage,1,self.report)
		
		# Check Tag
		click(objectRegion)	# Click on Escalator
		wait(1)
		reg = Region(1055,620,146,27)
		self.tagTest(reg)
		click(Region(1198,841,99,27))	# Close
	
	def tagTest(self, tagRegion):
		"""This function to create a tag, verify tag is present, delete tag
		   input TagRegion is the region of the Tag Button for the equipment"""
		
		#TagZONE			268	485		674	92
		#TagCheck1		278	495		13	13
		#TagCheck2		278	526		13	13
		#TagCheck3		278	557		13	13
		#NameTextBox		419	309		175	25
		#NotesTextBox	419	349		519	40
		#TypeListBox		419	401		276	20
		#TagBtn			617	604		81	26
		#ReleaseTagBtn	738	604		81	26
		#CloseBtn		865	604		81	26"""

		# TAG control system
		# 0/ Test Initial condition: Not Tagged
		# 1/ Enter a tag
		# 2/ Control tag is present
		# 3/ Delete TAG
		# 4/ Test Final condition: Not TAGGED 

		# Step 1 ----------------------------- Enter TAG 

		# Test initial condition NOT TAGGED
		if str.replace(Region(Region(758,579,178,25)).text(),' ','')=='Nottagged':
			print 'OK = Initial condition : Tag is not tagged'
		else:
			print 'NOK = Initial condition : Tag is already Tagged'
			

		# click Device Tag button
		reg=(Region(1055,593,144,26))
		click(reg)

		#click Execute button
		reg=(Region(1077,649,101,26))
		click(reg)

		#Enter Text on Name Textbox
		click(Region(419,309,175,25))
		type('Tag Name Test')
		type(Key.ENTER)

		#enter Text on Notes Textbox
		click(Region(419,349,519,40))
		type('Tag Note Test')
		type(Key.ENTER)

		#click Tag
		click(Region(617,604,81,26))

		#click Close
		click(Region(865,604,81,26))


		# Step 2 -  Control TAG is here
		# click Device Tag button
		reg=(Region(1055,593,144,26))
		click(reg)

		#click Execute button
		reg=(Region(1077,649,101,26))
		click(reg)

		# Step 2  ----------------------  CONTROL TAG IS Present
		wait(1)
		if str.replace(Region(520,484,214,31).text(),' ','')=='TagNoteTest':
			print 'OK = Tag is tagged'
		else:
			print 'NOK = Tag not found'
		#click Close
		click(Region(865,604,81,26))


		# Step 3  ----------------------  Delete TAG
		# click Device Tag button
		reg=(Region(1055,593,144,26))
		click(reg)

		#click Execute button
		reg=(Region(1077,649,101,26))
		click(reg)

		wait(1)
		#doucleclick on first checkbox
		reg=(Region(278,495,13,13))
		doubleClick(reg)
		wait(1)

		#click ReleaseTag Button
		reg=(Region(738,604,81,26))
		doubleClick(reg)


		# Step 4  ----------------------  Check Final condition = Not tagged
		wait(3)
		if str.replace(Region(Region(758,579,178,25)).text(),' ','')=='Nottagged':
			print 'OK = after tag release Tag is not tagged'
		else:
			print 'NOK = after tag release Tag is still Tagged'




	
	def controlLift(self, objectRegion):
		"""This function to control a lift with these oprations
			Start
			- click on the object then a window appear
			- clic on Start button
			- click on Execute button
			- click on Close button
			- verify the image liftOFF.png

			Stop
			- click on the object then a window appear
			- clic on Stop button
			- click on Confirm button
			- click on Execute button
			- click on Close button
			- verify the image liftOFF.png
			 """
		
		for x in range(1,3):
			click(objectRegion)	# Click on LIFT 
			wait(1)
 
			# Click on Start ----- 1 = Start / 2 = Stop
			self.report.addLine('Test LIFT Start' + str(x))
			if x == 1:
				click(Region(1056,511,146,27))
			else:
				click(Region(1056,552,146,27))
				click(Region(1220,389,79,24)) # Click on Confirm	
			wait(1)

			# Click on Execute 
			click(Region(1077,651,102,27))
			wait(1)

			# Click on Close 
			click(Region(1198,841,99,27))
			wait(1)
			if x==1:
				self.report.addLine('Test LIFT Start')
				self.GF.findImageInRegionAndReport(objectRegion, self.imagePath + '\\LiftStart.png',1,self.report)
			else:
				self.report.addLine('Test LIFT Stop')
				self.GF.findImageInRegionAndReport(objectRegion, self.imagePath + '\\LiftStop.png',1,self.report)
		
		# check Tag
		click(objectRegion)	# Click on Escalator
		wait(1)
		reg = Region(1055,593,146,27)
		self.tagTest(reg)
		# Click on Close 
		click(Region(1198,841,99,27))

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
	# v0.0.4 19-10-2017 check if pathReport exists
	# v0.0.3 11-10-2017 added date to time in the first line of the rapport
	# v0.0.2 10-10-2017 bug corrections
	# v0.0.1 October 2017 - first delivery POC
	#----------------------------------------------------------------------
	
    def __init__(self, pathReport):
		# define some things to do at the init
		# WARNING : please use / to declare pathReport instead of \
		print "HTMLReport class started v0.0.3 10/10/2017"
		if os.path.isdir(pathReport):
			print ("image path exists")
		else:print ("error : image path does not exist: " + pathReport )

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