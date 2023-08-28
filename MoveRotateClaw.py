import math
from PySide import QtCore, QtGui
from math import sin, cos, radians
from PySide.QtGui import QInputDialog

repeat = 0
speed = 0
def getUserInput():
  global repeat
  global speed
  repeat =  QtGui.QInputDialog.getInt(None,"Enter number","Cycle to repeat")[0]
  speed =  QtGui.QInputDialog.getInt(None,"Enter speed 5 to 100","Smaller is faster")[0]

# retrieve the objects from the document & set its home placement
linearCam = FreeCAD.ActiveDocument.getObject("Body004015")
#store placement for cam
camHBase= FreeCAD.Vector(0,0,22.7) # Home position
camHRot= FreeCAD.Rotation( FreeCAD.Vector( 0,0,0), 0) # Home rotation in degree
camHPlace = FreeCAD.Placement(camHBase,camHRot)       # make a home Placement object
#get claw and store placement for claw
clawMain= FreeCAD.ActiveDocument.getObject("Body004013")
clawHBase= FreeCAD.Vector(12.6,1.8,29.8) # Home position
clawHRot= FreeCAD.Rotation(FreeCAD.Vector( 0,0,0), 0) # Home rotation
clawHPlace = FreeCAD.Placement(clawHBase,clawHRot)       # make a home Placement object
clawClone1 = FreeCAD.ActiveDocument.getObject('Body004020')
clawClone1HBase=FreeCAD.Vector(-5.25,-12.04,29.8) #center of part is -7.3404, -10.0177, 29.8
clawClone1HRot=FreeCAD.Rotation( FreeCAD.Vector( 0,0,0), -121)
clawClone1HPlace=FreeCAD.Placement(clawClone1HBase,clawClone1HRot) 
#get nut001 and store placement for num001
lockNut= FreeCAD.ActiveDocument.getObject("Nut001")
lockNutHBase= FreeCAD.Vector(0,0,10) # Home BASE position
lockNutHRot= FreeCAD.Rotation( FreeCAD.Vector( 0,0,0), 0) # Home rotation
lockNutHPlace = FreeCAD.Placement(lockNutHBase,lockNutHRot)       # make a home Placement object
#get endNut and store placement for nut
endNut= FreeCAD.ActiveDocument.getObject("Nut")
endNutHBase= FreeCAD.Vector(0,0,10) # Home position
#endNutHRot= FreeCAD.Rotation( FreeCAD.Vector( 180,0,180), 0) # Home rotation
endNutHRot=FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180) 
endNutHPlace = FreeCAD.Placement(endNutHBase,endNutHRot)       # make a home Placement object
#get ThreadedRod and store placement for rod
rod= FreeCAD.ActiveDocument.getObject("ThreadedRod")
rodHBase= FreeCAD.Vector(0,0,58) # Home position
rodHRot=FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180) 
rodHPlace = FreeCAD.Placement(rodHBase,rodHRot)
#plungerCam= FreeCAD.ActiveDocument.addObject("App::Part", "PlungerCam")
newRot= FreeCAD.Rotation( FreeCAD.Vector( 0,1,0), -15) #rotate y axis by 15 deg anti-clockwise
clawMain.Placement = FreeCAD.Placement( clawHBase, newRot)
clawMain.Placement = FreeCAD.Placement( clawMain.Placement.Base + FreeCAD.Vector( 0, 0, 0 ), FreeCAD.Rotation( FreeCAD.Vector( 0,1,0), 25))
#get design parameters of system
ARad = FreeCAD.ActiveDocument.getObject("Sketch011").Constraints[8].Value #cam slope in radians
#get by using name but return value in degrees
AngA=FreeCAD.ActiveDocument.getObject("Sketch011").getDatum('AngA').Value
#get PivB distance of pivot from the center of plunger cam
PivB = FreeCAD.ActiveDocument.getObject("Sketch015").getDatum('PivB').Value/2 #half of diameter
#get value of cam dist from center of plunger cam to contact point
CamDistD = FreeCAD.ActiveDocument.getObject("Sketch016").getDatum('CamDistD').Value/2-0.5 #half of diameter
# get HDistC the horizontal dist from vertical edge(when at home position) to pivot, radius of top of claw
HDistC = FreeCAD.ActiveDocument.getObject("Sketch011").getDatum('HDistC').Value/2
#get HomeDistE1 length of the vertical edge(when at home position) of claw from pivot
HomeDistE1= FreeCAD.ActiveDocument.getObject("Sketch011").getDatum('HomeDistE1').Value
#get HtPivG height from base of foam dot to pivot
HtPivG=FreeCAD.ActiveDocument.getObject("Sketch011").getDatum('HtPivG').Value
tine=FreeCAD.ActiveDocument.getObject("Cylinder")
dot=FreeCAD.ActiveDocument.getObject('Cylinder001')
plungerAssy =FreeCAD.ActiveDocument.getObject('PlungerCam')
#calculate movement
arrPos=[]
rotLimit=50 #equal to 6 degrees
for x in range(0,rotLimit): #break into smallee 1/10 steps
  ClawRotAng=x/10 #  angle in degree
  HtJ = HtPivG-((PivB-CamDistD-(math.sin(((math.atan(HDistC/HomeDistE1)*180/math.pi)-ClawRotAng)*math.pi/180)*math.sqrt(math.pow(HDistC,2)+math.pow(HomeDistE1,2))))/(math.atan(((180-AngA)-ClawRotAng)*math.pi/180))+math.cos(((math.atan(HDistC/HomeDistE1)*180/math.pi)-ClawRotAng)*math.pi/180)*math.sqrt(math.pow(HDistC,2)+math.pow(HomeDistE1,2)))
  HtJ =float('%.3f' % HtJ) #convert to 3 decimal float number
  tmp=[HtJ,ClawRotAng]
  arrPos.append(tmp)

