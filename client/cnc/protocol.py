import os
import json
from cnc import conf, saveConfig
from cnc.geomerty import Geometry


class Protocol(Geometry):

    def __init__(self, current_x, current_y, current_z, min_x=-1000, max_x=1000, min_y=-1000, max_y=1000, min_z=-1000, max_z=1000, normalize=1) -> None:
        Geometry.__init__(self, min_x, max_x, min_y, max_y, min_z, max_z, normalize)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z
        self.current_x = current_x
        self.current_y = current_y
        self.current_z = current_z

    '''Перемещение по xyz c к определенному положению'''
    def go_to_x(self, val):
        steps = self.goto_x(val)
        return [ord(c) for c in f"gotox:{steps};"]

    def go_to_y(self, val):
        steps = self.goto_y(val)
        return [ord(c) for c in f"gotoy:{steps};"]
    
    def go_to_z(self, val):
        steps = self.goto_z(val)
        return [ord(c) for c in f"gotoz:{steps};"]

    '''Простое перемещение по xyz
        - перемещение происходит в пределах геометрии
        move_xyz(steps, dir=1)
        params:
        steps: количество шагов
        dir: Направление движения (1 по умолчанию)
            - > 0 положительное направление
            - < 0 отрицательное направление 
        return: bytearray
    '''

    def move_x(self, steps, dir=1):
        current = self.get_position_x()
        self.set_x(steps)
        if self.min_x <= current <= self.max_x:
            if dir > 0:
                return [ord(c)for c in f"goxr:{steps};"]
            elif dir < 0:
                return [ord(c)for c in f"goxl:{steps};"]
            else:
                return None
        elif self.min_x == current:
            if dir < 0:
                print("Вы можете двигаться только в положительном направлении")
            return [ord(c) for c in f"goxr:{steps};"]
        elif current == self.max_x:
            if dir > 0:
                print("Вы можете двигаться только в отрицательном направлении")
            return [ord(c) for c in f"goxl:{steps};"]

    def move_y(self, steps, dir=1):
        current = self.get_position_y()
        self.set_y(steps)
        if self.min_y <= current <= self.max_y:
            if dir > 0:
                return [ord(c) for c in f"goyr:{steps};"]
            elif dir < 0:
                return [ord(c) for c in f"goyl:{steps};"]
            else:
                return None
        elif self.min_y == current:
            if dir < 0:
                print("Вы можете двигаться только в положительном направлении")
            return [ord(c) for c in f"goyr:{steps};"]
        elif current == self.max_y:
            if dir > 0:
                print("Вы можете двигаться только в отрицательном направлении")
            return [ord(c) for c in f"goyl:{steps};"]

    def move_z(self, steps, dir=1):
        current = self.get_position_z()
        self.set_z(steps)
        if self.min_z <= current <= self.max_z:
            print(self.get_position_z())
            if dir > 0:
                return [ord(c) for c in f"gozr:{steps};"]
            elif dir < 0:
                return [ord(c) for c in f"gozl:{steps};"]
            else:
                return None
        elif self.min_z == current:
            if dir < 0:
                print("Вы можете двигаться только в положительном направлении")
            return [ord(c) for c in f"gozr:{steps};"]
        elif current == self.max_z:
            if dir > 0:
                print("Вы можете двигаться только в отрицательном направлении")
            return [ord(c) for c in f"gozl:{steps};"]

    '''Остановка всего'''
    def stop(self):
        return [ord(c) for c in 'stop;']

    '''Скорость/ускорение'''
    def set_speed(self, speed):
        '''
        speed: параметр скорости
        '''
        return [ord(c) for c in f"setsp:{speed};"]

    def set_acceleration(self, acceleration):
        '''
        acceleration: параметр ускорения
        '''
        return [ord(c) for c in f"setacc:{acceleration};"]

    def save_param(self, x, y, z):
        conf['current_x'] = x
        conf['current_y'] = y
        conf['current_z'] = z
        saveConfig(conf, 'coords.json')


    
