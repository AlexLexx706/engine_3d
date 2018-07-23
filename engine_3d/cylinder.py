# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from engine_3d import shape


class Cylinder(shape.Shape):
    def __init__(
            self,
            radius=1,
            length=1,
            segments=10,
            **kwargs):
        """
        Cylinder shape
        """
        shape.Shape.__init__(self, **kwargs)
        self.radius = radius
        self.length = length
        self.segments = segments

    def make(self):
        glNewList(self.list_id, GL_COMPILE)
        glRotate(90, 0, 1, 0)
        quadric = gluNewQuadric()
        gluQuadricOrientation(quadric, GLU_INSIDE)
        gluDisk(quadric, 0, self.radius, self.segments, 1)
        gluQuadricOrientation(quadric, GLU_OUTSIDE)
        gluCylinder(quadric, self.radius, self.radius,
                    self.length, self.segments, 1)
        glTranslatef(0, 0, self.length)
        gluDisk(quadric, 0, self.radius, self.segments, 1)
        glEndList()


if __name__ == '__main__':
    sphere()