#  "i" represents the angle of rotation in degrees
i = 3
def reset():
   # function to restore initial position of the objects
  global i
  i=3
  clawMain.Placement = clawHPlace
  clawClone1.Placement=clawClone1HPlace
  clawMain.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector( 0,1,0), -arrPos[i][1])
  clawClone1.Placement.Rotation=FreeCAD.Rotation(-121, -arrPos[i][1], 0)
  linearCam.Placement = camHPlace
  lockNut.Placement = lockNutHPlace
  endNut.Placement = endNutHPlace
  tine.Placement.Base.z = 0.5
  dot.Placement.Base.z = 0
  zChange = arrPos[i][0] -  camHBase.z
  plungerAssy.Placement.Base.z =zChange #add 1 empty line below, otherwise error
  if zChange < -2: 
    tine.Placement.Base.z = -4
    dot.Placement.Base.z = -4.5
  

reset()
getUserInput()
reverse = False
cycle=0
def update(): 
  global i #declare this touse the 1 variable in te global. If not, i is a new local variable
  global reverse
  global cycle
  global repeat
  global speed#no need to declare since speed is called in global only, not inside function
  #linearCam.Placement.Base = FreeCAD.Vector(0,0,arrPos[i][0])
  newZ = arrPos[i][0] -  camHBase.z
  FreeCAD.Console.PrintMessage(str(reverse)+'; i='+str(i)+'; NewZ='+str(newZ)+'\n')
  if not reverse:
    tine.Placement.Base.z = 0.5 + newZ
    dot.Placement.Base.z = 0 + newZ
    if newZ < -1.5:
      tine.Placement.Base.z = -4
      dot.Placement.Base.z = -4.5

  plungerAssy.Placement.Base.z = newZ
  clawMain.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector( 0,1,0), -arrPos[i][1])
  clawClone1.Placement.Rotation=FreeCAD.Rotation(-121, -arrPos[i][1], 0)
  FreeCAD.Gui.updateGui()
   # increase mechanism input position
  if i == rotLimit - 1:  reverse = True
  if reverse : 
    i -= 1
    if newZ >-0.5:
      tine.Placement.Base.z = 0.5
      dot.Placement.Base.z = 0
  else: i += 1
  if i == 0 and reverse:
    reverse = False
    #FreeCAD.Console.PrintMessage(reverse)
    i=0
    cycle += 1
    if cycle == repeat:
      reset()
      timer.stop()
      reverse = False
      cycle = 0

# create a timer object
timer = QtCore.QTimer()
# connect timer event to function "update"
timer.timeout.connect( update )
# start the timer by triggering "update" every 10 ms
timer.start(speed)


