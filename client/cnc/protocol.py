from client.cnc.geomerty import Geometry


class Protocol():

    def __init__(self, current_x, current_y, current_z, min_x, max_x, min_y, max_y, min_z,
                 max_z, normalize):
        self.current_x = current_x,
        self.current_y = current_y, 
        self.current_z = current_z, 
        self.min_x = min_x, 
        self.max_x = max_x, 
        self.min_y = min_y, 
        self.max_y = max_y, 
        self.min_z = min_z,
        self.max_z = max_z, 
        self.normalize = normalize

    """
        Рассчет шагов к конкретному положению
    """
    def go_to(self, current, max_c, min_c, dir=1):
        steps = 0
        if min_c <= current <= max_c:
            if dir > 0:
                steps = max_c - current
            elif dir < 0:
                steps = -1 * (current - min_c)
        return steps
        

    '''
        Перемещение по xyz c к определенному положению
        - val: int - значению к текущему положению 
    '''

    def go_to_x(self, current, dir=1):
        self.set_x(current * self.normalize)
        steps = self.go_to(current, self.max_x[0], self.min_x[0], dir) * self.normalize
        return [ord(c) for c in f"gox:{steps};"]

    def go_to_y(self, current, dir=1):
        self.set_y(current * self.normalize)
        steps = self.go_to(current, self.max_y[0], self.min_y[0], dir) * self.normalize
        return [ord(c) for c in f"goy:{steps};"]

    def go_to_z(self, current, dir=1):
        steps = self.go_to(current, self.max_z[0], self.min_z[0], dir) * self.normalize
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

    def move_x(self, steps, dir=1):
        if steps is not None:
            if dir < 0:
                return [ord(c) for c in f"goxl:{steps * self.normalize};"]
            else:
                return [ord(c) for c in f"goxr:{steps * self.normalize};"]
        self.stop()

    def move_y(self, steps, dir=1):
        if steps is not None:
            if dir < 0:
                return [ord(c) for c in f"goyl:{steps * self.normalize};"]
            else:
                return [ord(c) for c in f"goyr:{steps * self.normalize};"]
        self.stop()

    def move_z(self, steps, dir=1):
        if steps is not None:
            if dir < 0:
                return [ord(c) for c in f"gozl:{steps * self.normalize};"]
            else:
                return [ord(c) for c in f"gozr:{steps * self.normalize};"]    
        self.stop()

    '''В начало координат'''

    def gotomax(self):
        return [ord(c) for c in 'gotomax;']

    def gotomin(self):
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
