# -*- coding: utf-8 -*-
from OpenGL.GL import *
from engine_3d import node
from engine_3d import vector


class Shape(node.Node):
    line_width = 4.0
    center_length = 10.0

    def __init__(
            self,
            color=(1.0, 1.0, 1.0),
            show_center=True,
            offset=vector.Vector(0.0, 0.0, 0.0),
            **kwargs):
        '''Base class for all shapes (box, cilinder, sphere).
            colol - shape color
            show_center - show center of shape
            offset - offset of shape
        '''
        node.Node.__init__(self, **kwargs)
        self.color = color
        self.list_id = None
        self.visible = True
        self.first_make = True
        self.show_center = show_center
        self.offset = offset

    def make(self):
        '''Call for create opengl object,
            for create gllist object, can be used self.list_id
        '''
        pass

    def remove(self):
        '''Remove object fom scene, and free glList
        '''
        if self.list_id is not None:
            glDeleteLists(self.list_id, 1)
        node.Node.remove(self)

    def update(self):
        '''Called periodecly by scene and draw object'''
        if self.first_make:
            if self.list_id is None:
                self.list_id = glGenLists(1)
            self.make()
            self.first_make = False

        if self.visible:
            glLoadMatrixd(self.matrix.T)
            glColor(self.color)
            glPushMatrix()
            glTranslated(*self.offset)
            glCallList(self.list_id)
            glPopMatrix()

            # show center
            if self.show_center:
                # disable lighting
                glDisable(GL_LIGHTING)

                glLineWidth(self.line_width)
                glBegin(GL_LINES)
                glColor3f(1.0, 0.0, 0.0)
                glVertex3f(0.0, 0.0, 0.0)
                glVertex3f(self.center_length, 0, 0)

                glColor3f(0.0, 1.0, 0.0)
                glVertex3f(0.0, 0.0, 0.0)
                glVertex3f(0, self.center_length, 0)

                glColor3f(0.0, 0.0, 1.0)
                glVertex3f(0.0, 0.0, 0.0)
                glVertex3f(0, 0, self.center_length)
                glEnd()

                # enable lighting
                glEnable(GL_LIGHTING)


if __name__ == '__main__':
    Shape()
