#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from engine_3d import node
from engine_3d import vector
import math


class Bone(node.Node):
    def __init__(
            self,
            freedom_x_angle=None,
            freedom_y_angle=None,
            freedom_z_angle=None,
            **kwargs):
        """
            Обьект кость,
                с помощью кости можно решать задачу инверсной кинематики
            freedom_x_angle, freedom_y_angle,
                freedom_z_angle- ограничения вращения,
                None или (start_angle, end_angle) - углы в радианах
        """
        node.Node.__init__(self, **kwargs)
        self.targets = []
        self.freedom_x_angle = freedom_x_angle
        self.freedom_y_angle = freedom_y_angle
        self.freedom_z_angle = freedom_z_angle

    def calk_ik_on_plane(self, plane, base_axis, freedom, target, end):
        '''Рассчёт кинематики для оси'''
        if end.mag == 0:
            return

        axis, up = plane

        # делаем проекцию end на плоскость
        pos_proj = axis * axis.dot(end) + up * up.dot(end)

        # проверяем возможность поворота.
        if pos_proj.mag > 0.001:
            # делаем проекцию target на плоскость
            target_proj = axis * axis.dot(target) + up * up.dot(target)

            # найдём угол между векторами.
            offset_angle = target_proj.diff_angle(pos_proj)
            rotate_axis = axis.cross(up)

            # определим знак угла.
            if target_proj.dot(rotate_axis.cross(pos_proj)) < 0:
                offset_angle = -offset_angle

            # текущий угол поворота в плоскости
            cur_angle = self.get_proj_angle(axis, up, base_axis)
            dest_angle = cur_angle + offset_angle

            # меньше минимума
            if dest_angle < freedom[0]:
                offset_angle = freedom[0] - cur_angle
            # больше максимума
            elif dest_angle > freedom[1]:
                offset_angle = freedom[1] - cur_angle

            self.rotate(angle=offset_angle, axis=rotate_axis)

    def calk_ik_on_plane_2(self, plane, base_axis, freedom, targets):
        '''Рассчёт кинематики для оси'''
        offset_angle = 0

        for target, end, weight in targets:
            offset_angle += self.calk_ik_offset_angle(
                plane, base_axis, freedom, target, end) * weight

        axis, up = plane
        # текущий угол поворота в плоскости
        cur_angle = self.get_proj_angle(axis, up, base_axis)
        dest_angle = cur_angle + offset_angle

        # меньше минимума
        if dest_angle < freedom[0]:
            offset_angle = freedom[0] - cur_angle

        # больше максимума
        elif dest_angle > freedom[1]:
            offset_angle = freedom[1] - cur_angle

        if offset_angle != 0.0:
            rotate_axis = axis.cross(up)
            self.rotate(angle=offset_angle, axis=rotate_axis)

    def calk_ik_offset_angle(self, plane, base_axis, freedom, target, end):
        '''Рассчёт угла смещения для IK'''
        if end.mag == 0:
            return 0.0

        axis, up = plane

        # делаем проекцию end на плоскость
        pos_proj = axis * axis.dot(end) + up * up.dot(end)

        # проверяем возможность поворота.
        if pos_proj.mag > 0.001:
            # делаем проекцию target на плоскость
            target_proj = axis * axis.dot(target) + up * up.dot(target)

            # найдём угол между векторами.
            offset_angle = target_proj.diff_angle(pos_proj)
            rotate_axis = axis.cross(up)

            # определим знак угла.
            if target_proj.dot(rotate_axis.cross(pos_proj)) < 0:
                offset_angle = -offset_angle
            return offset_angle
        return 0.0

    def calk_ik_pos_2(self, targets):
        '''Рассчёт инверсной кинематики'''
        # 1. переведём в локальную систему координат
        cur_targets = []

        glob_targets = []
        for glob_target, end, weight in targets:
            glob_targets.append(glob_target)
            cur_targets.append((self.world_to_frame(glob_target), end, weight))

        for glob_target, end, weight in self.targets:
            glob_targets.append(glob_target)
            cur_targets.append((self.world_to_frame(glob_target), end, weight))

        # вращение по z
        if self.freedom_z_angle is not None:
            self.calk_ik_on_plane_2(
                (vector.Vector(1, 0, 0), vector.Vector(0, 1, 0)),
                self.axis,
                self.freedom_z_angle,
                cur_targets)

        # вращение по y
        if self.freedom_y_angle is not None:
            self.calk_ik_on_plane_2(
                (vector.Vector(0, 0, 1), vector.Vector(1, 0, 0)),
                self.axis.cross(self.up),
                self.freedom_y_angle,
                cur_targets)

        # вращение по x
        if self.freedom_x_angle is not None:
            self.calk_ik_on_plane_2(
                (vector.Vector(0, 1, 0), vector.Vector(0, 0, 1)),
                self.up,
                self.freedom_x_angle,
                cur_targets)

        # рассчитаем кинематику для родителя
        if self.parent is not None and isinstance(
                self.parent, node.Node):
            data = [
                (g, self.parent.world_to_frame(
                    self.frame_to_world(t[1])), t[2])
                for g, t in zip(glob_targets, cur_targets)]
            self.parent.calk_ik_pos_2(data)

        return self.frame_to_world(end)

    def calk_ik_pos(self, glob_target, end=vector.Vector(0, 0, 0)):
        '''Рассчёт инверсной кинематики'''
        # print "calk_ik_pos(calk_ik_pos:{})".format(glob_target)

        # 1. переведём в локальную систему координат
        target = self.world_to_frame(glob_target)

        # вращение по z
        if self.freedom_z_angle is not None:
            self.calk_ik_on_plane((vector.Vector(1, 0, 0), vector.Vector(
                0, 1, 0)), self.axis, self.freedom_z_angle, target, end)

        # вращение по y
        if self.freedom_y_angle is not None:
            self.calk_ik_on_plane(
                (vector.Vector(0, 0, 1), vector.Vector(1, 0, 0)),
                self.axis.cross(self.up),
                self.freedom_y_angle,
                target,
                end)

        # вращение по x
        if self.freedom_x_angle is not None:
            self.calk_ik_on_plane((vector.Vector(0, 1, 0), vector.Vector(
                0, 0, 1)), self.up, self.freedom_x_angle, target, end)

        # рассчитаем инематику для родителя
        if self.parent is not None and isinstance(
                self.parent, node.Node):
            self.parent.calk_ik_pos(
                glob_target,
                self.parent.world_to_frame(self.frame_to_world(end)))

        return self.frame_to_world(end)

    def rotate_by_normal(self, plane, base_axis, freedom, global_normal):
        '''Сориентировать звено по проекции плоскости'''
        # 1. преобразуем global_normal нормаль в локальную
        if self.parent is not None and isinstance(
                self.parent, node.Node):
            normal = self.parent.world_to_frame(
                vector.Vector(0, 0, 0) + global_normal) -\
                self.parent.world_to_frame(vector.Vector(0, 0, 0))
        else:
            normal = global_normal

        # 2. найдём cross нормалей
        horizont = normal.cross(plane[0].cross(plane[1]))

        # найдём угол горизонта
        if horizont.mag > 0:
            angle = self.get_proj_angle(plane[0], plane[1], horizont)
            self.set_proj_angle(freedom, angle, plane[0], plane[1], base_axis)

    def rotate_by_normal_y(self, global_normal=vector.Vector(0, 1, 0)):
        self.rotate_by_normal(
            (vector.Vector(0, 0, 1), vector.Vector(1, 0, 0)),
            self.axis.cross(self.up),
            self.freedom_y_angle,
            global_normal)


