from simpleai.search import SearchProblem, astar
from simpleai.search.viewers import ConsoleViewer
def planear_rover(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
    
    estado_inicial = (
        rover_inicio,
        bateria_inicial,
        None, #taladro desequipado = None, taladro termico = "termico", taladro percusion ="percutor"
        0,# bolsas que tiene junto, este valor puede ser 0,1 o 2.
        tuple(muestras_igneas),
        tuple(muestras_sedimentarias)
    )
    SOMBRAS = zonas_sombra
    GASTOS_BATERIA={"moverse":1,
                    "sobremarcha":4,
                    "equipar":1,
                    "recolectar":3,
                    "depositar":1, # verificar si es depositar o entregar
                    "recargar":-10
                    }
    COSTO_TIEMPO={"moverse":1,
                    "sobremarcha":1,
                    "equipar":3,
                    "recolectar":2,
                    "depositar":1,
                    "recargar":4
                    }
    

    class Ares1Problem(SearchProblem):
        def actions(self, state):
            acciones_posibles= []
            posicion_robot,bateria,taladro,almacenamiento,igneas,sedimentarias= state
            posF,posC= posicion_robot
            movimientos_sobremarcha=[
                (posF-2,posC),
                (posF+2,posC),
                (posF,posC-2),
                (posF,posC+2)
            ]
            #accion sobremarcha
            if bateria>4:    
                acciones_posibles.append(("sobremarcha",(posF-2,posC))) #abajo
                acciones_posibles.append(("sobremarcha",(posF+2,posC))) #arriba
                acciones_posibles.append(("sobremarcha",(posF,posC-2)))#izquierda
                acciones_posibles.append(("sobremarcha",(posF,posC+2))) #derecha 
            if bateria>1:   
                #accion moverse
                acciones_posibles.append(("moverse",(posF-1,posC))) #abajo
                acciones_posibles.append(("moverse",(posF+1,posC))) #arriba
                acciones_posibles.append(("moverse",(posF,posC-1)))#izquierda
                acciones_posibles.append(("moverse",(posF,posC+1))) #derecha

                if posicion_robot in igneas:
                    #accion equipar  
                    if taladro!="termico":
                        acciones_posibles.append(("equipar","termico"))
                if posicion_robot in sedimentarias:
                    if taladro!="percusion":
                        acciones_posibles.append(("equipar","percusion")) 
                #accion depositar 
                if almacenamiento > 0:
                    if almacenamiento == 2 or (len(igneas) + len(sedimentarias) == 0):
                        acciones_posibles.append(("depositar", None))   
            #accion recolectar
            if bateria>3: 
                if posicion_robot in igneas and almacenamiento<2 and taladro=="termico":
                    acciones_posibles.append(("recolectar","ignea"))
                if posicion_robot in sedimentarias and almacenamiento<2 and taladro=="percusion" :
                    acciones_posibles.append(("recolectar","sedimentaria"))     
            #accion recargar
            if posicion_robot not in SOMBRAS and bateria<20: #si no esta en un area de sombras y la bateria no esta cargada al maximo
                acciones_posibles.append(("recargar",None))
                 
            return acciones_posibles

        def result(self, state, action):
            lista_estado= list(state)
            nombre_accion,descripcion=action
            if nombre_accion=="moverse" or nombre_accion=="sobremarcha":
                lista_estado[0]=descripcion   
            if nombre_accion=="equipar":
                lista_estado[2]=descripcion
            if nombre_accion=="recolectar":
                lista_estado[3] += 1
                if descripcion=="ignea":
                    lista_rocas_igneas= list(lista_estado[4])
                    lista_rocas_igneas.remove(lista_estado[0])
                    lista_estado[4] = tuple(lista_rocas_igneas)
                else:
                    lista_rocas_sedimentarias = list(lista_estado[5])
                    lista_rocas_sedimentarias.remove(lista_estado[0])
                    lista_estado[5] = tuple(lista_rocas_sedimentarias) 
            if nombre_accion=="depositar":
                lista_estado[3]=0    
            lista_estado[1]-=GASTOS_BATERIA[nombre_accion]
            if lista_estado[1]>20:
                lista_estado[1]=20
            return tuple(lista_estado) 

        def is_goal(self, state):
            bateria=state[1]
            almacenamiento= state[3]
            piedras_igneas= len(state[4])
            piedras_sedimentarias= len(state[5])
            return bateria>0 and almacenamiento==0 and piedras_igneas==0 and piedras_sedimentarias==0
        #is_goal cuando se cumple que la bateria alcanzo, no tiene piedras almacenadas y no existen piedras por juntar. 

        def cost(self, state, action, state2):
            nombre_accion,descripcion= action
            if nombre_accion=="depositar" and state[3] ==2:
                return 2
            return COSTO_TIEMPO[nombre_accion]
        def heuristic(self, state):
            posicion_robot,bateria,taladro,almacenamiento,igneas,sedimentarias= state
            heuristica_valor = 0
            bateriaNecesaria = 0
            cant_igneas = len(igneas)
            cant_sed = len(sedimentarias)
            
            heuristica_valor += (cant_igneas + cant_sed)*2 #tiempo de recoleccion por cada piedra es de 2 minutos
            heuristica_valor += (cant_igneas + cant_sed) #tiempo de deposito minimo por cada piedra 1 minuto
            heuristica_valor += almacenamiento

            muestras = igneas + sedimentarias
            if len(muestras) >= 1:
                distancias  = []
                for m in muestras:
                    distancias.append(abs(posicion_robot[0] - m[0]) + abs (posicion_robot[1] - m[1]))
                    
                distMax = max(distancias)
                heuristica_valor += distMax/2
                #Buscamos la distnacia a la roca mas cercana y lo hacemos /2 porque se puede utilizar sobremarcha

                bateriaNecesaria += (cant_igneas + cant_sed)*GASTOS_BATERIA["recolectar"] #bateria necesaria para recolectar las piedras restantes
                bateriaNecesaria += ((cant_igneas + cant_sed)/2)*GASTOS_BATERIA["depositar"] #bateria necesaria para depositar las piedras restantes, se hace /2 porque se pueden depositar 2 piedras juntas
                bateriaNecesaria += distMax*GASTOS_BATERIA["moverse"] #bateria necesaria para moverse a la roca mas cercana

            if cant_igneas > 0 and taladro != "termico":
                heuristica_valor += 3
                bateriaNecesaria += GASTOS_BATERIA["equipar"]
            if cant_sed > 0 and taladro != "percusion":
                heuristica_valor += 3
                bateriaNecesaria += GASTOS_BATERIA["equipar"]
            if bateriaNecesaria > bateria:
                heuristica_valor += 4
            return heuristica_valor
        
    problema = Ares1Problem(initial_state=estado_inicial)
    solucion = astar(problema, graph_search=True)
    
    if solucion:
        return [paso[0] for paso in solucion.path() if paso[0] is not None]
    return []

if __name__ == "__main__":
    # Caso de prueba manual
    inicio = (0, 0)
    bat = 20
    sombras = [(0,1), (0,2)]
    i = [(1, 1),(1,2)]
    s = [(2, 3)]

    resultado = planear_rover(inicio, bat, sombras, i, s)

    if resultado:
        print("¡Plan encontrado!")
        for i, accion in enumerate(resultado):
            print(f"Paso {i+1}: {accion}")
    else:
        print("No se encontró solución.")