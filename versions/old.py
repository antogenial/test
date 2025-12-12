import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

# var and param (unité: mm)
decimal = 2
# R : le ryon exteriuer
r = list(range(105,111))#80, 90, 95] # rayon interieur
p = [3., 3.5, 4., 4.5, 5., 5.5]  # longeur du suport (a sa base)
# m : la longeur du suport (au milieux)
s = 7.5 # epaiseur min du cylindre (largeur au niveau de la rainure)
h = np.arange(0, 100, 10**(-decimal)) # hateur du suport / rainure
H = 30 # a choosen h

def R(x, r, p, rounding=False, returnParams=False):
    k = r - np.sqrt(r**2 +(x/2)**2)
    m = p + k
    d = m + s
    y = r + d
    #y = 2*r + p - np.sqrt(r**2 +(x/2)**2) + s
    if rounding:
        k = np.round(k, decimal)
        m = np.round(m, decimal)
        d = np.round(d, decimal)
        y =  np.round(y, decimal)
    if returnParams: 
        return y, {"k":k, "m":m, "d":d, "R":y}
    return y

def R_inv(y, r, p, rounding=False):
    x = 2 * np.sqrt((2*r + p + s - y)**2 - r**2)
    if rounding:
        return np.round(x, decimal)
    return x


# compute

y_min, y_max = np.min(R(h, min(r), min(p))), np.max(R(h, max(r), max(p)))
delta_img = y_max-y_min
y_bottom, y_top = y_min-(delta_img/20), y_max+(delta_img/20)
delta_y = y_top-y_bottom


# graph
#plt.axhline(y=RofH, xmin=0, xmax=H/h[-1], linestyle='--', color="grey", linewidth=0.5)
#plt.axvline(x=H, ymin=0, ymax=(RofH-y_min)/(y_max-y_min), linestyle='--', color="grey", linewidth=0.5)
#plt.plot(h, Rofh, label="R(h)")
#plt.plot(h, R_inv(h))
for i in r:
    for j in p:
        R1= R(h, i, j)
        plt.plot(h, R1, label=f"R(h, {i}, {j}, {s})")
        H = R_inv(120, i, j)
        #H = 30
        R2 = R(H, i, j)
        plt.plot(H, R2, "ro")#label=f"R({H})"
        plt.axhline(y=R2, xmin=0, xmax=H/h[-1], linestyle='--', color="grey", linewidth=0.5)
        plt.axvline(x=H, ymin=0, ymax=(R2-y_bottom)/delta_y, linestyle='--', color="grey", linewidth=0.5)
plt.xlim(h[0], h[-1])
plt.ylim(y_bottom, y_top)
plt.xlabel("h [mm]")
plt.ylabel("R [mm]")
plt.legend()
plt.show()
