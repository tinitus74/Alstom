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
	# v0.0.4 10 Nov 2017 - add Tag Sharing Function
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
		#if os.path.isdir(imagePath): TODO
		#	print ("image path exists")
		#else:print ("--> alstom.ControlHMI = error : image path does not exist: " + imagePath )
	
	def controlEscalator(self, objectRegion, strEquipment):
		"""This function to control an Escalator 
			Forward on 
			Forward OFF
			Reverse on
			Reverse Of
			 """
		self.strEquipment = strEquipment
		for x in range(1,5): #
			click(objectRegion)	# Click on Escalator
			
			wait(1)	
			if x ==1:
				# ECP_Forward On
				click(Region(1053,491,146,27))
				imgMyImage = self.imagePath + '\\escForwardOn.png'
			elif x ==2:
				# ECP_Forward Off
				click(Region(1053,524,146,27))	
				imgMyImage = self.imagePath + '\\escOFF.png'
			elif x ==3:
				# ECP_Reverse On
				click(Region(1053,557,146,27))
				imgMyImage = self.imagePath + '\\escReverseOn.png'
			elif x ==4:
				# ECP_Reverse Off
				click(Region(1053,590,146,27))
				imgMyImage = self.imagePath + '\\escOFF.png'

			# Click Exectue and Close then check image
			click(Region(1078,665,101,27))  # Execute
			click(Region(1198,841,99,27))	# Close
			#wait(1)
			if x==2 or x== 4:
				#self.GF.findImageInRegionAndReport(objectRegion, self.imagePath + '\\LiftStop.png',1,self.report,  "For Stop " + strEquipment)
				self.GF.findImageInRegionAndReport(objectRegion, imgMyImage,1,self.report, "For Stop" + strEquipment)
			else:
				if x==1:
					self.GF.findImageInRegionAndReport(objectRegion, imgMyImage,1,self.report, "For Forward ON " + strEquipment)
				else:
					self.GF.findImageInRegionAndReport(objectRegion, imgMyImage,1,self.report, "For Reverse ON " + strEquipment)

		
		# Check Tag
		click(objectRegion)	# Click on Escalator
		wait(1)
		regBtnTag  = Region(1055,620,146,26) # define "Tagging" button region
		regBtnExectue = Region(1077,662,101,26) # define "Exexute" button region
		regTagStatus  = Region(759, 620, 178,26) # define "Tag Status" region on control panel
		self.tagTest(regBtnTag, regBtnExectue, regTagStatus, "ESC")

		click(Region(1198,841,99,27))	# Close

	def controlCB(self, objectRegion):
		for x in range(1,3):
			click(objectRegion)	# Click on CB
			wait(1)
 
			# Click on Start ----- 1 = OPEN / 2 = CLOSE
			self.report.addLine('Test CB OPEN' + str(x))
			if x == 1:
				click(Region(1135,506,181,26))
			else:
				click(Region(1042,541,181,26))
				click(Region(1200,384,81,26)) # Click on Confirm	
			wait(1)

			# Click on Execute 
			click(Region(1082,626,101,26))
			wait(1)

			# Click on Close 
			click(Region(1042,541,181,26))
			wait(1)
		
		# check Tag
		click(objectRegion)	# Click on CB
		wait(1)
		reg = Region(1055,593,146,27)
		self.tagTest(reg)
		# Click on Close 
		click(Region(1198,841,99,27))

	def tagSharing(self, tagRegion1, tagRegion2, strEquipment):
		""" This function to tag an object and control if the tag is present on a second object
			tagRegion1 is the region of the 1st object to click
			tagRegion is for the 2nd object
			strEquipment indicates wich equipments are used for this function
			working only for type ESC & LIFT
		"""
		# -----------------------------------------------------------
		# Tag an object ESC or LCP
		# select another object ESC or LCP
		# control if second object is tagged with the same mention
		# if yes : tag sharing is positive => this is an error
		# untag the first object ! 
		# -----------------------------------------------------------
		print "Tag Sharing Control initiated..."
		
		for x in range(1,3):
			# click on object
			if x ==1:
				click(tagRegion1)	
			else:
				click(tagRegion2)
			wait(1)

			# find the type
			self.tObject = None 
			strToFind =  str.replace(Region(629, 408, 101, 24).text()," ","")
			if strToFind[:16] =='Escalatorcontrol':
				print 'This is an Escalator'
				self.closeRegion = Region(1198,841,99,27)	# Close
				self.tObject = "ESC"
				self.tagStatus = Region(755,621,186,32)
				self.tagButton = Region(1057,624,146,29) #Region(759,626,83,19)
				self.ExecuteButton = Region(1077,665,100,26)
			elif strToFind[:11] =='Liftcontrol':
				print 'This is a Lift'
				self.closeRegion = Region(1198,841,99,27)   # Close
				self.tObject = "LCP"
				self.tagStatus = Region(754,579,186,32)
				self.tagButton = Region(1055,599,145,23)
				self.ExecuteButton = Region(1077,652,100,26)
			else:
				print "Type of object not detected"
				break
			wait(1)

			# Confirm 1st object is not tagged...
			if x ==1:
				self.typeOfObjectOne = self.tObject
				if str.replace(self.tagStatus.text(),' ','')=='Nottagged':
					blTagOk = True
					print 'OK = Initial condition : first object is not tagged'
					# let's tag it
					click(self.tagButton)
					#click Execute button
					click(self.ExecuteButton)

					#Enter Text on Name Textbox
					click(Region(419,309,175,25))
					type('Tag Sharing Test')
					type(Key.ENTER)

					#enter Text on Notes Textbox
					click(Region(419,349,519,40))
					type('Tag Sharing Test Notes')
					type(Key.ENTER)

					#click Tag
					click(Region(617,604,81,26))

					#click Tag Close button
					click(Region(865,604,81,26))

				else:
					print 'NOK = Initial condition : Tag is already Tagged'
					print " found >" + str.replace(regTagStatus.text(),' ','') + "<"
					break
			if x ==2:
				# check if tag is shared !
				click(self.tagButton)
				#click Execute button
				click(self.ExecuteButton)	
				wait(1)
				strToCompare=Region(303,490,630,86).text()
				print strToCompare
				if strToCompare.find("Tag Sharing Test")> -1:
					print "Big problem Tag is shared !!!"
				else:
					print "No problem, no tag sharing"
				#click Tag Close Button
				click(Region(865,604,81,26))

			click(self.closeRegion)

		# Step 3  ----------------------  Delete TAG

		if self.typeOfObjectOne == "ESC":
			print "first was ESC"
			self.closeRegion = Region(1198,841,99,27)	# Close
			self.tagStatus = Region(755,621,186,32)
			self.tagButton = Region(1057,624,146,29) #Region(759,626,83,19)
			self.ExecuteButton = Region(1077,665,100,26)
		elif self.typeOfObjectOne == "LCP":
			print "first was LCP"
			self.closeRegion = Region(1198,841,99,27)   # Close
			self.tagStatus = Region(754,579,186,32)
			self.tagButton = Region(1055,599,145,23)
			self.ExecuteButton = Region(1077,652,100,26)

		click(tagRegion1)	
		click(self.tagButton)
		click(self.ExecuteButton)

		wait(1)
		#doucleclick on first checkbox
		reg=(Region(278,495,13,13))
		doubleClick(reg)
		wait(1)

		#click ReleaseTag Button
		reg=(Region(738,604,81,26))
		doubleClick(reg)

		#click Tag Close button
		click(Region(865,604,81,26))
		click(self.closeRegion)


	
	def tagTest(self, tagRegion, executeRegion, regTagStatus, tagObject):
		"""This function to create a tag, verify tag is present, delete tag
		   input tagRegion     is the Tag     Button for the equipment
		         executeRegion is the Execute Button region 
				 tagStatus is the text zone region on ECP control panel
				 tagObject is the kind of object ie ESC LIFT..."""
		
		# TAG control system
		# 0/ Test Initial condition: Not Tagged
		# 1/ Enter a tag
		# 2/ Control tag is present
		# 3/ Delete TAG
		# 4/ Test Final condition: Not TAGGED 

		# Step 1 ----------------------------- Enter TAG 

		
		
		# Defining the TAG button & Tag Status Text zone depending on object type
		self.textStatusX2 = 182
		self.textStatusY2 = 26

		# Test initial condition NOT TAGGED, sometimes the status needs delay to be present on the HMI
		blTagOk = False 
		for x in range (1,5):
			if str.replace(regTagStatus.text(),' ','')=='Nottagged':
				blTagOk = True
				print 'OK = Initial condition : Tag is not tagged'
				break
			else:
				print 'NOK = Initial condition : Tag is already Tagged'
				print " found >" + str.replace(regTagStatus.text(),' ','') + "<"
				
			wait(.5)
		if blTagOk == True:
			self.message = ["Initial condition OK:Not Tagged ", " " ,"OK", "For Create TAG " + self.strEquipment]
			self.report.addLine(self.message)
		else:
			self.message = ["Initial condition NOK: already Tagged ", " " ,"NOK", "For Create TAG initial condition false " + self.strEquipment]
			self.report.addLine(self.message)
		

		# click Device Tag button
		click(tagRegion)
		#click Execute button
		click(executeRegion)

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
		click(tagRegion)
		#click Execute button
		click(executeRegion)

		# Step 2  ----------------------  CONTROL TAG IS Present
		wait(1)
		if str.replace(Region(520,484,214,31).text(),' ','')=='TagNoteTest':
			print 'OK = Tag is tagged'
			self.message = ["Tag text found in region ", " " ,"OK", "For Create TAG " + self.strEquipment]
			self.report.addLine(self.message)
		else:
			self.message = ["Tag text NOT found in region ", " " ,"NOK", "For Release TAG " + self.strEquipment]
			print 'NOK = Tag not found'
			self.report.addLine(self.message)
		#click Close
		click(Region(865,604,81,26))


		# Step 3  ----------------------  Delete TAG
		# click Device Tag button
		click(tagRegion)
		#click Execute button
		click(executeRegion)

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
		if str.replace(regTagStatus.text(),' ','')=='Nottagged':
			self.message = ["Tag released OK ", " " ,"OK", self.strEquipment]
			self.report.addLine(self.message)
		else:
			print 'NOK = after tag release Tag is still Tagged'
			self.message = ["Tag is Not released correctly", " " ,"NOK", self.strEquipment]
			self.report.addLine(self.message)

	
	def controlLift(self, objectRegion, strEquipment):
		"""This function to control a lift 
			objectRegion define where is the lift
			strMessage contains the name of the lift
		"""
		#with these oprations
		#	Start
		#	- click on the object then a window appear
		#	- clic on Start button
		#	- click on Execute button
		#	- click on Close button
		#	- verify the image liftOFF.png

		#	Stop
		#	- click on the object then a window appear
		#	- clic on Stop button
		#	- click on Confirm button
		#	- click on Execute button
		#	- click on Close button
		#	- verify the image liftOFF.png

		self.strEquipment = strEquipment
		
		for x in range(1,3):
			click(objectRegion)	# Click on LIFT 
			wait(1)
 
			# Click on Start ----- 1 = Start / 2 = Stop
			# self.report.addLine('Test LIFT Start' + str(x))
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
				#self.report.addLine('Test LIFT Start')
				
				self.GF.findImageInRegionAndReport(objectRegion, self.imagePath + '\\LiftStart.png',1,self.report, "For Start " + strEquipment)
			else:
				#self.report.addLine('Test LIFT Stop')
				self.GF.findImageInRegionAndReport(objectRegion, self.imagePath + '\\LiftStop.png',1,self.report,  "For Stop " + strEquipment)
		
		# check Tag
		click(objectRegion)	# Click on Escalator
		wait(1)
		regBtnTag  = Region(1055,595,146,26) # define "Tagging" button region
		regBtnExectue = Region(1077,649,101,26) # define "Exexute" button region
		regTagStatus  = Region(756,581,180,23) # define "Tag Status" region on control panel
		self.tagTest(regBtnTag, regBtnExectue, regTagStatus, "ESC")
		
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

	def findImageInRegionAndReport(self, region, imagePath, imageSimilarity, report, objMessage):
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
			self.message = ["Region Find", imagePath,"OK", objMessage]
			report.addLine(self.message)
			return True
		except:
			self.message = ["Region Find", imagePath,"NOK", objMessage]
			report.addLine(self.message)
			return False

			

