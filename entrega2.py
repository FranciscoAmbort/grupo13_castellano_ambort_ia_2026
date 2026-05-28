
from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
)

def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters): 
    filas,columnas= camp_size
    crateres_sets= set(craters)
    variables_hab = [f"hab_{i}" for i in range(habs)]
    variables_gen = [f"gen_{i}" for i in range(generators)]
    variables_lab = [f"lab_{i}" for i in range(labs)]
    variables_dep = [f"dep_{i}" for i in range(deposits)]
    variables_air = [f"air_{i}" for i in range(airlocks)]
    variables= variables_hab+variables_gen+variables_lab+variables_dep+variables_air
    restricciones = []
    dominio_general_variables = [
        (f, c) for f in range(filas) for c in range(columnas) 
        if (f, c) not in crateres_sets #quita del dominio aquellas posiciones donde existen crateres.
    ]
    dominio_air = [
        (f,c) for (f,c) in dominio_general_variables
        if f==0 or f==filas-1 or c==0 or c==columnas-1
    ]
    dominio_hab = [
    (f, c) for (f, c) in dominio_general_variables
    if f != 0 and f != filas - 1 and c != 0 and c != columnas - 1
    ] 
        
    dominios= {}
    for hab in variables_hab:
        dominios[hab]=dominio_hab #agrega al diccionario de habitaciones, los dominios que no estan al borde
    for air in variables_air:
        dominios[air]= dominio_air #agrega al diccionario de esclusas de aire, los dominios que estan al borde 
    for var in variables_gen+variables_lab+variables_dep:
        dominios[var]= dominio_general_variables        
    # sin superposicion
    def diferentes(variables, values):
        return values[0] != values[1]

    for var1, var2 in combinations((variables), 2):
        restricciones.append(
        ((var1, var2), diferentes)
    )
    def verificar_adyacencia(variables,values):
        val1,val2= values
        f1,c1= val1
        f2,c2= val2
        if ((f1+1 == f2 or f1-1 == f2) and c1==c2) or ((c1+1==c2 or c1-1==c2) and f1==f2):
            return False 
        return True
    #aislamiento hab y generador
    for gen in variables_gen:
        for hab in variables_hab:
            restricciones.append(((gen,hab),verificar_adyacencia))
    #aislamiento generadores
    for gen1, gen2 in combinations((variables_gen), 2):
        restricciones.append(
        ((gen1, gen2), verificar_adyacencia)
    )
    def cadena_suministro(variables,values):
        val1= values[0]
        val2= values[1:]
        f1,c1= val1
        for f2,c2 in val2:
            if ((f1+1 == f2 or f1-1 == f2) and c1==c2) or ((c1+1==c2 or c1-1==c2) and f1==f2):
                return True #cuando encuentra al menos 1 deposito adyacente, return True.
        return False #no encontro ningun deposito adyacente al laboratorio
    #laboratorios adyacentes a deposito
    for lab in variables_lab:
        variables_evaluar= [lab] + variables_dep
        variables_evaluar_tupla= tuple(variables_evaluar)
        restricciones.append((variables_evaluar_tupla,cadena_suministro))
    
    def modulo_habitacion_libre(variables,values):
        val1= values[0]
        val2= values[1:]
        f1,c1= val1
        contador=0
        adyacentes= ((f1+1,c1),(f1-1,c1),(f1,c1+1),(f1,c1-1))
        for a in adyacentes:
            if (a in crateres_sets):
                contador+=1
        for f2,c2 in val2:
            if ((f1+1 == f2 or f1-1 == f2) and c1==c2) or ((c1+1==c2 or c1-1==c2) and f1==f2):
                contador+=1 #si encuentra algo en la posicion adyacente, devuelve False
        if contador>3: 
            return False
        return True 
    
    for hab in variables_hab:
        variables_evaluar= [hab] + variables_dep + variables_air+ variables_gen+variables_lab
        variables_evaluar_tupla= tuple(variables_evaluar)
        restricciones.append((variables_evaluar_tupla,modulo_habitacion_libre))    
