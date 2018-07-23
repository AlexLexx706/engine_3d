import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from engine_3d import scene_view


app = QtWidgets.QApplication(sys.argv)
view = scene_view.SceneView()
view.show()
sys.exit(app.exec_())