class HTMLReport:
    """HTML Report Generator Class ' A LA ACTIS DRIVE '
	   PathReport = complete path for the html report"""
	#----------------------------------------------------------------------
	# v0.0.4 19-10-2017 check if pathReport exists
	# v0.0.3 11-10-2017 added date to time in the first line of the rapport
	# v0.0.2 10-10-2017 bug corrections
	# v0.0.1 October 2017 - first delivery POC
	#----------------------------------------------------------------------

	
    def __init__(self, pathReport, reportTitle=None, versionProcedure=None):
		# define some things to do at the init
		# WARNING : please use / to declare pathReport instead of \
		
		print "HTMLReport class started v0.0.3 10/10/2017"
		self.reportTitle="Test Actis Drive"
		self.reportTitle = reportTitle
		self.versionProcedure = versionProcedure
		# TODO : check path
		#if os.path.isdir(pathReport):
		#	print ("image path exists")
		#else:print ("HTMLReport error : image path does not exist: " + pathReport )
		
		
		
		# ---- Generate the Report Header 
		#self.html_str = "<hr>"
		#self.html_str = self.html_str + "<b>Automagically test tarting at </b>" + time.strftime('%d-%m-%Y %H:%M:%S')
		#self.html_str = self.html_str + "<hr>"
		self.pathReport = pathReport

		# Header starts here
		self.html_str = "<html lang='en'>"
		self.html_str = self.html_str + "<head>"
		self.html_str = self.html_str + "<meta charset='utf-8'" + chr(47) + "><title>" 
		self.html_str = self.html_str + self.reportTitle
		self.html_str = self.html_str + "<" + chr(47) + "title><link href='results.css' rel='stylesheet' " + chr(47) + "><script src='results.js'><" + chr(47) + "script>"
		self.html_str = self.html_str + "<" + chr(47) + "head>"
		
		# Body starts here
		self.html_str = self.html_str + "<body><h1>" + self.reportTitle + "<" + chr(47) + "h1>"
        # Buttons generation
		self.html_str = self.html_str + "<div>"
		self.html_str = self.html_str + "<input class='displayOptionButton' onclick='displayOnlyTests();' type='button' value='Display OK and NOK'" + chr(47) + ">"
		self.html_str = self.html_str + "<input class='displayOptionButton' onclick='displayOnlyTestsNOK();' type='button' value='Display Only NOK'" + chr(47) + ">"
		self.html_str = self.html_str + "<input class='displayOptionButton' onclick='displayAll();' type='button' value='Display All'" + chr(47) + ">"
		self.html_str = self.html_str + "<input type='hidden' value='2' " + chr(47) + ">"
		self.html_str = self.html_str + "<" + chr(47) + "div>"        
		self.html_str = self.html_str + "<h2>Versions<" +chr(47)+"h2><table><tr" +chr(47)+ "><tr " +chr(47)+ "><" + chr(47) + "table><br " + chr(47) 
		self.html_str = self.html_str + "><br " + chr(47) + "><br " + chr(47) + ">"
		self.html_str = self.html_str + "<h2>Procedure:<" + chr(47) + "h2>"
		
		
		# Start the procedure table
		self.html_str = self.html_str + "<table id='procedures'><tr><td class='tableHeader'>"
		self.html_str = self.html_str + "Date<" + chr(47) + "td><td class='tableHeader'>Instruction<" + chr(47) + "td><td class='tableHeader'>Result<" + chr(47) 
		self.html_str = self.html_str + "td><td class='tableHeader'>Comments<" + chr(47) + "td><" + chr(47) + "tr><tr>"
		
    def addLine(self, Message = []):
		print Message
		try:
			# self.html_str = self.html_str + time.strftime('%H:%M:%S') + ' - '  + stringToAdd + "<br>"
			self.html_str = self.html_str + "<td class='result' colspan='1'>"
			self.html_str = self.html_str + time.strftime("%Y-%m-%d %H:%M:%S") 
			self.html_str = self.html_str + "<" + chr(47) + "td><td class='result' colspan='1'>"
			self.html_str = self.html_str + Message[0] 
			self.html_str = self.html_str + "<img src='file:" + Message[1] + "' alt='F1.png'" 
			self.html_str = self.html_str + "align='middle' width='29' height='58' " + chr(47) + ">" 
			self.html_str = self.html_str + Message[1] + "<" + chr(47) + "td>"
			if Message[2]=="OK":
				self.html_str = self.html_str + "<td class='statusOK'>OK<" + chr(47) + "td><td class='result_res'>" 
			else:
				self.html_str = self.html_str + "<td class='statusNOK'>NOK<" + chr(47) + "td><td class='result_res'>"
			self.html_str = self.html_str + Message[3] + "<" + chr(47) + "td><" + chr(47) + "tr><tr>"
		except:
			self.html_str = self.html_str + time.strftime('%H:%M:%S') + " error trying addLine"  
		
		# </html>

    def writeReport(self):
		self.html_str = self.html_str + "<" + chr(47) + "table><" + chr(47) + "body>"
		self.html_file = open(self.pathReport,'w+')
		self.html_file.write (self.html_str)
		self.html_file.close()