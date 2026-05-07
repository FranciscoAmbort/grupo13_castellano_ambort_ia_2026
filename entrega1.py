from simpleai.search import SearchProblem, astar

def planear_rover(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias):
    
    estado_inicial = (
        rover_inicio,
        bateria_inicial,
        0,
        0,
        (muestras_igneas),
        (muestras_sedimentarias)
    )
    SOMBRAS = zonas_sombra

    class Ares1Problem(SearchProblem):
        def actions(self, state):


            return 

        def result(self, state, action):
           
            
            return state 

        def is_goal(self, state):

            return False

        def cost(self, state, action, state2):

            return 1

