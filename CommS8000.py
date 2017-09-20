import OpenOPC
from time import sleep

def printList(elements):
	i = 1
	for element in elements:
		print element
		if i > 100:
			print 'more than 100 entries'
			break
		i = i + 1




server = 'Alstom.S8000.1'
tag1 =   'L4A1'
tag2 =   tag1 + '.PPLOOP3CB1'
tag3 =   tag2 + '.RM10'


server = 'S2K.OpcServer.1'
tag1 = 'L46C2D1_LPS1LOOP2ACC'
tag2 = tag1 + '.ALARM_STATE.AL_CMD_ABORT'
tag3 = tag2 + '.LABEL.LABEL.Value.Quality'

#L46C2D1_LPS1LOOP2ACC.ALARM_STATE.AL_CMD_ABORT.LABEL.LABEL.Value.Quality

print
print '--------------------------------'
print '---- OPC Test : ' + server
print 

#opc = OpenOPC.open_client('localhost') #OpenOPC.client()
opc = OpenOPC.client()



print '--- Servers'
printList (opc.servers())
print '------------------'

for i  in [1, 2]:

	if i == 1:
		server = 'S2K.OpcServer.1'
		tag1 = 'L46C2D1_LPS1LOOP2ACC'
		tag2 = tag1 + '.ALARM_STATE.AL_CMD_ABORT'
		tag3 = tag2 + '.LABEL.LABEL.Value.Quality'

	else:
		server = 'Alstom.S8000.1'
		tag1 =   'L4A1'
		tag2 =   tag1 + '.PPLOOP3CB1'
		tag3 =   tag2 + '.RM10'
		#tag2 = tag1 + '.CABLELPSLOOP1'
		#tag3 = tag2 + '.STATE'

	
	try:
		opc.connect(server)
	except:
		print 'Connection to server failed  ->' + server
		print '--------------------------------------' 
		quit(0)

	print '--- Server info ' + server
	printList(opc.info())
	print

#print '--- List info = root'
#printList (opc.list())
#print

#print '--- List info=' + tag1
#printList (opc.list(tag1))
#print

#print '--- List info=' + tag2
#printList (opc.list(tag2))
#print

print '--- List properties of tag =' + tag3
printList (opc.properties(tag3))
print

#opc.read(tag3,group='test',update=3000)
#for name, value, quality in opc.iread(tag3, group = 'test'):
# print name, value, quality

opc[tag3] = 1

# print data_pull

print opc.groups()
print opc.remove('test')


opc.close()

print '------------------'
print
