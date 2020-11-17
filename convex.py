import funcs
import math
from functools import reduce
import sys
import pandas as pd
import matplotlib.pyplot as plt

if 0:
    funcs.generate(100,0,90000)
    sys.exit(1)
# in the "input_dots.txt" first two lines MUST be "min" or "max" the task is and coefs of the function
# IN THIS ORDER!!!

file = open("input_dots.txt","r")
# the first line contains coefs of the function, everything else are dots of the initial set
functionCoefs, *dots = list(map(lambda line : list(map(lambda dot : float(dot),iter(line.split(",")))),file))

print(10,"%")

xArray, yArray = zip(*dots)
xAvg, yAvg = sum(xArray) / len(xArray), sum(yArray) / len(yArray)
dispersionX = (sum(map(lambda a: a * a,xArray)) / len(xArray) - xAvg * xAvg)**(0.5)
dispersionY = (sum(map(lambda a: a * a,yArray)) / len(yArray) - yAvg * yAvg)**(0.5)

# normalize all values of X and Y in dots array
# need for training model
dots = funcs.nomalizeXandY(dots)

print(20,"%")

optDotsValues, convex_hulls = funcs.maxConvexHullsDots(dots, functionCoefs, dispersionX, dispersionY, xAvg, yAvg)

# na = [[1,"a"],[2,"b"],[3,"c"]] -> zip(*na) -> [1,2,3] ["a","b","c"]
#xValuesArray, yValuesArray = zip(*maxDotsValues)
df = pd.DataFrame(optDotsValues)
df.columns = ["x" + str(i) for i in range(df.shape[1] - 1)] + ["f"]

print(40,"%")

df, degree = funcs.getTheBestDegreeOfRegression(df)

print("Polynomial degree is ->",degree)
print("MES error (normalized) ->",funcs.mes(f = df["f"], newf = df["f'"]))
print(70,"%")

# unnormalize all opt dots
df["x0"] = df["x0"] * dispersionX + xAvg
df["f"] = df["f"] * dispersionY + yAvg
df["f'"] = df["f'"] * dispersionY + yAvg
df["(f-f')^2 classic"] = (df["f"] - df["f'"])**2
print("MES error (unnormalized) ->",funcs.mes(f = df["f"], newf = df["f'"]))
# save chosen dots into the xlsx file
df.to_excel("output.xlsx")

print(90,"%")

funcs.plotResult(df)

file.close()
del(file)
del(xArray)
del(yArray)
del(dots)
del(optDotsValues)
del(functionCoefs)

print(100,"%")
# - [+] scatter set of dots and plot OPTIMAL Selected dot
# - [+] write the algorithm to minimise the MES (by searching the lowest MES [0 up to when the MES(t) == MES(t - 1)])
# - [] choose if it is usefull to use only 70% of all data to train the model and use other 30% to check the MES
# 
# - [+] IT DOES NOT MATTER WHAT THE PORBLEM IS (max or min) -> need to find max and min in on iteration (and add it into optimal array) -> 
# regression will give the trand-curve -> from the MIN point to MAX point in one time -> the further forcast would be more accurate
# 
# Все переменные были нормально распределены => нормализованы => нормальное распределение
# Логарифмировать все переменные => загнать множество в квадрат со стороными от 0 до 1.
# 
# Хи^2 => критерий согласия => на сколько мое распределение согласуется с нормальным распрделением => 
# if pi_value близок к 0 => империческое распрделение очень далеко от нормального распрделления (если больше 5% - это нормальное распределение => нормализация не нужна)
# (x - x(avg)) / sigma = стандартизация
# 
# Если нормализация нужна => логарифмическое распределение, полулогарифмическое, линейное - часто в экономике
# Есть другой вариант преобразования Бокса-Кокса. => подбирается лямбда, которая делает переменную нормальнно распрделенной
# (Можно в ручную, но каждый раз проверять критерий согласия с нормальным распрделением) => делать через while
# 
# 
# 
# 
