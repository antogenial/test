import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import sympy as sp

# var. et param. (unité: mm)
decimal = 2
R = sp.Symbol("R") # rayon exteriuer
r = sp.Symbol("r") # rayon interieur
d = sp.Symbol("d") # rayon interieur
m = sp.Symbol("m") # m : la longeur du suport (au milieux)
s = sp.Symbol("s") # epaiseur min du cylindre (largeur au niveau de la rainure)
p = sp.Symbol("p") # longeur du suport (a sa base)
k = sp.Symbol("k") # dif. entre m et p
h = sp.Symbol("h") # hateur du suport / rainure
params = [R, r, d, m, s, p, k, h]

# équations
def_R = sp.Eq(R, r + d)
def_d = sp.Eq(d, m + s)
def_m = sp.Eq(m, p - k)
def_k = sp.Eq(k, r - (r**2 + (h/2)**2)**(1/2))
syst_eq = (eq1, eq2, eq3, eq4)
sols_dict = {param.name: sp.solve(syst_eq, param, dict=True) for param in params}


for key, val in sols_dict:
    print(key, ":", val, end=2*"\n")
    

# numerics
params = {"r": 105, "p": 4, "s": 7.5, "h": np.arange(0, 100, 10**(-decimal))} 

