# -*- coding: utf-8 -*-
from OpenGL.GL import *
import engine_3d
from engine_3d import camera


class Scene():
    def __init__(self):
        self.frames = []
        if engine_3d.CUR_SCENE is None:
            engine_3d.CUR_SCENE = self
        self.camera = camera.Camera()

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for frame in self.frames:
            frame.update()

        self.camera.update_camera()

    def initializeGL(self):
        lightPos = (200, 0.0, 2000.0, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_COLOR_MATERIAL)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glEnable(GL_BLEND)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        side = min(width, height)
        if side < 0:
            return
        glViewport(
            int((width - side) / 2),
            int((height - side) / 2),
            side,
            side)
