# -*- coding: utf-8 -*-
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
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
        if sys.platform != 'win32':
            glNewList(self.list_id, GL_COMPILE)
            glutSolidSphere(self.radius, self.segments, self.segments)
            glEndList()
        else:
            self.create_box()

    def create_box(self):
        print('Sphere.create_box radius: self.radius:%s' % (self.radius, ))
        glNewList(self.list_id, GL_COMPILE)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-self.radius, self.radius, +self.radius)
        glVertex3f(+self.radius, self.radius, +self.radius)
        glVertex3f(+self.radius, self.radius, -self.radius)
        glVertex3f(-self.radius, self.radius, -self.radius)

        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-self.radius, -self.radius, +self.radius)
        glVertex3f(-self.radius, -self.radius, -self.radius)
        glVertex3f(+self.radius, -self.radius, -self.radius)
        glVertex3f(+self.radius, -self.radius, +self.radius)

        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(-self.radius, +self.radius, +self.radius)
        glVertex3f(-self.radius, -self.radius, +self.radius)
        glVertex3f(+self.radius, -self.radius, +self.radius)
        glVertex3f(+self.radius, +self.radius, +self.radius)

        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-self.radius, +self.radius, -self.radius)
        glVertex3f(+self.radius, +self.radius, -self.radius)
        glVertex3f(+self.radius, -self.radius, -self.radius)
        glVertex3f(-self.radius, -self.radius, -self.radius)

        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-self.radius, +self.radius, +self.radius)
        glVertex3f(-self.radius, +self.radius, -self.radius)
        glVertex3f(-self.radius, -self.radius, -self.radius)
        glVertex3f(-self.radius, -self.radius, +self.radius)

        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(self.radius, +self.radius, +self.radius)
        glVertex3f(self.radius, -self.radius, +self.radius)
        glVertex3f(self.radius, -self.radius, -self.radius)
        glVertex3f(self.radius, +self.radius, -self.radius)
        glEnd()
        glEndList()


if __name__ == '__main__':
    sphere()
