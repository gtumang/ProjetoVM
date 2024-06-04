import numpy as np
from math import pi,sin,cos

def calculaPosTela(posImage)->list:
  img_x = 1.1817465091420418*posImage[0]-43.937802920365854
  img_y = 1.1363829502613019*posImage[1]-53.45218434265953
  return [img_x,img_y]

def calculaPosKukaB(posTelaH,mHom)->tuple:
  posT = np.array(posTelaH)
  posB = np.matmul(mHom,posT.T)
  posB_list = list(posB.copy())
  posB_list.pop(3)
  return posB_list

def image2kuka(imgPoint):
  DIST_Y_ROB = 865  # mm

  alpha = -pi/2


  H_tB = np.array([[1,     0,         0,        -60],
                 [0, cos(alpha), -sin(alpha), DIST_Y_ROB],
                 [0, sin(alpha), cos(alpha),   320],
                 [0,     0,         0,        1]])
  
  telaPoint = calculaPosTela(imgPoint)
  telaPoint.append(865)
  telaPoint.append(1)
  telaPointH = np.array(telaPoint)
  robPoint = calculaPosKukaB(telaPointH, H_tB)

  robPoint[1] = -200
  robPoint.append(0)
  robPoint.append(0)
  robPoint.append(-175)

  return robPoint
