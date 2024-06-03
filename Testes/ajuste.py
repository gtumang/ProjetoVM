import math

pos_x = (57.96082591, -1.57934635, -57.89615511)
erro_x = (-35, -25, -15)

m = (erro_x[0]-erro_x[2])/(pos_x[0]-pos_x[2])
print(m)
print()
