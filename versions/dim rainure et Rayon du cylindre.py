import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import sympy as sp
import copy

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
w = sp.Symbol("w")
x = sp.Symbol("x")
y = sp.Symbol("y")
z = sp.Symbol("z")
params = [R, r, d, m, s, p, k, h, w, x, y, z]


# Équations
eq1 = sp.Eq(R, r + d+ w)
eq2 = sp.Eq(d, m + s)
eq3 = sp.Eq(m, p - k)
eq4 = sp.Eq(k, r - sp.sqrt(r**2 + (h/2)**2))
eq5 = sp.Eq(w, x + y -d)
eq6 = sp.Eq(y, 2*z)
syst_eq = [eq1, eq2, eq3, eq4, eq5, eq6]

# dictionnaire pour stocker toutes les définitions possibles
defs = {param.name: [] for param in params}

for eq in syst_eq:
    for param in params:
        if param in eq.free_symbols: # n'essaye de resoudre que si le param voulu est dans l'eq.
            try:
                sols = sp.solve(eq, param) # listes des solutuions
                for sol in sols:
                    if sol not in defs[param.name]:
                        defs[param.name].append(sol)
            except:
                pass

#function
def Title(text):
    print(f"\n\t"+ text +"\n")

def End_line(lenght=60):
    print(60*"_", end=2*"\n")

def get_param(param_name: str, params_list=params):
    for p in params_list:
        if p.name == param_name:
            return p

def scoring(eq, known_parameters):
    known_parameters = {get_param(key) for key in known_parameters}
    eq_used_param = eq.free_symbols
    eq_total_param = len(eq_used_param)
    nbr_available_param = len(known_parameters & eq_used_param) 
    if nbr_available_param == eq_total_param:
        nbr_available_param =  len(known_parameters)
    return nbr_available_param / eq_total_param

def matching_rate(x, y):
    pass

def compute(eq, known_parameters):
    resolved = eq.subs(known_parameters)
    return resolved.evalf()

def resolution(unknown, known_parameters, definitions=defs):
    print("unknown:", unknown)
    print("params:", set(known_parameters.keys()))
    if unknown in known_parameters:
        print(unknown, "allready know")
        return known_parameters[unknown]
    if unknown in definitions: # otherwise can't be resolve
        eqs = []
        unsolvable = []
        for i, eq in enumerate(definitions[unknown]):
            score = scoring(eq, known_parameters)
            eqs.append((eq, score, i))
            print(f"formula {i+1}:")
            print("    required parameters:", eq.free_symbols)
            print("    score :", score, end="")
            if score >= 1: # 100% know params
                print("  (> 1) -> direct compute of ", unknown)
                return compute(eq, known_parameters) # 1 equation in enought
            print()

        if len(eqs) == 0:
            print("No avaible definition for", unknown, "(e1)")
            

        while len(eqs) > 0:
            max_tuple = max(eqs, key=lambda x: x[1]) # start with the one that have the most params 
            best_def, max_score, formula_index = max_tuple
            print(f"Try to solv formula {formula_index+1} of {unknown}'s def")
            unknown_params = eq.free_symbols -  {get_param(key) for key in known_parameters}
            print("unknown_params:", unknown_params)
            # remove defs using the unknown (prevents infinit recursiv call)
            available_definitions = copy.deepcopy(definitions)
            for p, def_list in available_definitions.items():
                for d in def_list:
                    if get_param(unknown) in d.free_symbols:
                        available_definitions[p].remove(d)

            # resolve unknown_params
            for p in unknown_params:
                if p in unsolvable:
                    print(p, "has been declared insolvable") 
                    continue
                print("deeper layer: ", end="")
                p_val = resolution(p.name, known_parameters, available_definitions) # recursive call
                if p_val is not None:
                    known_parameters[p.name] = p_val
                    print(f"uper layer: unknown:", unknown)
                    continue
                else:
                    break
            if p_val is None: # unsolvable parameters -> unsovable unknow
                if not p in unsolvable:
                    print(f"uper layer: unknown:", unknown)
                unsolvable.append(p)
                eqs.remove(max_tuple)
                print("remaining formula:", len(eqs))
                continue
            new_score = scoring(best_def, known_parameters)
            if new_score >= 1:
                print("compute:", unknown)
                return compute(eq, known_parameters)
        if len(eqs) == 0:
            print("No avaible definition for", unknown, "(e3)")
            
            
    elif unknown not in definitions:
        print("No avaible definition for", unknown, "(e2)")


# affichage
Title("Relations:")
for key, val in defs.items():
    print(f"{key} : {val}")
End_line()


# test
# Cas 1 : résolvable avec paramètres explicites
Title("Test 1:")
known1 = {"d": 3, "r": 2}
unknown1 = "R"
R_val = resolution(unknown1, known1) 
if R_val is not None:
    R_val = round(R_val, decimal)
print("resut:", R_val)
print()
# Cas 2 : non résolvable avec paramètres explicites
Title("Test 2:")
known2 = {"r": 1, "m": 10}
unknown2 = "R"
k_val = resolution(unknown2, known2)
if k_val is not None:
    k_val = round(k_val, decimal)
print("resut:", k_val)
print()
# Cas 3 : résolvable avec paramètres implicites
Title("Test 3:")
known3 = {"m": 4, "s": 1, "k": 3}  # m + s = d ; k choisi cohérent avec r et h
unknown3 = "d"
d_val = resolution(unknown3, known3)
if d_val is not None:
    d_val = round(d_val, decimal)
print("resut:", d_val)
print()
# Cas 4 : non résolvable avec paramètres implicites
Title("Test 4:")
known4 = {"r": 10}#, "s": 1, "k": 1, "m": 2}  # incompatibilité avec h
unknown4 = "h"
h_val = resolution(unknown4, known4, defs)
if h_val is not None:
    h_val = round(h_val, decimal)
print("resut:", h_val)
print()
# Cas 5 : non résolvable avec paramètres implicites
Title("Test 5:")
known5 = {"r": 100, "p": 4, "h": 30 , "s": 5, "x": 0, "z": 0}
unknown5 = "R"
h_val = resolution(unknown5, known5, defs)
if h_val is not None:
    h_val = round(h_val, decimal)
print("resut:", h_val)
print()


                
                
        
           
                
        
 

