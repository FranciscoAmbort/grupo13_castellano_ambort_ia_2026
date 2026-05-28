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

Prompt utilzado para entrega2_por_ia.py:

Actúa como un Ingeniero de Software experto en Inteligencia Artificial y resolución de problemas de satisfacción de restricciones (CSP). Necesito que resuelvas un problema de diseño de campamento base en Marte utilizando la biblioteca `simpleai.search` en Python. 

El código generado formará parte de un archivo llamado `entrega2_por_ia.py` y debe cumplir estrictamente con las siguientes pautas.

### Consigna del Problema
Debemos ubicar una cantidad exacta de módulos en una cuadrícula rectangular de dimensiones `(filas, columnas)`. 
Los tipos de módulos y sus identificadores son:
- Habitacional: "hab"
- Generador: "gen"
- Laboratorio: "lab"
- Depósito: "dep"
- Esclusa de aire: "air"

Algunas celdas de la cuadrícula contienen "cráteres" `(craters)` y son completamente inaccesibles.

### Interfaz Requerida
Debes implementar la función principal con la siguiente firma exacta:
def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    """
    camp_size: tupla (filas, columnas)
    habs, generators, labs, deposits, airlocks: enteros con las cantidades a ubicar
    craters: lista de tuplas (fila, columna)
     Retorna: Lista de tuplas (tipo, fila, columna) o None si no hay solución.
    """

### Restricciones a Implementar (Compatibles con SimpleAI)
1. Sin superposición: No puede haber dos módulos en la misma celda.
2. Cráteres intransitables: Ningún módulo puede estar en una celda de la lista `craters`.
3. Esclusas en el borde: Las esclusas ("air") solo pueden estar en la primera/última fila o primera/última columna.
4. Habitacionales al interior: Los módulos "hab" NO pueden estar en los bordes de la cuadrícula.
5. Seguridad energética: Un "gen" no puede ser adyacente ortogonalmente (arriba, abajo, izquierda, derecha) a un "hab".
6. Aislamiento entre generadores: Dos "gen" no pueden ser adyacentes ortogonalmente entre sí.
7. Cadena de suministro científico: Cada "lab" debe ser adyacente ortogonalmente a AL MENOS UN "dep".
8. Ruta de evacuación: Cada módulo "hab" debe tener al menos una celda vecina ortogonal completamente libre (es decir, que no contenga ningún módulo de ningún tipo y que tampoco sea un cráter).

### Estrategia de Modelado CSP (Muy Importante)
Para asegurar que se cumplan las cantidades exactas de módulos eficientemente, modela el CSP de la siguiente manera:
- Variables: Crea una lista de variables únicas para cada módulo individual según la cantidad pedida. Por ejemplo, si `habs=2` y `generators=1`, las variables pueden ser `['hab_0', 'hab_1', 'gen_0']`.
- Dominios: El dominio de cada variable debe ser la lista de todas las posiciones `(fila, columna)` posibles de la cuadrícula. Para optimizar, puedes excluir los cráteres directamente de los dominios iniciales.
- Restricciones de SimpleAI: Utiliza `CspProblem` y el método `backtrack` de `simpleai.search`. Define las restricciones utilizando funciones que reciban las variables involucradas y verifiquen las condiciones de adyacencia o posición. 
  - Nota para el Lab (Restricción 7): Dado que un laboratorio requiere *al menos un* depósito adyacente, asocia la restricción a la variable del laboratorio y a *todas* las variables de depósitos en conjunto.
  - Nota para la Evacuación (Restricción 8): Dado que depende de todas las variables para saber qué celdas quedan libres, implementa una restricción global o multivariable que involucre al habitacional y al resto de los componentes para chequear las celdas libres a su alrededor.

### Requisitos de Código y Rendimiento
- No ejecutes ninguna lógica de CSP a nivel de módulo (al importar el archivo). Todo debe procesarse dentro de `build_camp`.
- Si `backtrack` no encuentra solución, la función debe retornar explícitamente `None`.
- Si encuentra solución, transforma el diccionario devuelto por `backtrack` (ej: `{'hab_0': (1,2)}`) al formato de salida requerido: una lista de tuplas `(tipo, fila, columna)` (ej: `[('hab', 1, 2)]`).
- Escribe un código limpio, modular, bien comentado en español, optimizando las funciones de restricción para que el algoritmo descarte ramas inválidas lo antes posible (heurísticas por defecto de simpleai).

Por favor, provee únicamente el código de Python estructurado y listo para ser testeado.

