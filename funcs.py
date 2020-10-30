import matplotlib.pyplot as plt
import random
import numpy as np

def plotSet(result):
    for ind,_ in enumerate(result):
        plt.plot( \
            [result[ind][0],result[ind + 1 if ind != len(result) - 1 else 0][0]], \
            [result[ind][1],result[ind + 1 if ind != len(result) - 1 else 0][1]], \
            "ro-")
    plt.show()

def generate(n = 5):
    file = open("input_dots.txt","w")
    dots = set()

    while len(dots) < n:
        dot = (random.randint(0,16),random.randint(0,16))
        if dot not in dots:
            dots.add(dot)
            print(str(dot[0]) + "," + str(dot[1]), file = file)

    file.close()
    del(dots)
    del(file)

def returnCoefsOfLine(dot1,dot2):
    return (
            dot2[1] - dot1[1],
            dot1[0] - dot2[0],
            dot1[0] * dot2[1] - dot1[1] * dot2[0]
            )