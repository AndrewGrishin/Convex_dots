import matplotlib.pyplot as plt
import time
import numpy as np

def distanceFromCenter(dot, centre):
    return ((dot[0] - centre[0])**2 + ((dot[1] - centre[1])**2))**(0.5)

file = open("input_dots.txt","r")
dots = list(map(lambda s : tuple(map(float,iter(s.split(",")))),file))

x = [i[0] for i in dots]
y = [i[1] for i in dots]
centre = (sum(x) / len(x), sum(y) / len(y))

dots = list(map(lambda dot: (dot, distanceFromCenter(dot,centre)),dots))
dots = sorted(dots, key = lambda dot : dot[1], reverse = 1)
