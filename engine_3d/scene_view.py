# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from engine_3d import shape
import engine_3d


class SceneView(QtOpenGL.QGLWidget):
    # сигнал, движение курсора:
    # Camera, QPoint, состояние: 0-начало, 1-движение, 2-конец
    cursor_move = QtCore.pyqtSignal(object, object, int)
    CAMERA_SCALE_STEP = 50

    def __init__(self, *args, **kwargs):
        QtOpenGL.QGLWidget.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)
        self.scale_camera = False
        self.rotate_camera = False
        self.move_cursor = False
        self.old_cursore_pos = None
        self.center = shape.Shape()

    def sizeHint(self):
        return QtCore.QSize(1024, 768)

    @property
    def scene(self):
        return engine_3d.CUR_SCENE

    def initializeGL(self):
        # glutInit(sys.argv)
        self.scene.initializeGL()

    def paintGL(self):
        self.scene.update()

    def resizeEvent(self, event):
        QtOpenGL.QGLWidget.resizeEvent(self, event)

    def resizeGL(self, width, height):
        self.scene.resizeGL(width, height)

    def update(self):
        self.updateGL()

    def mouseMoveEvent(self, event):
        if self.scale_camera:
            offset = (event.pos() - self.old_cursore_pos).y()
            self.scene.camera.move_eye(offset * 2)
        elif self.rotate_camera:
            offset = event.pos() - self.old_cursore_pos
            self.scene.camera.rotate_camera(
                -offset.x() * 0.001, -offset.y() * 0.001)
        elif self.move_cursor:
            # сдвиг камеры
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                s_p = self.scene.camera.get_mouse_pos(QtCore.QPoint(0, 0))
                n_p = self.scene.camera.get_mouse_pos(
                    event.pos() - self.old_cursore_pos)
                self.scene.camera.pos -= (n_p - s_p)
            else:
                self.cursor_move.emit(self.scene.camera, event.pos(), 1)
        self.old_cursore_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if QtCore.Qt.MidButton == event.button():
            self.scale_camera = False
        elif QtCore.Qt.RightButton == event.button():
            self.rotate_camera = False
        elif QtCore.Qt.LeftButton == event.button():
            self.move_cursor = False
            if not (event.modifiers() & QtCore.Qt.ShiftModifier):
                self.cursor_move.emit(self.scene.camera, event.pos(), 2)

    def mousePressEvent(self, event):
        self.old_cursore_pos = event.pos()

        # средняя кнопка
        if QtCore.Qt.MidButton == event.button():
            self.scale_camera = True
        elif QtCore.Qt.RightButton == event.button():
            self.rotate_camera = True
        elif QtCore.Qt.LeftButton == event.button():
            self.move_cursor = True
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                self.old_3d_cur_pos = self.scene.camera.get_mouse_pos(
                    event.pos())
            else:
                self.cursor_move.emit(self.scene.camera, event.pos(), 0)

    def keyPressEvent(self, event):
        '''change camera scale'''
        if event.key() == QtCore.Qt.Key_Equal:
            self.scene.camera.move_eye(-self.CAMERA_SCALE_STEP)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.scene.camera.move_eye(self.CAMERA_SCALE_STEP)

    def wheelEvent(self, event):
        '''Uased for change camera scale factor'''
        self.scene.camera.move_eye(event.angleDelta().y() * 0.1)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = GLWidget()
    mainWin.show()
    sys.exit(app.exec_())
