import pickle
import json


class Geometry:

    def __init__(self, min_x=0, max_x=1000, min_y=0, max_y=1000, min_z=0, max_z=1000, NORMALIZE=1) -> None:

        """Инициализация геометрии"""
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y
        self.max_z = max_z
        self.min_z = min_z
        self.current_x = None
        self.current_y = None
        self.current_z = None
        self.NORMALIZE = NORMALIZE
        self.temp = None

    def set_geometry(self, **kwargs) -> None:
        self.max_x = kwargs['max_x']
        self.min_x = kwargs['min_x']
        self.max_y = kwargs['max_y']
        self.min_y = kwargs['min_y']
        self.max_z = kwargs['max_z']
        self.min_z = kwargs['min_z']

    '''Получить текущие координаты'''

    def get_position_x(self) -> float:
        return self.current_x

    def get_position_y(self) -> float:
        return self.current_y

    def get_position_z(self) -> float:
        return self.current_z

    '''Установить координаты'''

    def set_x(self, pos):
        self.current_x = pos

    def set_y(self, pos):
        self.current_y = pos

    def set_z(self, pos):
        self.current_z = pos

    '''Переместиться к положению'''

    def goto_x(self, pos) -> float:
        steps = None
        if pos < self.min_x:
            steps = self.min_x - pos
            self.set_x(self.min_x)
            return steps
        elif pos > self.max_x:
            steps = pos - self.max_x
            self.set_x(self.max_x)
            return steps * -1
        elif self.min_x <= pos <= self.max_x:
            self.set_x(pos)
            if pos < self.current_x:
                steps = self.min_x - pos
                self.set_x(steps)
                return steps
            elif pos > self.current_x:
                steps = pos - self.current_x
                self.set_x(pos)
                return steps
        else:
            return 0

    def goto_y(self, pos) -> float:
        steps = None
        if pos < self.min_y:
            steps = self.min_y - pos
            self.set_y(self.min_y)
            return steps
        elif pos > self.max_y:
            steps = pos - self.max_y
            self.set_y(self.max_y)
            return steps * -1
        elif self.min_y <= pos <= self.max_y:
            self.set_y(pos)
            if pos < self.current_y:
                steps = self.min_y - pos
                return steps
            elif pos > self.current_y:
                steps = pos - self.current_y
                return steps
        else:
            return 0

    def goto_z(self, pos) -> float:
        steps = None
        if pos < self.min_z:
            steps = self.min_z - pos
            self.set_z(self.min_z)
            return steps * self.NORMALIZE
        elif pos > self.max_z:
            steps = pos - self.max_z
            self.set_x(self.max_z)
            return steps * -1
        elif self.min_z <= pos <= self.max_z:
            self.set_z(pos)
            if pos < self.current_z:
                steps = self.min_z - pos
                self.set_z(steps)
                return steps
            elif pos > self.current_z:
                steps = pos - self.current_z
                return steps
        else:
            return 0
