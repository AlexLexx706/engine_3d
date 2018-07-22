import sys
from PyQt4 import QtGui
from engine_3d import scene_view


app = QtGui.QApplication(sys.argv)
view = scene_view.SceneView()
view.show()
sys.exit(app.exec_())
