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

def maxConvexHullsDots(dots, functionCoefs, dispX, dispY, avgX, avgY):
    maxDotsValues, minDotsValues = [], []
    # array to collect subconvex_hulls
    convex_hulls = []

    # get the function to find the value of the function in the current dot
    functionVal = findValueInDot(functionCoefs)

    ind = 0
    file = open("output_convex_hulls.txt","w")

    while len(dots) != 0:
        convex_hull = jarvis_march(dots)
        # save convex_hull just in case
        convex_hulls.append(convex_hull)
        #dot = max(convex_hull, key = functionVal) if task else min(convex_hull, key = functionVal)
        maxDot, minDot = max(convex_hull, key = functionVal), min(convex_hull, key = functionVal)

        if maxDot not in maxDotsValues and maxDot not in minDotsValues: maxDotsValues.append(maxDot)
        if minDot not in minDotsValues and minDot not in maxDotsValues: minDotsValues.append(minDot)
        # print current convex_hull to the file output_convex_hulls.txt
        # for dot in convex_hull:
        #     print(str(dot[0]) + "," + str(dot[1]), file = file)
        # print("\n",file = file)
        dots = tuple(set(map(tuple,dots)) - set(map(tuple,convex_hull)))

        # PRINT NUMBER of iterations and its dots
        print("Iteration",ind, file = file)
        for dot in convex_hull:
            print("{},{}".format(dot[0] * dispX + avgX,dot[1] * dispY + avgY), file = file)
        print(file = file)
        ind += 1

        del(convex_hull)
    minDotsValues.reverse()
    
    file.close()
    del(file)
    del(ind)
    return (maxDotsValues + minDotsValues,convex_hulls)

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
    
# train the model
def regress(df, degreeOfRegression, model = None):

    if model == None:
        # polynomial regression is 2 steps process
        # first -> transform data into polynomial ("PolynomicalFeaturs()")
        # second -> use Linear Regression
        # to automate this process -> use Pipelines
        # here creates steps of NonLinear Regression
        input = [("polynomial",PolynomialFeatures(degree = degreeOfRegression)), ("modal",LinearRegression())]
        # creates model "pipe", using these steps
        model = Pipeline(input)
        # creates a model with "self.df.shape[1] - 1" number of coeficents and one basis variable "f"
        # ASSUMPTION!!! it always will be the last column
        # train the model
    
    model.fit(df[list(df.columns)[0:-1:1]],df[list(df.columns)[-1]])
    return model

def mes(f,newf):
    import pandas as pd
    df = pd.DataFrame(zip(f,newf))
    return ((df[0] - df[1])**2).sum() / df.shape[0]

def nomalizeXandY(dots):
    xArray, yArray = zip(*dots)
    xAvg, yAvg = sum(xArray) / len(xArray), sum(yArray) / len(yArray)
    dispersionX = (sum(map(lambda a: a * a,xArray)) / len(xArray) - xAvg * xAvg)**(0.5)
    dispersionY = (sum(map(lambda a: a * a,yArray)) / len(yArray) - yAvg * yAvg)**(0.5)
    for ind,_ in enumerate(dots):
        dots[ind] = tuple(((dots[ind][0] - xAvg) / dispersionX,(dots[ind][1] - yAvg) / dispersionY))

    del(dispersionX)
    del(dispersionY)
    del(xAvg)
    del(yAvg)
    del(xArray)
    del(yArray)

    return dots

def getTheBestDegreeOfRegression(df):
    degree = 0
    # initialize the model and train it
    pipe = regress(df,degreeOfRegression = degree)
    # add a new column with predicted values
    df["f'"] = [pipe.predict([[df["x0"][i]]])[0] for i in range(df.shape[0])]

    mes0 = mes(f = df["f"], newf = df["f'"])
    mes1 = mes(f = df["f"], newf = df["f'"]) 

    while mes0 >= mes1:

        degree += 1

        del(df["f'"])

        # initialize the model and train it
        pipe = regress(df,degreeOfRegression = degree)
        # add a new column with predicted values
        df["f'"] = [pipe.predict([[df["x0"][i]]])[0] for i in range(df.shape[0])]

        mes0 = mes1
        mes1 = mes(f = df["f"], newf = df["f'"]) 

    del(df["f'"])
    # technical decent
    degree -= 1 
    # initialize the model and train it
    pipe = regress(df,degreeOfRegression = degree)
    # add a new column with predicted values
    df["f'"] = [pipe.predict([[df["x0"][i]]])[0] for i in range(df.shape[0])]
    df["(f-f')^2 normalized"] = (df["f"] - df["f'"])**2
    return (df,degree)

def plotResult(df):
    ax = plt.subplots()[1]
    df.plot(x = "x0",y = ["f","f'"], ax = ax)
    ax.scatter(df["x0"],df["f"])
    ax.scatter(df["x0"],df["f'"])
    # Don't allow the axis to be on top of your data
    ax.set_axisbelow(True)
    # Turn on the minor TICKS, which are required for the minor GRID
    ax.minorticks_on()
    # Customize the major grid
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    # Customize the minor grid
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()
