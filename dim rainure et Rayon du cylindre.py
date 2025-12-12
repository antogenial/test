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
eq4 = sp.Eq(k, r - sp.sqrt(r**2 - (h/2)**2))
syst_eq = [eq1, eq2, eq3, eq4]


syst_eq = se.Syst_eq(params, syst_eq)


# affichage
Title("Relations:")
syst_eq.print_definitions()
End_line()

# calcul
Title("Calcul:")
known1 = {"r": 105/2, "R":110/2, "h": 30}
longeur_renfort = known1["r"]/2
unknown1 = syst_eq.compute(syst_eq.definitions["k"][1], known1)#sp.solve(eq4, k)[0], known1)
print("k1 = s2 =", unknown1)
print("m2 = longeur_renfort - s2")
print(f"m2 = {longeur_renfort} - {unknown1}")
m2 = longeur_renfort - unknown1
print(f"{m2 = }") 



Title("Verif:")
known2 = {"R": known1["r"], "h": 30, "s": unknown1, "m":m2}
unknown2 = "r"
h_val = syst_eq.resolution(unknown2, known2)
if h_val is not None:
    h_val = round(h_val, decimal)

print("resut:", h_val)
print()




   
                
        
           
                
        
 

