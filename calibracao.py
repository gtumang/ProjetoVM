from sklearn.metrics import mean_squared_error, r2_score
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
import cv2 as cv
import imageProc
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
import pandas as pd

DIST_X_MM = 880
DIST_Y_MM = 492


imagePoints = [(41.264610290527344, 46.855491638183594), (84.14583587646484, 47.1357536315918),
               (126.93546295166016, 46.61134719848633), (39.470001220703125, 87.5546646118164), (82.65890502929688, 88.74637603759766), (125.48236083984375, 87.98776245117188), (37.778141021728516, 129.0103302001953), (81.37162780761719, 129.9384765625), (123.58495330810547, 130.00584411621094), (79.67622375488281, 173.16761779785156)]

worldPoints = [(0, 0), (50, 0), (100, 0),
               (0, 50), (50, 50), (100, 50), (0, 100), (50, 100), (100, 100), (50, 150)]

X_image = [x[0] for x in imagePoints]
X_world = [y[0] for y in worldPoints]

Y_image = [x[1] for x in imagePoints]
Y_world = [y[1] for y in worldPoints]

X_dict = {'X': X_image, 'Y': X_world}
Y_dict = {'X': Y_image, 'Y': Y_world}

df_x = pd.DataFrame(X_dict)
df_y = pd.DataFrame(Y_dict)
print(df_x)


# find line of best fit
a_x, b_x = np.polyfit(df_x['X'], df_x['Y'], 1)
a_y, b_y = np.polyfit(df_y['X'], df_y['Y'], 1)

print(f"X: {a_x}x+{b_x}")
print(f"Y: {a_y}x+{b_y}")

fig = plt.figure(figsize=(16, 9))

fig.add_subplot(1, 2, 1)
plt.title('X image x world')
plt.scatter(df_x['X'], df_x['Y'])
plt.plot(df_x['X'], a_x*df_x['X']+b_x)

fig.add_subplot(1, 2, 2)
plt.title('Y image x world')
plt.scatter(df_y['X'], df_y['Y'])
plt.plot(df_y['X'], a_y*df_y['X']+b_y)

plt.show()