###############################################################################
if __name__ == '__main__':
    from PyQt4 import QtGui
    from scene_view import SceneView
    import sys
    from sphere import sphere

    app = QtGui.QApplication(sys.argv)
    mainWin = SceneView()

    # координаты
    x_arrow = arrow(pos=(0, 0, 0), axis=(1, 0, 0), length=20,
                    shaftwidth=0.5, fixedwidth=True, color=(1, 0, 0))
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 1, 0), length=20,
                    shaftwidth=0.5, fixedwidth=True, color=(0, 1, 0))
    x_arrow = arrow(pos=(0, 0, 0), axis=(0, 0, 1), length=20,
                    shaftwidth=0.5, fixedwidth=True, color=(0, 0, 1))

    # создадим руку
    b1 = Bone(freedom_z_angle=(0, 2))
    b2 = Bone(parent=b1, pos=(20, 0, 0), freedom_z_angle=(0, 2))
    b3 = Bone(parent=b2, pos=(20, 0, 0), freedom_z_angle=(0, 2))
    b4 = Bone(parent=b3, pos=(20, 0, 0), freedom_z_angle=(0, 2))
    sp = sphere()

    # обработчик
    def on_cursor_move(camera, pos):
        global b4
        pos = camera.get_mouse_pos(pos, ((0, 0, 1), (0, 0, 0)))
        b4.calk_ik_pos(pos)
        sp.pos = pos

    mainWin.cursor_move.connect(on_cursor_move)
    mainWin.show()
    sys.exit(app.exec_())
