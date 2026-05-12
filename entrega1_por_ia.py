from simpleai.search import SearchProblem, astar

def planear_rover(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
    
    # Convertimos listas a tuplas para asegurar que sean hasheables dentro del estado
    zonas_sombra = tuple(zonas_sombra)
    muestras_igneas = tuple(muestras_igneas)
    muestras_sedimentarias = tuple(muestras_sedimentarias)

    class AresRoverProblem(SearchProblem):
        def __init__(self, initial_state):
            super().__init__(initial_state)

        def actions(self, state):
            pos, bateria, taladro, carga, m_igneas, m_sedim = state
            accs = []

            # 1. Movimientos (moverse y sobremarcha)
            r, c = pos
            # Moverse (1 min, 1 bat)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                destino = (r + dr, c + dc)
                if bateria > 1:
                    accs.append(("moverse", destino))
            
            # Sobremarcha (1 min, 4 bat)
            for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                destino = (r + dr, c + dc)
                if bateria > 4:
                    accs.append(("sobremarcha", destino))

            # 2. Equipar taladro (3 min, 1 bat)
            if bateria > 1:
                if taladro != "termico":
                    accs.append(("equipar", "termico"))
                if taladro != "percusión":
                    accs.append(("equipar", "percusión"))

            # 3. Recolectar (2 min, 3 bat)
            if bateria > 3 and len(carga) < 2:
                if pos in m_igneas and taladro == "termico":
                    accs.append(("recolectar", "ignea"))
                if pos in m_sedim and taladro == "percusión":
                    accs.append(("recolectar", "sedimentaria"))

            # 4. Depositar (1 min por muestra, 1 bat)
            # Regla: 2 muestras o la última del mundo
            if len(carga) > 0:
                total_restantes = len(m_igneas) + len(m_sedim)
                if len(carga) == 2 or (len(carga) == 1 and total_restantes == 0):
                    if bateria > 1:
                        accs.append(("depositar", None))

            # 5. Recargar (4 min, restaura hasta 20)
            if pos not in zonas_sombra and bateria < 20:
                accs.append(("recargar", None))

            return accs

        def result(self, state, action):
            pos, bateria, taladro, carga, m_igneas, m_sedim = state
            tipo, param = action

            if tipo == "moverse":
                return (param, bateria - 1, taladro, carga, m_igneas, m_sedim)
            
            if tipo == "sobremarcha":
                return (param, bateria - 4, taladro, carga, m_igneas, m_sedim)

            if tipo == "equipar":
                return (pos, bateria - 1, param, carga, m_igneas, m_sedim)

            if tipo == "recolectar":
                nueva_carga = list(carga)
                nueva_carga.append(param)
                if param == "ignea":
                    nuevas_m = tuple(m for m in m_igneas if m != pos)
                    return (pos, bateria - 3, taladro, tuple(nueva_carga), nuevas_m, m_sedim)
                else:
                    nuevas_m = tuple(m for m in m_sedim if m != pos)
                    return (pos, bateria - 3, taladro, tuple(nueva_carga), m_igneas, nuevas_m)

            if tipo == "depositar":
                # El costo de batería es 1 fijo, pero el tiempo (cost) escala con len(carga)
                return (pos, bateria - 1, taladro, (), m_igneas, m_sedim)

            if tipo == "recargar":
                nueva_bat = min(20, bateria + 10)
                return (pos, nueva_bat, taladro, carga, m_igneas, m_sedim)

        def is_goal(self, state):
            # Todas las muestras recolectadas y carga vacía (depositada)
            return len(state[3]) == 0 and len(state[4]) == 0 and len(state[5]) == 0

        def cost(self, state, action, state2):
            tipo, _ = action
            if tipo == "depositar":
                # state[3] es la carga antes de depositar
                return len(state[3])
            costs = {"moverse": 1, "sobremarcha": 1, "equipar": 3, "recolectar": 2, "recargar": 4}
            return costs.get(tipo, 1)

        def heuristic(self, state):
            # Una heurística simple y admisible:
            # Cada muestra pendiente requiere al menos: moverse (1) + recolectar (2) = 3 minutos.
            # Además, si hay muestras en la bodega, requieren al menos depositar (1).
            m_pendientes = len(state[4]) + len(state[5])
            carga_actual = len(state[3])
            
            # Multiplicamos por 2 en lugar de 3 para ser extremadamente conservadores y asegurar admisibilidad
            # ya que "sobremarcha" permite cubrir 2 celdas en 1 min.
            return (m_pendientes * 2) + (1 if carga_actual > 0 else 0)

    # Estado inicial: (posicion, bateria, taladro, carga_tupla, muestras_igneas_tupla, muestras_sedim_tupla)
    estado_inicial = (rover_inicio, bateria_inicial, "ninguno", (), muestras_igneas, muestras_sedimentarias)
    
    problema = AresRoverProblem(estado_inicial)
    resultado = astar(problema, graph_search=True)
    
    if resultado:
        return [accion for accion, estado in resultado.path()[1:]]
    return []