import sympy as sp
import copy


class Syst_eq:
    def __init__(self, params_list: list, eqs_list: list):
        self.syst_eq = eqs_list
        self.params = params_list
        self.definitions = None
        self.solve_system_for_params_expressions()
        

    def get_param_by_name(self, param_name: str):
        for p in self.params:
            if p.name == param_name:
                return p

    def  solve_system_for_params_expressions(self):
        # dictionnaire pour stocker toutes les définitions possibles
        self.definitions = {param.name: [] for param in self.params}
        for eq in self.syst_eq:
            for param in self.params:
                if param in eq.free_symbols: # n'essaye de resoudre que si le param voulu est dans l'eq.
                    try:
                        sols = sp.solve(eq, param) # listes des solutuions
                        #if sols not in self.definitions[param.name]:
                        #    self.definitions[param.name].append(sols)
                        for sol in sols:
                            if sol not in self.definitions[param.name]:
                                self.definitions[param.name].append(sol)
                    except:
                        pass

    def scoring(self, eq, known_parameters):
        known_parameters = {self.get_param_by_name(key) for key in known_parameters}
        eq_used_param = eq.free_symbols
        eq_total_param = len(eq_used_param)
        nbr_available_param = len(known_parameters & eq_used_param) 
        if nbr_available_param == eq_total_param:
            nbr_available_param =  len(known_parameters)
        return eq_total_param - nbr_available_param #nbr_available_param / eq_total_param


    def matching_rate(self, x, y):
        pass

    def print_definitions(self, definitions=None):
        if definitions is None:
            definitions = self.definitions
        for key, val in definitions.items():
            print(f"{key} : {val}")
            
    def get_available_definitions(self, unknown, definitions):
        #print("before selection :")
        #self.print_definitions(definitions)
        available_definitions = {}
        for param, def_list in copy.deepcopy(definitions).items():
            available_definitions[param] = []
            for d in def_list:
                if self.get_param_by_name(unknown) not in d.free_symbols:
                    available_definitions[param].append(d)
                #else:
                #    print(f"remove def: {param} = {d}")
        #print("selection:")
        #self.print_definitions(available_definitions)
        return available_definitions

    def compute(self, eq, known_parameters):
        resolved = eq.subs(known_parameters)
        return resolved.evalf()

    def resolution(self, unknown, known_parameters, definitions=None, printProgress=True):
        known_parameters = known_parameters.copy()
        # default value
        if definitions is None:
            definitions = self.definitions

        if printProgress:
            print("unknown:", unknown)
            print("params:", set(known_parameters.keys()))

        # case of known "unknown"
        if unknown in known_parameters:
            if printProgress:
                print(unknown, "allready know")
            return known_parameters[unknown], known_parameters

        # remove cyclique way
        definitions = self.get_available_definitions(unknown, definitions)

        # main solveur part
        if unknown in definitions: # otherwise can't be resolve
            eqs = []
            unsolvable = []
            # evalue the ways
            for i, eq in enumerate(definitions[unknown]):
                score = self.scoring(eq, known_parameters)
                eqs.append((eq, score, i))
                if printProgress:
                    print(f"formula {i+1}:")
                    print("    required parameters:", eq.free_symbols)
                    print("    score :", score, end="")
                if score <= 0: #score >= 1: # 100% know params
                    if printProgress:
                        print("  (< 0) -> direct compute of ", unknown)
                    return self.compute(eq, known_parameters), known_parameters # 1 equation in enought
                if printProgress:
                    print()

            if len(eqs) == 0:
                if printProgress:
                    print("No avaible definition for", unknown, "(e1)")
                
            # solving tree / recursive loop
            while len(eqs) > 0:
                min_tuple = min(eqs, key=lambda x: x[1]) # start with the one that have the most params 
                best_def, min_score, formula_index = min_tuple
                if printProgress:
                    print(f"Try to solv formula {formula_index+1} of {unknown}'s def")
                unknown_params = eq.free_symbols -  {self.get_param_by_name(key) for key in known_parameters}
                if printProgress:
                    print("unknown_params:", unknown_params)

                # resolve unknown_params
                for p in unknown_params:
                    if p in unsolvable:
                        if printProgress:
                            print(p, "has been declared insolvable")
                        continue
                    if printProgress:
                        print("deeper layer: ", end="")
                    p_val, known_parameters = self.resolution(p.name, known_parameters, definitions, printProgress) # recursive call
                    if p_val is not None:
                        known_parameters[p.name] = p_val
                        if printProgress:
                            print(f"uper layer: unknown:", unknown)
                        continue
                    else:
                        break
                if p_val is None: # unsolvable parameters -> unsovable unknow
                    if not p in unsolvable:
                        if printProgress:
                            print(f"uper layer: unknown:", unknown)
                    unsolvable.append(p)
                    eqs.remove(max_tuple)
                    if printProgress:
                        print("remaining formula:", len(eqs))
                    continue
                new_score = self.scoring(best_def, known_parameters)
                if new_score <= 0:
                    if printProgress:
                        print("compute:", unknown)
                    return self.compute(eq, known_parameters), known_parameters
            if len(eqs) == 0:
                if printProgress:
                    print("No avaible definition for", unknown, "(e3)")
                
                
        elif unknown not in definitions:
            if printProgress:
                print("No avaible definition for", unknown, "(e2)")
        return None, known_parameters

