import SystEq as se
import sympy as sp


def Title(text):
    print(f"\n\t"+ text +"\n")

def End_line(lenght=60):
    print(lenght*"_", end=2*"\n")


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


# Équations
eq1 = sp.Eq(R, r + d)
eq2 = sp.Eq(d, m + s)
eq3 = sp.Eq(m, p - k)
eq4 = sp.Eq(k, r - sp.sqrt(r**2 + (h/2)**2))
syst_eq = [eq1, eq2, eq3, eq4]


syst_eq = se.Syst_eq(params, syst_eq)


# affichage
Title("Relations:")
syst_eq.print_definitions()
End_line()


# test
# Cas 1 : résolvable avec paramètres explicites
Title("Test 1:")
known1 = {"d": 3, "r": 2}
unknown1 = "R"
R_val = syst_eq.resolution(unknown1, known1)
if R_val is not None:
    R_val = round(R_val, decimal)
print("resut:", R_val)
print()
# Cas 2 : non résolvable avec paramètres explicites
Title("Test 2:")
known2 = {"r": 1, "m": 10}
unknown2 = "R"
k_val = syst_eq.resolution(unknown2, known2)
if k_val is not None:
    k_val = round(k_val, decimal)
print("resut:", k_val)
print()
# Cas 3 : résolvable avec paramètres implicites
Title("Test 3:")
known3 = {"m": 4, "s": 1, "k": 3}  # m + s = d ; k choisi cohérent avec r et h
unknown3 = "d"
d_val = syst_eq.resolution(unknown3, known3)
if d_val is not None:
    d_val = round(d_val, decimal)
print("resut:", d_val)
print()
# Cas 4 : non résolvable avec paramètres implicites
Title("Test 4:")
known4 = {"r": 10}#, "s": 1, "k": 1, "m": 2}  # incompatibilité avec h
unknown4 = "h"
h_val = syst_eq.resolution(unknown4, known4)
if h_val is not None:
    h_val = round(h_val, decimal)
print("resut:", h_val)
print()
# Cas 5 : non résolvable avec paramètres implicites
Title("Test 5:")
known5 = {"r": 100, "p": 4, "h": 30 , "s": 5, "x": 0, "z": 0}
unknown5 = "R"
h_val = syst_eq.resolution(unknown5, known5)
if h_val is not None:
    h_val = round(h_val, decimal)
print("resut:", h_val)
print()
