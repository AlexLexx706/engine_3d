# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from engine_3d import shape


class Sphere(shape.Shape):
    def __init__(
            self,
            radius=1,
            segments=10,
            **kwargs):
        """
        Shpere shape
        """
        shape.Shape.__init__(self, **kwargs)
        self.radius = radius
        self.segments = segments

    def make(self):
        glNewList(self.list_id, GL_COMPILE)
        gluSphere(
            gluNewQuadric(),
            self.radius,
            self.segments,
            self.segments)
        glEndList()


if __name__ == '__main__':
    sphere()
