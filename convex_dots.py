def distanceFromCenter(dot, centre):
    return ((dot[0] - centre[0])**2 + ((dot[1] - centre[1])**2))**(0.5)

file = open("input_dots.txt","r")
dots = list(map(lambda s : tuple(map(float,iter(s.split(",")))),file))
file.close()
del(file)

x = [i[0] for i in dots]
y = [i[1] for i in dots]
centre = ((sum(x) / len(x), sum(y) / len(y)),0)
del(x)
del(y)

dots = list(map(lambda dot: (dot, distanceFromCenter(dot,centre[0])),dots))
dots = sorted(dots, key = lambda dot : dot[1], reverse = 1)

def ru_er(dot, centre):
    return dot[0][0] >= centre[0][0] and dot[0][1] >= centre[0][1]
def rd_er(dot, centre):
    return dot[0][0] >= centre[0][0] and dot[0][1] <= centre[0][1]
def lu_er(dot, centre):
    return dot[0][0] <= centre[0][0] and dot[0][1] >= centre[0][1]
def ld_er(dot, centre):
    return dot[0][0] <= centre[0][0] and dot[0][1] <= centre[0][1]

ru = []
rd = []
lu = []
ld = []

for dot in dots:
    if ru_er(dot,centre):
        if dot not in ru:
            k = 0
            for sub_dot in ru:
                if ru_er(sub_dot,dot):
                    k += 1
            if k == 0:
                ru.append(dot)
    elif rd_er(dot,centre):
         if dot not in rd:
            k = 0
            for sub_dot in rd:
                if rd_er(sub_dot,dot):
                    k += 1
            if k == 0:
                rd.append(dot)
    elif ld_er(dot,centre):
        if dot not in ld:
            k = 0
            for sub_dot in ld:
                if ld_er(sub_dot,dot):
                    k += 1
            if k == 0:
                ld.append(dot)
    else:
        if dot not in lu:
            k = 0
            for sub_dot in lu:
                if lu_er(sub_dot,dot):
                    k += 1
            if k == 0:
                lu.append(dot)

print("Right-Up",ru)
print("Right-Down",rd)
print("Left-Down",ld)
print("Left-Up",lu)
