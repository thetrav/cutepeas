from random import randint, random
import math

class Vector(object):
    __slots__ = ('x', 'y') 
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return '(%.1f,%.1f)' % (self.x, self.y)
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, o):
        return self.x == o.x and self.y == o.y
    
    def __cmp__(self, o):
        return self.__eq__(o)
    
    def __ne__(self, o):
        return not self.__eq__(o)
    
    def __hash__(self):
        return self.x + self.y * 10000
    
    def __lt__(self, o):
        if self.x < o.x:
            return True
        if self.y < o.y:
            return True
        
    def __add__(self, o):
        return Vector(self.x + o.x, self.y + o.y)
    
    def __sub__(self, o):
        return Vector(self.x - o.x, self.y - o.y)
    
    def __div__(self, o):
        return Vector(self.x / o, self.y / o)
    
    def __mul__(self, o):
        return Vector(self.x * o, self.y * o)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
#    def __getitem__(self, a):
#        if not a: return self.x
#        return self.y
#    def __setitem__(self, a, v):
#        if a == 0: self.x = v
#        if a == 1: self.y = v

    def length(self):
        return math.hypot(self.x, self.y)
    
    def normalise(self):
        length = math.hypot(self.x, self.y)
        self.x = self.x / length
        self.y = self.y / length
        
    @staticmethod
    def random(xrange,yrange):
        return Vector(randint(xrange[0], xrange[1]), randint(yrange[0], yrange[1]))
    @staticmethod
    def random_range(center, max_radius):
        a = random() * math.pi * 2
        r = random() * max_radius
        return Vector(center.x + math.cos(a) * r, center.y + math.sin(a) * r)
    @staticmethod
    def list(l):
        return Vector(l[0], l[1])
    def to_list(self):
        return [self.x, self.y]
if __name__ == '__main__':
    import timeit
    t = timeit.Timer('b = a.y', 'from Vector import Vector\na = Vector(5.3, 6.2)')
    print min(t.repeat(5, 1000000))
    # getitem is 10 times slower then attribute access!