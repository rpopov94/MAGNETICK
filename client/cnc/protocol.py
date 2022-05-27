from cnc.geomerty import Geometry


class Protocol(Geometry):
    
    def __init__(self, min_x=-1000, max_x=1000, min_y=-1000, max_y=1000, min_z=-1000, max_z=1000) -> None:
        Geometry.__init__(self, min_x, max_x, min_y, max_y, min_z, max_z)
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y
        self.max_z = max_z
        self.min_z = min_z
    
    '''Перемещение по xyz c к определенному положению'''
    def go_to_x(self, val):
        steps = self.goto_x(val)
        return [hex(int(c)) for c in f"gotox:{steps};"]

    def go_to_y(self, val):
        steps = self.goto_y(val)
        return [ord(c) for c in f"gotoy:{steps};"]
    
    def go_to_z(self, val):
        steps = self.goto_z(val)
        return [ord(c) for c in f"gotoz:{steps};"]

    '''Простое перемещение по xyz'''
    def move_x(self, steps, dir=1):
        if dir > 0:
            return [ord(c)for c in f"goxr:{steps};"]
        elif dir < 0:
            return [ord(c)for c in f"goxl:{steps};"]
        else:
            return None

    def move_y(self, steps, dir=1):
        if dir > 0:
            return [ord(c) for c in f"goyr:{steps};"]
        elif dir < 0:
            return [ord(c) for c in f"goyl:{steps};"]
        else:
            return None

    def move_z(self, steps, dir=1):
        if dir > 0:
            return [ord(c) for c in f"gozr:{steps};"]
        elif dir < 0:
            return [ord(c) for c in f"gozl:{steps};"]
        else:
            return None

    def stop(self):
        return [ord(c) for c in 'stop;']


    
