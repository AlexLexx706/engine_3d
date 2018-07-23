# -*- coding: utf-8 -*-
from OpenGL.GL import *
from engine_3d import shape
from engine_3d import vector


class Box(shape.Shape):
    def __init__(
            self,
            length=1,
            height=1,
            width=1,
            size=None,
            **kwargs):
        '''Box shape'''
        shape.Shape.__init__(self, **kwargs)
        self.length = length
        self.height = height
        self.width = width

        if size is not None:
            self.length = size[0]
            self.height = size[1]
            self.width = size[2]

    def make(self):
        d_x = self.length / 2.0
        d_y = self.height / 2.0
        d_z = self.width / 2.0

        glNewList(self.list_id, GL_COMPILE)
        glBegin(GL_QUADS)           # Start Drawing The Cube
        glNormal3f(0.0, 1.0, 0.0)       # Top Right Of The Quad (Top)
        glVertex3f(-d_x, d_y, +d_z)     # Top Right Of The Quad (Top)
        glVertex3f(+d_x, d_y, +d_z)     # Top Left Of The Quad (Top)
        glVertex3f(+d_x, d_y, -d_z)     # Bottom Left Of The Quad (Top)
        glVertex3f(-d_x, d_y, -d_z)     # Bottom Right Of The Quad (Top)

        glNormal3f(0.0, -1.0, 0.0)      # Top Right Of The Quad (Top)
        glVertex3f(-d_x, -d_y, +d_z)        # Top Right Of The Quad (Bottom)
        glVertex3f(-d_x, -d_y, -d_z)        # Top Left Of The Quad (Bottom)
        glVertex3f(+d_x, -d_y, -d_z)        # Bottom Left Of The Quad (Bottom)
        glVertex3f(+d_x, -d_y, +d_z)        # Bottom Right Of The Quad (Bottom)

        glNormal3f(0.0, 0.0, 1.0)       # Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, +d_z)  # Top Right Of The Quad (Front)
        glVertex3f(-d_x, -d_y, +d_z)  # Top Left Of The Quad (Front)
        glVertex3f(+d_x, -d_y, +d_z)  # Bottom Left Of The Quad (Front)
        glVertex3f(+d_x, +d_y, +d_z)  # Bottom Right Of The Quad (Front)

        glNormal3f(0.0, 0.0, -1.0)      # Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, -d_z)        # Bottom Left Of The Quad (Back)
        glVertex3f(+d_x, +d_y, -d_z)        # Bottom Right Of The Quad (Back)
        glVertex3f(+d_x, -d_y, -d_z)        # Top Right Of The Quad (Back)
        glVertex3f(-d_x, -d_y, -d_z)        # Top Left Of The Quad (Back)

        glNormal3f(-1.0, 0.0, 0.0)      # Top Right Of The Quad (Top)
        glVertex3f(-d_x, +d_y, +d_z)        # Top Right Of The Quad (Left)
        glVertex3f(-d_x, +d_y, -d_z)        # Top Left Of The Quad (Left)
        glVertex3f(-d_x, -d_y, -d_z)        # Bottom Left Of The Quad (Left)
        glVertex3f(-d_x, -d_y, +d_z)        # Bottom Right Of The Quad (Left)

        glNormal3f(1.0, 0.0, 0.0)       # Top Right Of The Quad (Top)
        glVertex3f(d_x, +d_y, +d_z)  # Top Right Of The Quad (Right)
        glVertex3f(d_x, -d_y, +d_z)  # Top Left Of The Quad (Right)
        glVertex3f(d_x, -d_y, -d_z)  # Bottom Left Of The Quad (Right)
        glVertex3f(d_x, +d_y, -d_z)  # Bottom Right Of The Quad (Right)
        glEnd()                         # Done Drawing The Quad
        glEndList()


if __name__ == '__main__':
    box()
