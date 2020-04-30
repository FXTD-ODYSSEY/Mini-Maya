from maya import standalone as std
std.initialize()

from maya import cmds

cube = cmds.polyCube(ch=0)[0]
cmds.polySmooth(cube,sdt=2)
cmds.polySmooth(cube,sdt=2)
cmds.polyReduce(cube)


import os
import sys
DIR = os.path.dirname(__file__)
file_path = os.path.realpath(os.path.join(DIR,"a.ma"))
cmds.file(rename=file_path)
cmds.file(save=1,type="mayaAscii")

# mel.eval("$temp = $gMainWindow")

