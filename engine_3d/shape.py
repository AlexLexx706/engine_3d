# -*- coding: utf-8 -*-
from OpenGL.GL import *
from engine_3d import node


class Shape(node.Node):
    def __init__(self, color=(1.0, 1.0, 1.0), **kwargs):
        '''Base class for all shapes (box, cilinder, sphere).'''
        node.Node.__init__(self, **kwargs)
        self.color = color
        self.list_id = None
        self.visible = True
        self.first_make = True

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
            glCallList(self.list_id)


if __name__ == '__main__':
    Shape()
