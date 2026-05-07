from simpleai.search import SearchProblem, astar

def planear_rover(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
    
    estado_inicial = (
        rover_inicio,
        bateria_inicial,
        None, #taladro desequipado = None, taladro termico = "termico", taladro percusion ="percutor"
        0,# bolsas que tiene junto, este valor puede ser 0,1 o 2.
        tuple(muestras_igneas),
        tuple(muestras_sedimentarias)
    )
    TAMANIO_GRILLA= 5
    SOMBRAS = zonas_sombra
    GASTOS_BATERIA={"moverse":1,
                    "sobremarcha":4,
                    "equipar":1,
                    "recolectar":3,
                    "depositar":1, # verificar si es depositar o entregar
                    "recargar":0
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
            movimientos=[
                (posF-1,posC),
                (posF+1,posC),
                (posF,posC-1),
                (posF,posC+1)
            ]
            movimientos_sobremarcha=[
                (posF-2,posC),
                (posF+2,posC),
                (posF,posC-2),
                (posF,posC+2)
            ]
            #accion sobremarcha
            if bateria>4:    
                for nuevaF,nuevaC in movimientos_sobremarcha:
                    if 0<=nuevaF < TAMANIO_GRILLA and 0<=nuevaC <TAMANIO_GRILLA:
                        acciones_posibles.append("sobremarcha",(nuevaF,nuevaC))    
            if bateria>1:   
                #accion moverse
                for nuevaF,nuevaC in movimientos:
                    if 0<=nuevaF < TAMANIO_GRILLA and 0<=nuevaC <TAMANIO_GRILLA:
                        acciones_posibles.append("moverse",(nuevaF,nuevaC))
                #accion equipar  
                if taladro==None:
                    acciones_posibles.append("equipar","percutor") 
                    acciones_posibles.append("equipar","termico")
                if taladro=="termico":
                    acciones_posibles.append("equipar","percutor") 
                else:
                    acciones_posibles.append("equipar","termico")
                #accion depositar 
                if almacenamiento==2 or ((len(igneas)+len(sedimentarias)==1) and (almacenamiento==1)): #indica que es la ultima bolsa     
                    acciones_posibles.append("depositar",None)    
            #accion recolectar
            if bateria>3: 
                if posicion_robot in igneas and almacenamiento<2 and taladro=="termico":
                    acciones_posibles.append("recolectar","ignea")
                if posicion_robot in sedimentarias and almacenamiento<2 and taladro=="percutor" :
                    acciones_posibles.append("recolectar","sedimentaria")     
            #accion recargar
            if posicion_robot not in SOMBRAS: 
                acciones_posibles.append("recargar",None)
                 
            return acciones_posibles

        def result(self, state, action):
            lista_estado= list(state)
            nombre_accion,descripcion=action
            if nombre_accion=="moverse" or nombre_accion=="sobremarcha":
                lista_estado[0]=descripcion   
            if nombre_accion=="equipar":
                lista_estado[2]=descripcion
            if nombre_accion=="recolectar":
                if descripcion=="ignea":
                    lista_estado[4].remove(lista_estado[0])
                else:
                    lista_estado[5].remove(lista_estado[0])    
            if nombre_accion=="depositar":
                lista_estado[3]==0
            if nombre_accion=="recargar":
                lista_estado[1]+=10
                if lista_estado[1]>20:
                    lista_estado[1]=20 #supero la bateria maxima
            lista_estado[1]-=GASTOS_BATERIA[nombre_accion]
            return state 

        def is_goal(self, state):
            bateria=state[1]
            almacenamiento= state[4]
            piedras_igneas= len(state[5])
            piedras_sedimentarias= len(state[6])
            return bateria>=0 and almacenamiento==0 and piedras_igneas==0 and piedras_sedimentarias==0
        #is_goal cuando se cumple que la bateria alcanzo, no tiene piedras almacenadas y no existen piedras por juntar. 

        def cost(self, state, action, state2):
            nombre_accion,descripcion= action
            if nombre_accion=="depositar" and state[3] ==2:
                return 2
            return COSTO_TIEMPO[nombre_accion]
        def heuristic(self, state):
            return 0
