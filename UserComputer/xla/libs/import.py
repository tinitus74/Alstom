if not 'd:/Tools/alstom' in sys.path:sys.path.append('d:/Tools/alstom')
import alstom

GF = alstom.GraphicFunctions()
myReport = alstom.HTMLReport('d:/Tools/alstom/reports/EM4G1')
myControl = alstom.ControlHMI('d:\Tools\alstom\reports\EM4G1', GF, myReport) 

# Sample 3 lines to remove
# myReport.addLine("Check LIFT LCP1 - on L4G1")
# myControl.controlLift(Region(891, 644,33,33))
# myReport.writeReport()
# end of region to remove