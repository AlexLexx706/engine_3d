# -*- coding: utf-8 -*-
import logging
import numpy as np
import math
from engine_3d import scene
from engine_3d import transformations
from engine_3d import vector

LOG = logging.getLogger(__name__)


class Node:
    '''Base class for all objects in engines'''
    o_x = vector.Vector(1.0, 0.0, 0.0)
    o_y = vector.Vector(0.0, 1.0, 0.0)
    o_z = vector.Vector(0.0, 0.0, 1.0)
    freedom_x_angle = None
    freedom_y_angle = None
    freedom_z_angle = None

    def __init__(
            self,
            parent=None,
            pos=vector.Vector(0.0, 0.0, 0.0),
            axis=vector.Vector(1.0, 0.0, 0.0),
            up=None,
            **kwargs):
        """
            Создание фрейма.
            Параметры:
            parent - родитель
            pos - позиция в локальных координатах
            axis - орт x
            up  - орт y
        """
        self.parent = parent

        axis = vector.Vector(axis).norm()
        # Определение осей
        up = vector.Vector(0.0, 1.0, 0.0) if up is None else\
            vector.Vector(up).norm()

        up = axis.cross(up).cross(axis)
        if up.mag == 0:
            up = axis.cross(
                vector.Vector(-1.0, 0.0, 0.0)).cross(axis)

        self._matrix = np.identity(4)
        self._matrix[:3, 0] = axis
        self._matrix[:3, 1] = up
        self._matrix[:3, 2] = axis.cross(up)
        self._matrix[:3, 3] = pos
        self.scene = scene.Scene.cur_scene()
        self.scene.frames.append(self)
        self.childs = []

        if self.parent is not None:
            self.parent.childs.append(self)

    def set_freedom_x_angle(self, freedom):
        self.freedom_x_angle = freedom

    def get_freedom_x_angle(self):
        return self.freedom_x_angle

    def set_freedom_y_angle(self, freedom):
        self.freedom_y_angle = freedom

    def get_freedom_y_angle(self):
        return self.freedom_y_angle

    def set_freedom_z_angle(self, freedom):
        self.freedom_z_angle = freedom

    def get_freedom_z_angle(self):
        return self.freedom_z_angle

    @property
    def axis(self):
        '''орт оси x'''
        return self._matrix[:3, 0].view(vector.Vector)

    @property
    def up(self):
        '''орт оси y'''
        return self._matrix[:3, 1].view(vector.Vector)

    @property
    def pos(self):
        '''позиция в локальных координатах'''
        return self._matrix[:3, 3].view(vector.Vector)

    @pos.setter
    def pos(self, pos):
        '''установит позицию в локальных координатах'''
        self._matrix[:3, 3] = pos

    @property
    def matrix(self):
        '''Возвращает матрицу фрейма'''
        return self._matrix if self.parent is None else\
            self.parent.matrix.dot(self._matrix)

    def remove(self):
        '''Удалить со сцены'''
        self.scene.frames.remove(self)

        for ch in self.childs:
            ch.parent = None

        if self.parent is not None:
            self.parent.childs.remove(self)
        self.childs = []

    def frame_to_world(self, frame_pos):
        u'''Преобразует локальные координаты frame_pos в глобальные'''
        return vector.Vector(
            self.matrix.dot(
                np.array((frame_pos[0], frame_pos[1], frame_pos[2], 1.0)))[:3])

    def world_to_frame(self, world_pos):
        """
            Преобразует глобальные координаты world_pos
            в локальные координаты фрейма
        """
        m = self.matrix
        pos = vector.Vector(world_pos) - m[:3, 3]
        return vector.Vector(m.T.dot(np.array((
            pos[0], pos[1], pos[2], 0.)))[:3])

    def rotate(self, angle, axis, point=None):
        '''
            вращать во круг заданной оси axis
            относительно заданной точки point
            на угол angle
        '''
        pos = self._matrix[:3, 3].copy()
        self._matrix[:3, 3] = (0, 0, 0)
        r_m = transformations.rotation_matrix(angle, axis, point)
        self._matrix = r_m.dot(self._matrix)
        self._matrix[:3, 3] = pos

    def get_proj_angle(self, axis, up, vec):
        """
            возвращает угол проекции vec на плоскость (axis, up),
            угол отсчитывается от axis"""
        return math.atan2(up.dot(vec), axis.dot(vec))

    def set_proj_angle(self, freedom, angle, axis, up, vec):
        """
            Выстовить угол проекции вектора на плоскость axis,
            up с учётом проидолов
        """
        if freedom is not None:
            if angle < freedom[0]:
                angle = freedom[0]

            if angle > freedom[1]:
                angle = freedom[1]

        # установим угол
        offset_angle = angle - self.get_proj_angle(axis, up, vec)
        self.rotate(angle=offset_angle, axis=axis.cross(up))

    def get_angle_x(self):
        '''return angle by x ort'''
        return self.get_proj_angle(self.o_y, self.o_z, self.up)

    def set_angle_x(self, angle):
        self.set_proj_angle(
            self.freedom_x_angle, angle, self.o_y, self.o_z, self.up)

    def get_angle_y(self):
        return self.get_proj_angle(
            self.o_z, self.o_x, self.axis.cross(self.up))

    def set_angle_y(self, angle):
        self.set_proj_angle(
            self.freedom_y_angle, angle,
            self.o_z, self.o_x, self.axis.cross(self.up))

    def get_angle_z(self):
        return self.get_proj_angle(self.o_x, self.o_y, self.axis)

    def set_angle_z(self, angle):
        self.set_proj_angle(
            self.freedom_z_angle, angle,
            self.o_x, self.o_y, self.axis)

    ang_x = property(get_angle_x, set_angle_x)
    ang_y = property(get_angle_y, set_angle_y)
    ang_z = property(get_angle_z, set_angle_z)

    def update(self):
        '''
            Вызывается сценой нужно использовать для
            обновления внутренней логики'''
        pass


if __name__ == "__main__":
    f = Node(pos=(12, 23, 3))
    print(f.pos)
    print(f.up)
    print(f.axis)
    print(f.matrix)
    print(f.frame_to_world(vector.Vector((1, 2, 3))))
    print(f.world_to_frame((12, 12, 23)))
