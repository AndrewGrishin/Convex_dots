import matplotlib.pyplot as plt
import random
# from scipy.spatial import ConvexHull
from functools import reduce
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

# (0,15) -> (12,16)

def plotSet(result, dots):
    for ind,_ in enumerate(result):
        plt.plot([result[ind][0],result[(ind + 1) % len(result)][0]],\
                 [result[ind][1],result[(ind + 1) % len(result)][1]],\
            "ro-")
    xArray = [xAxes[0] for xAxes in dots]
    yArray = [yAxes[1] for yAxes in dots]
    plt.scatter(xArray,yArray)
    del(xArray)
    del(yArray)
    plt.show()

# define lambda function to find the value of the function in the certain dot
def findValueInDot(functionCoefs):
    def f(dot):
        return reduce(lambda a,b : a + b,map(lambda a : a[0] * a[1],zip(dot,functionCoefs)))
    return f

def maxConvexHullsDots(dots, task, functionCoefs):
    maxDotsValues = []
    # array to collect subconvex_hulls
    convex_hulls = []

    # get the function to find the value of the function in the current dot
    functionVal = findValueInDot(functionCoefs)
    ind = 0
    while len(dots) != 0:
        convex_hull = jarvis_march(dots)
        # save convex_hull just in case
        convex_hulls.append(convex_hull)
        #dot = max(convex_hull, key = functionVal) if task else min(convex_hull, key = functionVal)
        maxDotsValues.append(max(convex_hull, key = functionVal) if task else min(convex_hull, key = functionVal))
        # print current convex_hull
        # for dot in convex_hull:
            # print(str(dot[0]) + "," + str(dot[1]))
        # print()
        dots = list(set(map(tuple,dots)) - set(map(tuple,convex_hull)))

        print("Iteration",ind)
        for dot in convex_hull:
            print("{},{}".format(dot[0],dot[1]))
        print()
        ind += 1
        del(convex_hull)

    return (maxDotsValues,convex_hulls)

def generate(n,a,b):
    file = open("input_dots.txt","w")
    dots = set()
    c,d = max(a,b),min(a,b)

    while len(dots) < n:
        dot = (random.randint(d,c),random.randint(d,c))
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

def direction(p, q, r):
    number = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if (number == 0): return 0
    return 1 if number > 0 else 2

def jarvis_march(dotsArray):

    # form convex hull
    l = dotsArray.index(min(dotsArray, key = lambda dot: dot[1]))
    convex_hull = [dotsArray[l]]

    # first iteration to make p != l
    p = l
    q = (p + 1) % len(dotsArray)
    for ind in range(len(dotsArray)):
        if (direction(dotsArray[p],dotsArray[ind],dotsArray[q]) == 2):
            q = ind
    p = q # by this line we do p != l and let the main loop works

    # other iterations
    while (p != l):
        convex_hull.append(dotsArray[p])
        q = (p + 1) % len(dotsArray)
        for ind in range(len(dotsArray)):
            if (direction(dotsArray[p],dotsArray[ind],dotsArray[q]) == 2):
                q = ind
        p = q  

    # add colinear points to the convex hull
    convex_hull2 = convex_hull[:]
    for ind in range(len(convex_hull)):
        a,b,c = returnCoefsOfLine(convex_hull[ind],convex_hull[(ind + 1) % len(convex_hull)])

        for dot in dotsArray:
            if dot == convex_hull[ind] or dot == convex_hull[(ind + 1) % len(convex_hull)]: continue
            if a * dot[0] + b * dot[1] == c: convex_hull2.append(dot)

    del(convex_hull)
    #del(p)
    #del(q)
    #del(l)
    return convex_hull2
    
# trains the model
def regress(df, degreeOfRegression = 3):
    # polynomial regression is 2 steps process
    # first -> transform data into polynomial ("PolynomicalFeaturs()")
    # second -> use Linear Regression
    # to automate this process -> use Pipelines
    # here creates steps of NonLinear Regression
    input = [("polynomial",PolynomialFeatures(degree = degreeOfRegression)), ("modal",LinearRegression())]
    # creates model "pipe", using these steps
    pipe = Pipeline(input)
    # creates a model with "self.df.shape[1] - 1" number of coeficents and one basis variable "f"
    # ASSUMPTION!!! it always will be the last column
    # train the model
    pipe.fit(df[list(df.columns)[0:-1:1]],df[list(df.columns)[-1]])
    return pipe

def mes(f,newf):
    import pandas as pd
    df = pd.DataFrame(zip(f,newf))
    return ((df[0] - df[1])**2).sum() / df.shape[0]


