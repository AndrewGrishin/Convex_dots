import rnd_dots

#rnd_dots.generate()

def distance(dot, centre):
    return ((dot[0] - centre[0])**2 + ((dot[1] - centre[1])**2))**(0.5)

file = open("input_dots.txt","r")
dots = list(map(lambda s : tuple(map(float,iter(s.split(",")))),file))
file.close()
del(file)

x = [i[0] for i in dots]
y = [i[1] for i in dots]
print(sum(x),sum(y))
centre = (sum(x) / len(x), sum(y) / len(y))
del(x)
del(y)

#dots = list(map(lambda dot: dot,dots))
dots = sorted(dots, key = lambda dot : distance(dot, centre), reverse = 1)

def ru_er(dot, centre):
    return dot[0] > centre[0] and dot[1] > centre[1]
def rd_er(dot, centre):
    return dot[0] > centre[0] and dot[1] < centre[1]
def lu_er(dot, centre):
    return dot[0] < centre[0] and dot[1] > centre[1]
def ld_er(dot, centre):
    return dot[0] < centre[0] and dot[1] < centre[1]
def sorter(array,dot, func):
        if dot not in array and sum(1 for sub_dot in array if func(sub_dot,dot)) == 0:
            return 1
        else:
            return 0

dotsMatrix = [[],[],[],[]]

for dot in dots:
    if ru_er(dot,centre) and sorter(dotsMatrix[0],dot,func = ru_er):
        dotsMatrix[0].append(dot)
        continue
    if rd_er(dot,centre) and sorter(dotsMatrix[1],dot,func = rd_er):
        dotsMatrix[1].append(dot)
        continue
    if ld_er(dot,centre) and sorter(dotsMatrix[2],dot,func = ld_er):
        dotsMatrix[2].append(dot)
        continue
    if lu_er(dot,centre) and sorter(dotsMatrix[3],dot,func = lu_er):
        dotsMatrix[3].append(dot)
        continue

del(centre)
for line in dotsMatrix:
    print(line)
#del(dots)
#dotsMatrix = [j for i in dotsMatrix for j in i]

# - [ ] cover dots to fit the set
#   - [ ] using nearest neighbor
# - [ ] sort all selected dots clockwise
# - [ ] delete selected dots, to make the set convex
#   - [ ] check if the dot should be deleted, using “line. Compare ‘y’ coordinates

# use travelling sales man problem for the first step (and maybe second)
# import tsp module, input matrix of way (way - length between dots)
# then get the final matrix (array of steps to do)
# then use "line method to skip all useless points"