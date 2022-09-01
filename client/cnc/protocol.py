from client.cnc.geomerty import Geometry


class Protocol(Geometry):

    def __init__(self, current_x, current_y, current_z, min_x=-1000, max_x=1000, min_y=-1000, max_y=1000, min_z=-1000,
                 max_z=1000, normalize=1) -> None:
        Geometry.__init__(self, current_x, current_y, current_z, min_x, max_x, min_y, max_y, min_z, max_z, normalize)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z
        self.current_x = current_x
        self.current_y = current_y
        self.current_z = current_z
        self.normalize=normalize

    '''Перемещение по xyz c к определенному положению
        - val: int - значению к текущему положению 
    '''

    def go_to_x(self, current, dir=1):
        self.set_x(current * self.normalize)
        steps = self.go_to(current, dir) * self.normalize
        return [ord(c) for c in f"gox:{steps};"]

    def go_to_y(self, current, dir=1):
        self.set_y(current * self.normalize)
        steps = self.go_to(current, dir) * self.normalize
        return [ord(c) for c in f"goy:{steps};"]

    def go_to_z(self, current, dir=1):
        self.set_z(current * self.normalize)
        steps = self.go_to(current, dir) * self.normalize
        return [ord(c) for c in f"goz:{steps};"]

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

    def move_x(self, steps, current, dir=1):
        if steps is not None:
            self.set_x(steps * self.normalize)
            if self.min_x <= current <= self.max_x:
                if dir > 0:
                    return [ord(c) for c in f"goxr:{steps * self.normalize};"]
                elif dir < 0:
                    return [ord(c) for c in f"goxl:{steps * self.normalize};"]
            elif self.min_x == current:
                if dir < 0:
                    print("Вы можете двигаться только в положительном направлении")
                return [ord(c) for c in f"goxr:{steps * self.normalize};"]
            elif current == self.max_x:
                if dir > 0:
                    print("Вы можете двигаться только в отрицательном направлении")
                return [ord(c) for c in f"goxl:{steps * self.normalize};"]
        return [ord(c) for c in f"goyl:{0};"]

    def move_y(self, steps, current, dir=1):
        if steps is not None:
            self.set_y(steps * self.normalize)
            if self.min_y <= current <= self.max_y:
                if dir > 0:
                    return [ord(c) for c in f"goyr:{steps * self.normalize};"]
                elif dir < 0:
                    return [ord(c) for c in f"goyl:{steps * self.normalize};"]
            elif self.min_y == current:
                if dir < 0:
                    print("Вы можете двигаться только в положительном направлении")
                return [ord(c) for c in f"goyr:{steps * self.normalize};"]
            elif current == self.max_y:
                if dir > 0:
                    print("Вы можете двигаться только в отрицательном направлении")
                return [ord(c) for c in f"goyl:{steps * self.normalize};"]
        return [ord(c) for c in f"goyl:{0};"]

    def move_z(self, steps, current, dir=1):
        if steps is not None:
            self.set_z(steps * self.normalize)
            if self.min_z <= current <= self.max_z:
                if dir > 0:
                    return [ord(c) for c in f"gozr:{steps * self.normalize};"]
                elif dir < 0:
                    return [ord(c) for c in f"gozl:{steps * self.normalize};"]
            elif self.min_z == current:
                if dir < 0:
                    print("Вы можете двигаться только в положительном направлении")
                return [ord(c) for c in f"gozr:{steps * self.normalize};"]
            elif current == self.max_z:
                if dir > 0:
                    print("Вы можете двигаться только в отрицательном направлении")
                return [ord(c) for c in f"gozl:{steps * self.normalize};"]
        return [ord(c) for c in f"gozl:{0};"]

    '''В начало координат'''
    def gotomax(self):
        self.set_x(self.max_x * self.normalize)
        return [ord(c) for c in 'gotomax;']

    def gotomin(self):
        self.set_x(self.min_x * self.normalize)
        return [ord(c) for c in 'gotomin;']

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
