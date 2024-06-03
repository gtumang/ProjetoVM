import numpy as np

def calculaPosTelaC(u,v,Z,mtx,ro_h,ro_w,u0,v0)->list:
  fx = mtx[0][0]
  fy = mtx[1][1]
  cx = mtx[0][2]
  cy = mtx[1][2]

  print(fx,fy,cx,cy)

  x = (u-u0)*ro_w
  y = (v-v0)*ro_h

  print(x,y)

  X = (x-cx)*Z/fx
  Y = (y-cy)*Z/fy
  return [x,y,Z]

def calculaPosKukaB(pos,mHom)->tuple:
  print(pos)
  posC = np.array(pos)
  print(posC)
  posB = np.matmul(mHom,posC)
  return posB
