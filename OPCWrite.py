import OpenOPC
print ('-------------------------------')
print ('')
print ('--- OPC Python test program ---')
print ('')
print ('-------------------------------')
print ('')
opc = OpenOPC.client()

lsServer = 'S2K.OpcServer.1'
lsItem = 'L4A1'
lsSubItem = 'PPLOOP3CB1'
ls2SubItem = 'RM02'

ls1SubItem = lsItem + '.' + lsSubItem
ls2SubItem = ls1SubItem + '.' + ls2SubItem



print ('--- This is the list of OPC Servers ')
print opc.servers()
print ('---')


## DCOM Mode used
opc.connect(lsServer)

## Open using the OpenPC Gateway service
# opc.OpenOPC.open_client('localhost')

try:
    print ('')
    opc.connect(lsServer)
    print ('Connection to ' + lsServer )
    print opc.info()
    print ('---')
except:
    print ('Connection to the requested server has failed')


## getting list of available items
print ('--- This is list of available items')
print opc.list()
print ('---')


print ('--- Reading List Item from ' + lsItem)
print opc.list(lsItem)
print ('---')

print ('--- Reading List Item from ' + ls1SubItem )
print opc.list(ls1SubItem )
print ('---')

print ('--- Properties for ls2SubItem ---')
try:
    print opc.properties (ls2SubItem)
except:
    print ('--- Error : no properties for this sub item + ' + ls2SubItem)


print('--- Closing session ---')
opc.close()

