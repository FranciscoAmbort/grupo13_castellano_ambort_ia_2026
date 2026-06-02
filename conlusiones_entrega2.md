Luego de comparar los diferentes códigos, pudimos ver que tanto nuestra solución como la
solución generada por la IA (GeminisPro) parten de una base de variables iguales, debido
a que se definen exactamente el mismo conjunto y ambos aplicamos una estrategia
temprana para quitar dominios. Esto se hace para optimizar el espacio de búsqueda desde
el inicio al restringir el dominio de las esclusas de aire exclusivamente a los bordes del
mapa, y el de los módulos habitacionales estrictamente a las celdas del interior. También,
ambos enfoques descartamos del terreno preventivamente todas las coordenadas
ocupadas por cráteres intransitables.

Al ejecutar ambas soluciones,pudimos ver que en esta entrega(a diferencia de la entrega1),
los dos códigos funcionan perfecto y pasan todas las pruebas, la diferencia se encuentra
en el tiempo de ejecución. El código que armamos nosotros tardó alrededor de 3.60 segundos,
casi la mitad que el de la IA, que se fue a 6.59 segundos. Esto pasa porque la IA
intentó dar una solución demasiado estructurada, teniendo varias funciones a las cuales
llamaba, cada vez que el programa intentaba buscar una posición para los módulos del
campamento, pero al hacer esto, termino ralentizando el programa, debido a que las
llamada a funciones en python son más caras de lo normal.

Nuestra versión es más rápida porque va directo al grano. En lugar de llamar tantas
funciones o de por ejemplo hacer (otras_posiciones = set(values[1:])) en la última
restricción (esto termina siendo contraproducente), usamos caminos más directos para
revisar si las habitaciones tienen salida o si los laboratorios estaban adyacentes de los
depósitos. Al final, en este trabajo podemos ver, que si bien la IA, generó un código que
cumple con las expectativas, la eficiencia del mismo es pobre comparada con lo realizado por nuestra parte.
