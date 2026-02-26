[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zLAxRSGr)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22890628&assignment_repo_type=AssignmentRepo)
# Práctica 3. Estructuras
En esta práctica, utilizaremos el tipo de dato `struct` para generar nuevos tipos de datos que contengan atributos de diferentes tipos.

En este repositorio se encuentran tres archivos con terminación ".c". Estos contienen los esqueletos de los programas en lenguaje C sobre los que se puede hacer la edición para obtener finalmente el código que resuelve el problema. Si se desea, se puede escribir el código desde 0, sin seguir el esqueleto. También se puede resolver alguno o todos los ejercicios en Python. Si es el caso, se tiene que generar el archivo con terminación ".py" y hacer el desarrollo correspondiente.

**Nota importante:** Al final de cada esqueleto, hay una sección de preguntas teóricas que deben de ser contestadas junto con la entrega de la práctica. 

## Ejercicio 1. Simulador de Póker (2 jugadores)
Para este ejercicio, se requiere definir una estructura que represente los naipes de una _baraja inglesa_, la cual consiste de 52 cartas que se clasifican por dos datos: El _palo_ (tréboles, espadas, corazones y diamantes); cada palo consta de 13 cartas con un valor o puntaje: As, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K. Para los efectos del ejercicio, los valores se pueden tomar del 1 al 13. **Ninguna de las cartas se repite**.

La versión básica de Póker que programarán en este ejercicio se llama _Texas Hold'em_. El juego consta de varias fases que se describen fácilmente en rondas:
 - **Primera ronda**: El jugador 1 y el jugador 2 reciben dos cartas de manera aleatoria. Cada jugador tiene derecho de permanecer en el juego o retirarse. Si ambos jugadores se quedan en el juego, se pasa a la siguiente ronda.
 - **Segunda ronda**: Al inicio de la segunda ronda, el _dealer_ (básicamente, el programa) muestra tres cartas elegidas aleatoriamente. A este conjunto de tres cartas se le llama _river_. Nuevamente, a cada jugador se le pregunta si desea permanecer en el juego o retirarse. Si ambos se quedan, se pasa a la siguiente ronda.
 - **Tercera ronda**: Al inicio de la tercera ronda, el dealer muestra una carta carta que agrega a las tres del river. Se le vuelve a consultar a cada jugador si se queda o se retira. Si ambos se quedan, se pasa a la siguiente ronda.
 - **Cuarta ronda**: En la cuarta ronda, se abre la quinta y última carta que se elige aleatoriamente. En esta ronda, no es necesario consultar si los jugadores se quedan o se retiran. Directamente se determina quién gana la partida.
 - **Condición de gane**: Un jugador ganará la partida si ocurre alguno de los siguientes escentarios:
   1. Si el otro jugador se retira del juego en alguna de las primeras tres rondas.
   2. Si ambos jugadores llegan a la última ronda, ganará aquél jugador cuyo par de cartas puedan sustituir dos de las cinco cartas del dealer y se forme una mano _mejor_ que lo que se formaría con el par de cartas del otro jugador.
  
 **Jerarquía de manos**:
 1. _Corrida real_: 10, 11, 12, 13, 1 del mismo palo.
 2. _Corrida de color_: 5 cartas seguidas del mismo palo (por ejemplo, 3, 4, 5, 6 y 7 de tréboles).
 3. _Póker_: 4 cartas iguales (por ejemplo, 5 de espadas, 5 de tréboles, 5 de diamantes y 5 de corazones).
 4. _Casa llena (tercia y par)_: Tres cartas con el mismo valor y dos cartas con el mismo valor.
 5. _Color_: 5 cartas del mismo palo.
 6. _Corrida_: 5 cartas seguidas (de diferentes palos).
 7. _Tercia_.:
 8. _Dos pares_.
 9. _Un par_.
 10. _Carta más alta_: Gana la carta más alta cuando ninguno de los dos jugadores puede generar alguna de las manos superiores con las cartas del dealer. Por ejemplo, si el dealer tiene las cartas 4 de tréboles, 5 de corazones, 9 de espadas, y 7 y J de diamantes, el jugador 1 tiene 12 y 2 de corazones, y el jugador 2 tiene 13 de espadas y 3 de tréboles, entonces gana el jugador 2 por tener el 13.
  
**Funcionalidades adicionales (opcionales)**: Éstas son funcionalidades que pueden incluir en su programa para hacer la simulación un poco más parecida a la realidad (y más divertida!).
- Dos variables `int` guardando la cantidad de fichas que cada jugador tiene, de modo que cada jugador pueda apostar en cada ronda para intentar espantar a su contrincante.
- Que se pueda elegir la cantidad de jugadores que estarán en la partida.
- Una opción para que en la primera ronda, las cartas de cada jugador aparezcan "cubiertas", y que se puedan descubrir y ver cuando el jugador (el usuario) tenga seguridad de que no lo están viendo los demás jugadores.
- Que al final de la partida, aparezca un análisis de cada ronda, en la que se vaya calculando cuál era la probabilidad que cada jugador tenía de ganar dada la información disponible en dicha ronda.

## Ejercicio 2. Pizzería de Copilco
El reto en este ejercicio es definir la estructura `pizza`, cuyos datos son su tamaño (radio de la circunferencia), la cantidad de _toppings_ que llevará, y el precio. El programa le pregunta al usuario cuántas pizzas va a querer, de qué tamaño y con cuáles ingredientes. Al final, el programa debe de arrojar un _ticket_, es decir, el desglose de la orden, y el precio total que va a pagar el usuario. Adicionalmente, se debe de incluir una promoción: Si se compran dos pizzas del mismo tamaño, entonces se aplica la promoción del 2x1, que se debe de ver reflejada en el precio final del ticket.

## Ejercicio 3. Intersección de circunferencias 
En este ejercicio, se debe de definir un tipo de datos que abstraiga la noción de un círculo (es decir, se requiere que contenga un radio positivo, y un par de números reales que indiquen la posición del centro en el plano cartesiano). El programa le pide al usuario que ingrese dos círculos. La función básica del programa es responder si los círculos tienen al menos un punto de intersección. 

**Funcionalidad adicional (opcional)**. Para hacer el problema más interesante. se puede arrojar un valor real positivo, que corresponda con el tamaño del área de intersección de ambos círculos.
