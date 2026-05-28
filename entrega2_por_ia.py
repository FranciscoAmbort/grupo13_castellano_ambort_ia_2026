import collections
from simpleai.search import CspProblem, backtrack

def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    """
    Resuelve el diseño del campamento base en Marte utilizando un CSP.
    
    camp_size: tupla (filas, columnas)
    habs, generators, labs, deposits, airlocks: enteros con las cantidades a ubicar
    craters: lista de tuplas (fila, columna)
    
    Retorna: Lista de tuplas (tipo, fila, columna) o None si no hay solución.
    """
    rows, cols = camp_size
    craters_set = set(craters)

    # ----------------------------------------------------
    # 1. Definición de Variables
    # ----------------------------------------------------
    # Creamos variables únicas para cada instancia de módulo individual
    variables = []
    
    hab_vars = [f"hab_{i}" for i in range(habs)]
    gen_vars = [f"gen_{i}" for i in range(generators)]
    lab_vars = [f"lab_{i}" for i in range(labs)]
    dep_vars = [f"dep_{i}" for i in range(deposits)]
    air_vars = [f"air_{i}" for i in range(airlocks)]
    
    variables.extend(hab_vars)
    variables.extend(gen_vars)
    variables.extend(lab_vars)
    variables.extend(dep_vars)
    variables.extend(air_vars)

    # Si no se pide ningún módulo, la solución es trivial (lista vacía)
    if not variables:
        return []

    # ----------------------------------------------------
    # 2. Definición de Dominios (Optimizados en origen)
    # ----------------------------------------------------
    def is_border(r, c):
        return r == 0 or r == rows - 1 or c == 0 or c == cols - 1

    # Todas las celdas de la grilla que no son cráteres
    all_valid_cells = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in craters_set]

    domains = {}
    for var in variables:
        tipo = var.split('_')[0]
        
        if tipo == "air":
            # Restricción 3: Esclusas solo en el borde
            domains[var] = [cell for cell in all_valid_cells if is_border(*cell)]
        elif tipo == "hab":
            # Restricción 4: Habitacionales solo al interior
            domains[var] = [cell for cell in all_valid_cells if not is_border(*cell)]
        else:
            domains[var] = list(all_valid_cells)

    # ----------------------------------------------------
    # 3. Funciones Auxiliares de Restricción
    # ----------------------------------------------------
    def are_adjacent(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

    def get_neighbors(pos):
        r, c = pos
        adj = []
        if r > 0: adj.append((r - 1, c))
        if r < rows - 1: adj.append((r + 1, c))
        if c > 0: adj.append((r, c - 1))
        if c < cols - 1: adj.append((r, c + 1))
        return adj

    # R1: Sin superposición (Binaria)
    def restr_no_overlap(variables_afectadas, values):
        return values[0] != values[1]

    # R5: Seguridad energética (Gen no adyacente a Hab)
    def restr_gen_hab(variables_afectadas, values):
        return not are_adjacent(values[0], values[1])

    # R6: Aislamiento entre generadores (Gen no adyacente a Gen)
    def restr_gen_gen(variables_afectadas, values):
        return not are_adjacent(values[0], values[1])

    # R7: Cadena de suministro científico (Lab adyacente a al menos un Dep)
    # Recibe la variable del laboratorio como primera posición y TODOS los depósitos después
    def restr_lab_dep(variables_afectadas, values):
        lab_pos = values[0]
        dep_positions = values[1:]
        return any(are_adjacent(lab_pos, dep_pos) for dep_pos in dep_positions)

    # R8: Ruta de evacuación (Hab necesita al menos una celda vecina ortogonal libre)
    # Recibe el Hab actual en la primera posición y absolutamente todas las DEMÁS variables después
    def restr_evacuacion_hab(variables_afectadas, values):
        hab_pos = values[0]
        otras_posiciones = set(values[1:])
        
        # Vecinos del habitacional dentro del mapa
        vecinos = get_neighbors(hab_pos)
        
        # Una celda está libre si no es cráter (ya filtrado en dominios) y no está ocupada por otra variable
        for v in vecinos:
            if v not in craters_set and v not in otras_posiciones:
                return True # Encontró al menos una salida libre
        return False

    # ----------------------------------------------------
    # 4. Construcción de las Restricciones del CSP
    # ----------------------------------------------------
    constraints = []

    # Combinaciones para evitar superposición (Todas las variables entre sí)
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            constraints.append(((variables[i], variables[j]), restr_no_overlap))

    # Restricciones de proximidad Gen-Hab
    for g_var in gen_vars:
        for h_var in hab_vars:
            constraints.append(((g_var, h_var), restr_gen_hab))

    # Restricciones de aislamiento Gen-Gen
    for i in range(len(gen_vars)):
        for j in range(i + 1, len(gen_vars)):
            constraints.append(((gen_vars[i], gen_vars[j]), restr_gen_gen))

    # Restricciones Lab-Dep (Cada lab acoplado a la lista completa de depósitos)
    if lab_vars:
        # Si hay laboratorios pero no depósitos, el caso es inmediatamente imposible
        if not dep_vars:
            return None
        for l_var in lab_vars:
            scope = [l_var] + dep_vars
            constraints.append((tuple(scope), restr_lab_dep))

    # Restricciones de Evacuación para cada Habitacional
    for h_var in hab_vars:
        # El alcance es el Hab actual seguido de todas las demás variables en el CSP
        otras_vars = [v for v in variables if v != h_var]
        scope = [h_var] + otras_vars
        constraints.append((tuple(scope), restr_evacuacion_hab))

    # ----------------------------------------------------
    # 5. Resolución del Problema
    # ----------------------------------------------------
    problem = CspProblem(variables, domains, constraints)
    solution = backtrack(problem)

    if solution is None:
        return None

    # Transformar el diccionario de la solución al formato requerido de salida
    formatted_solution = []
    for var, pos in solution.items():
        tipo = var.split('_')[0] # Extrae 'hab', 'gen', etc.
        formatted_solution.append((tipo, pos[0], pos[1]))

    return formatted_solution