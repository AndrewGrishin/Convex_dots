import funcs
import math
from functools import reduce
import sys
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt

if 0:
    funcs.generate(180,0,14)
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

# initialize the model and train it
pipe = funcs.regress(df,degreeOfRegression = 10)
# add a new column with predicted values
df["f'"] = [pipe.predict([[df["x0"][i]]])[0] for i in range(df.shape[0])]
df["(f-f')^2"] = (df["f"] - df["f'"])**2

# save chosen dots into the xlsx file
df.to_excel("output.xlsx")

#for ind,convex_hull in enumerate(convex_hulls):
#    print("Iteration: {}".format(ind))
#    for dot in convex_hull:
#        print(str(dot[0]) + "," + str(dot[1]))
#    print()

print("MES error ->",funcs.mes(f = df["f"], newf = df["f'"]))
print(df)

df.plot(x = "x0",y = ["f","f'"])
xArray, yArray = zip(*dots)
plt.scatter(xArray,yArray)
plt.show()

file.close()
del(file)
del(xArray)
del(yArray)
del(dots)
del(maxDotsValues)
del(functionCoefs)
del(task)

# scatter set of dots and plot OPTIMAL Selected dots
# write the algorithm to minimise the MES (by searching the lowest MES [0 up to when the MES(t) == MES(t - 1)])
# choose if it is usefull to use only 70% of all data to train the model and use other 30% to check the MES
# 
# check all points not in OPTIMAL ARRAY to fit the regression-curve
# (if values of Y varies less then EPSILON => add this point to the OPTIMAL ARRAY and add it to the plot)