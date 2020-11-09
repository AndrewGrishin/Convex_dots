import funcs
import math
from functools import reduce
import sys
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt

if 0:
    funcs.generate(16,0,16)
    sys.exit(1)
# in the "input_dots.txt" first two lines MUST be "min" or "max" the task is and coefs of the function
# IN THIS ORDER!!!

file = open("input_dots.txt","r")
# if the task is to MAX the Function => 1, else 0
task = 1 if next(file).replace("\n","") == "max" else 0
# the first line contains coefs of the function, everything else are dots of the initial set
functionCoefs, *dots = tuple(map(lambda line : tuple(map(lambda dot : float(dot),iter(line.split(",")))),file))

maxDotsValues, convex_hulls = funcs.maxConvexHullsDots(dots, task, functionCoefs)

# na = [[1,"a"],[2,"b"],[3,"c"]] -> zip(*na) -> [1,2,3] ["a","b","c"]
#xValuesArray, yValuesArray = zip(*maxDotsValues)

df = pd.DataFrame(maxDotsValues)
df.columns = ["x" + str(i) for i in range(df.shape[1] - 1)] + ["f"]
pipe = funcs.regress(df)
df["f'"] = [pipe.predict([[df["x0"][i]]])[0] for i in range(df.shape[0])]
df["(f-f')^2"] = (df["f"] - df["f'"])**2

for convex_hull in convex_hulls:
    print(convex_hull   )
print("MES error ->",df["(f-f')^2"].sum() / df.shape[0])
print(df)

df.to_excel("output.xlsx")

#df.plot(x = "x0",y = ["f","f'"])
#plt.show()

file.close()
del(file)
del(dots)
del(maxDotsValues)
del(functionCoefs)
del(task)

