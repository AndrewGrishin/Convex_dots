import funcs
import tsp
import numpy as np

columns = 20

#funcs.generate(columns)

def distance(dot, centre):
    return ((dot[0] - centre[0])**2 + ((dot[1] - centre[1])**2))**(0.5)

file = open("input_dots.txt","r")
dots = list(map(lambda s : tuple(map(float,iter(s.split(",")))),file))
file.close()
del(file)

x,y,length = sum(i[0] for i in dots),sum(i[1] for i in dots),len(dots)
centre = (x / length, y / length)
del(x)
del(y)
del(length)

# tsp and line check -> time -> too long after 45 nodes
dotsDict = { (i,j) : distance(dots[i],dots[j]) if i != j else np.inf for i in range(len(dots)) for j in range(len(dots)) }
result = list(map(lambda ind : dots[ind],tsp.tsp(range(columns),dotsDict)[1]))
del(dotsDict)
del(dots)

def func(a,b,c):
    return lambda x,y : x * a + y * b + c

# rout, connecting all dots to the file "output_rout.txt"
file = open("output_rout.txt","w")
for ind,val in enumerate(result):
    dot1,dot2 = val,result[ind + 1] if ind != len(result) - 1 else result[0]
    a,b,c = funcs.returnCoefsOfLine(dot1,dot2)
    print(dot1,"->",dot2,":",(a,b,c), file = file)

    if dot1[1] >= centre[1] or dot2[1] >= centre[1]:
        if a == 0:
            # are there any dots above ?
            pass
        if b == 0 and (dot1[0] >= centre[0] or dot2[1] >= centre[0]):
            # are there any dots righter ?
            pass
        if b == 0 and (dot1[0] <= centre[0] or dot2[1] <= centre[0]):
            # are there any dots lefter ?
            pass
        if a > 0 and (dot1[0] >= centre[0] or dot2[1] >= centre[0]):
            # are there any dots above?
            pass
        
    else:
        pass

# Jarvice Wrapping

file.close()
del(file)
del(result)
del(centre)
