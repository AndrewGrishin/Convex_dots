import random

def generate():
    file = open("input_dots.txt","w")
    dots = set()

    while len(dots) <= 17:
        dots.add((random.randint(0,16),random.randint(0,16)))

    dots = list(dots)
    for dot in dots:
        print(str(dot[0]) + "," + str(dot[1]), file = file)

    file.close()
    del(dots)
    del(file)