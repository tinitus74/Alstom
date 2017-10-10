# USAGE : please add the 2 following lines below to your sikuli script 
# if not 'd:\Tools\alstom' in sys.path:sys.path.append('d:\Tools\alstom')
# import alstom
# --------------------- Enjoy !

import time

class GraphicFunctions:
	"""Graphic Functions to do some operations using Sikuli"""
	def __init__(self):
		#define some things to do at the init
		print "GF started v0.0.01 10/10/2017"
		
	def findImageInRegion(self, region, imagePath, imageSimilarity):
		""" This function to find in image in a region
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
		""" This function to find in image in a region
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
			report.addLine(" - Image found " + imagePath + " in region " + str(region.x) + " " + str(region.y))
			return True
		except:
			report.addLine("<font color=red> - ERROR ! Image not found " + imagePath + " in region " + str(region.x) + " " + str(region.y) + "</font>")
			return False

			

class HTMLReport:
    """HTML Report Generator Class """
    def __init__(self, pathReport):
		#define some things to do at the init
		print "HTMLReport class started"
		self.html_str = "<hr>"
		self.html_str = self.html_str + "<b>Automagically test tarting at </b>" + time.strftime('%H:%M:%S')
		self.html_str = self.html_str + "<hr>"
		self.pathReport = pathReport
    def addLine(self, stringToAdd):
        try:
			self.html_str = self.html_str + time.strftime('%H:%M:%S') + ' - '  + stringToAdd + "<br>"
        except:
			self.html_str = self.html_str + time.strftime('%H:%M:%S') + " error trying addLine"  

    def writeReport(self):
        print "writeReport OK"
        self.html_file = open(self.pathReport,'w')
        self.html_file.write (self.html_str)
        self.html_file.close()