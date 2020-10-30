import funcs
import numpy as np

class Dot:
    def __init__(self,dot):
        self.x = dot[0]
        self.y = dot[1]

    def sub(self,dot):
        return Dot((self.x - dot[0], self.y - dot[1]))
    
def crossProduct(a,b):
    return a[0] * b[1] - a[1] * b[0]

def direction(a,b,c):
    return crossProduct(c.sub(a),b.sub(b))

def left(a,b,c):
    return direction(a,b,c) < 0

def right(a,b,c):
    return direction(a,b,c) > 0

def collinear(a,b,c):
    return direction(a,b,c) == 0

columns = 20
funcs.generate(columns)

# Jarvice Wrapping

file = open("input_dots.txt","r")
dots = list(map(lambda s : Dot(tuple(map(float,iter(s.split(","))))),file))
file.close()
del(file)


minYdot = dots[0]
for dot in dots:
    if minYdot.y >= dot.y:
        minYdot = dot

