from sklearn.metrics import mean_squared_error, r2_score
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
import cv2 as cv
import lib.imageProc as imageProc
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
import pandas as pd

DIST_X_MM = 880
DIST_Y_MM = 492

# [(480.5, 229.0), (417.5555419921875, 223.94606018066406)]

imagePoints = [(41.264610290527344, 46.855491638183594), (84.14583587646484, 47.1357536315918),
               (126.93546295166016, 46.61134719848633), (39.470001220703125, 87.5546646118164), (82.65890502929688, 88.74637603759766), (125.48236083984375, 87.98776245117188), (37.778141021728516, 129.0103302001953), (81.37162780761719, 129.9384765625), (123.58495330810547, 130.00584411621094), (79.67622375488281, 173.16761779785156), (82.53385162353516, 66.46875), (167.96585083007812, 67.5243911743164), (251.9176788330078, 67.47514343261719), (335.5308532714844, 65.99056243896484), (419.5305480957031, 67.92684936523438), (78.45093536376953, 151.0478515625), (162.53170776367188, 152.96829223632812), (249.07315063476562, 156.46945190429688), (336.3485412597656, 159.55935668945312), (422.3958740234375, 162.58047485351562), (66.65210723876953, 237.3938751220703), (155.89810180664062, 239.0), (246.4439697265625, 240.94180297851562), (334.5317077636719, 241.03170776367188), (419.0950012207031, 244.5)]

worldPoints = [(0, 0), (50, 0), (100, 0),
               (0, 50), (50, 50), (100, 50), (0, 100), (50, 100), (100, 100), (50, 150), (52, 20),(152,20),(252,20),(352,20),(452,20),(52,120),(152,120),(252,120),(352,120),(452,120),(52,220),(152,220),(252,220),(352,220),(452,220)]

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
