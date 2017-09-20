# ESCALATORS and LIFTS TEST
# Proto 07/09/2017 - RC SCALIAN for ALSTOM

# 
# %SystemRoot%\system32;
# %SystemRoot%;%SystemRoot%\System32\Wbem;
# %SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;
# C:\Program Files\Microsoft SQL Server\110\DTS\Binn\;
# C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\;
# C:\Program Files\Microsoft SQL Server\110\Tools\Binn\;
# C:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\;
# C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\IDE\PrivateAssemblies\;
# C:\Program Files (x86)\Microsoft SQL Server\110\DTS\Binn\;
# C:\Program Files (x86)\Microsoft SQL Server\80\Tools\Binn\;
# C:\Program Files (x86)\Alstom\ICONIS\S2K\Bin\Common\;
# C:\Program Files\Alstom\ICONIS\S2K\Bin\Server;
# C:\Python27\;C:\Python27\Scripts;C:\Python27\Lib;C:\Python27\Lib\site-packages;C:\Python27\libs;c:\OpenOPC\bin


# L4G1.ECP.RM00 - RM06
# TABMDBRW.NAE1.RW12
# TABMDBRW.NAE1.RW13
# TABMDBRW.NAE1.RW14

from time import sleep

print
print '--------------------------------------'
print '---- OPC LIFTS & ESCALATORS TESTS ----'
print '        on Alstom.S8000.1'
print '        Riyadh L46'
print ''

import OpenOPC
class ServerCommunication:
	"""A class to manage communcation between OpenOPC and Alstom.S8000 server """
	def __init__(self):
		self.opc = OpenOPC.client()		

	def connect(self, server):
		try:
			status_conn =  self.opc.connect(server)
			print 'status ' 
			print status_conn
		except:
			print 'Connection to server failed  ->' + server
			print ' Exit ' 
			quit(0)

	def properties(self,tag):
		self._printList(self.opc.properties(tag))

	def servers_list(self):
		self._printList (self.opc.servers())

	def list(self, tag):
		self._printList(self.opc.list(tag))

	def writeTag(self, tag, value):
		try:
			if (self.opc.write([tag,value]))=="Error":	
				print 'Write is not working on tag ' + tag
			else:
				print 'write done on tag ' + tag
		except:
			print 'writeTag function on tag ' + tag

	def close(self):
		self.opc.close()
		print 'connection closed'

	def _printList(self, elements):
		i = 1
		max_element = 10
		for element in elements:
			print element
			if i > max_element:
				print 'more than ' + str(max_element) + ' entries'
				break
			i = i + 1
	def printValue(self, tag):
		elements = self.opc.properties(tag)
		i = 1
		for element in elements:
			if i ==3:
				print element
				break
			i = i + 1

''' --------------------------------------------   END OF CLASS '''

server = 'Alstom.S8000.1'

tag1 =   'L4G1'
tag2 =   tag1 + '.ECP1'
tag3 =   tag2 + '.CONTROL'

my_server = ServerCommunication()

print 'List of servers'
my_server.servers_list()

print
print 'connection to server ' + server
my_server.connect(server)

print 'list of tag for ' + tag1
my_server.list(tag1) 

print 'properties of last tag in the tree'
my_server.properties(tag3)

# TABMDBRW.NAE1.RW12
# TABMDBRW.NAE1.RW13
# TABMDBRW.NAE1.RW14




tag3 = 'L4G1.TABMDBRW.NAE1.RW12'

my_server.printValue(tag3)
my_server.writeTag(tag3, 0)
sleep(2)
my_server.writeTag(tag3, 1)
sleep(2)
my_server.writeTag(tag3, 2)
sleep(2)
my_server.writeTag(tag3, 4)
sleep(2)
my_server.writeTag(tag3, 8)


my_server.close()