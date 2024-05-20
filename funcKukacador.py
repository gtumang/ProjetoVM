import numpy as np

def calculaPosTelaC(u,v,Z,f,ro_h,ro_w)->list:
  x = ro_w*(u-320)*Z/f
  y = ro_h*(v-240)*Z/f
  return [x,y,Z]

def calculaPosKukaB(pos,mHom)->tuple:
  print(pos)
  posC = np.array(pos)
  print(posC)
  posB = np.matmul(mHom,posC)
  return posB
