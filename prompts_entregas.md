Prompt utilzado para entrega1_por_ia.py:

Actúa como un experto en Inteligencia Artificial y Python.
Necesito que resuelvas el siguiente problema de búsqueda utilizando la librería simpleai.search. El objetivo es encontrar la secuencia de acciones óptima (menor tiempo total) para que un rover en Marte recolecte todas las muestras.
Requisitos técnicos obligatorios:
Función Principal: Debes implementar obligatoriamente la función planear_rover(rover_inicio, bateria_inicial, zonas_sombra, muestras_igneas, muestras_sedimentarias) que retorne una lista de tuplas con el formato especificado en la consigna.
Algoritmo: Utiliza astar (A*) para garantizar la optimalidad en tiempo (costo).
Definición del Estado: Diseña un estado que sea hasheable (tuplas). Debe incluir: posición del rover, batería actual, taladro equipado, muestras en la bodega (carga), y las muestras que aún faltan recolectar en el mapa.
Heurística Admisible: Implementa una función heuristic que no sobreestime el costo real 
Costo: El método cost debe devolver el tiempo que consume cada acción (1, 2, 3 o 4 minutos según corresponda).
Restricciones críticas a programar en el método actions y result:
Batería: El rover nunca debe llegar a 0. Si una acción consume más batería de la disponible, no es válida. El tope de batería es 20.
Carga: Máximo 2 muestras. Solo se puede "depositar" para vaciar la carga.
Taladros: Para recolectar una muestra ígnea se requiere el taladro "termico"; para sedimentaria, el de "percusión".
Depósito: Para depositar (crear cápsula) se requieren 2 muestras, a menos que solo quede una última muestra en el mundo por recolectar o ya cargada.
Recarga: No permitida en zonas_sombra.
Adjunto la consigna completa y el archivo de tests. Asegúrate de que el código pase todos los tests provistos, respetando los nombres de las acciones y el formato de las coordenadas.



