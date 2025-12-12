import SystEq as se
import sympy as sp


def Title(text):
    print(f"\n\t"+ text +"\n")

def End_line(lenght=60):
    print(lenght*"_", end=2*"\n")


# var. et param. (unité: mm)
decimal = 2
r = sp.Symbol("r") # rayon du cylindre
M = sp.Symbol("M") # petite diagonal, distance maximal bord cylindre: distance corner-cylindre,
m = sp.Symbol("m") # distance minimal bord-cylindre
D = sp.Symbol("D") # grande diagonal, diagonal face du cube
d = sp.Symbol("d") # diagonal du comprtiment moteur
H = sp.Symbol("H") # hauteur / longeur du cube
h = sp.Symbol("h") # hateur du compartiment moteur
l = sp.Symbol("l") # longeur du compartiment moteur
a = sp.Symbol("a") # alpha: l'angle avec la vertical de la diagonal d

params = [r, M, m, D, d, H, h, l, a]


# Équations
eq1 = sp.Eq(H, 2*(r+m))
eq2 = sp.Eq(d, (l*l + h*h)**0.5)
eq3 = sp.Eq(D, H*(2**0.5))
eq4 = sp.Eq(D, 2*(r+M))
eq5 = sp.Eq(l, r*sp.cos(a) + m)
eq6 = sp.Eq(h, r*sp.sin(a) + m)
eq7 = sp.Eq(l, h*sp.tan(a))
eq8 = sp.Eq(sp.sin(a), h/d)
eq9 = sp.Eq(sp.cos(a), l/d)
syst_eq = [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9]


syst_eq = se.Syst_eq(params, syst_eq)


# affichage
Title("Relations:")
syst_eq.print_definitions()
End_line()


# test
# Cas 1 : résolvable avec paramètres explicites
Title("Test 1:")
known1 = {"H": 140, "r": 110 ,"l": 28}

if 1:
#for p in params:
    p = d
    print(p.name, ":", syst_eq.resolution(p.name, known1, printProgress=1)[0])
    print()
