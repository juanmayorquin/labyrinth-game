# Escape Labyrinth

**Escape Labyrinth** es un juego en 2D creado utilizando la librería **PyGame** en Python. El objetivo del juego es guiar a un jugador a través de un laberinto lleno de obstáculos y enemigos, mientras se busca llegar a la salida sin chocar con los enemigos.

## Características

- **Interfaz de Menú**: El juego comienza con un menú principal donde el jugador puede iniciar el juego, consultar las instrucciones o salir.
- **Juego en 2D**: El jugador se mueve a través de un laberinto generado dinámicamente.
- **Enemigos**: El juego incluye enemigos que se mueven de manera predefinida por el laberinto. El jugador debe evitar colisionar con ellos.
- **Meta del Juego**: El objetivo es llegar a la salida del laberinto sin tocar a los enemigos. Si el jugador choca con un enemigo, el juego termina.
- **Instrucciones**: El juego incluye una pantalla de instrucciones donde se explica cómo jugar y los controles.

## Controles

- **Flechas direccionales**: Mover al jugador en el laberinto (arriba, abajo, izquierda, derecha).
- **Escape**: Regresar al menú desde el juego o desde las instrucciones.
- **Clic izquierdo**: Seleccionar opciones en el menú.

## Pantallas del juego

1. **Menú**: Ofrece tres opciones: iniciar el juego, ver las instrucciones o salir.
2. **Instrucciones**: Explica las reglas del juego y cómo controlar al jugador.
3. **Juego**: El jugador navega a través de un laberinto con el objetivo de llegar a la meta mientras evita a los enemigos.
4. **Game Over**: Si el jugador choca con un enemigo, el juego muestra una pantalla de "Game Over" con opciones para reintentar o volver al menú.

## Estructura del Proyecto

- **Archivo principal (`main.py`)**: Contiene la lógica principal del juego, los menús y las transiciones entre pantallas.
- **Función `get_labyrinth()`**: Importada de un archivo externo (`maze.py`), genera el laberinto aleatoriamente, la posición del jugador, la meta y los enemigos.
- **Funciones personalizadas**: El juego incluye varias funciones personalizadas, como `renderMaze()`, `renderPlayer()`, `renderEnemies()`, entre otras, para manejar la representación del laberinto y los objetos en la pantalla.

## Criterios de evaluación

- El proyecto incluye varias funciones personalizadas, que controlan aspectos como el movimiento del jugador, la generación del laberinto, la interacción con los enemigos y las transiciones de pantalla.
- El código está organizado en diferentes funciones para separar las responsabilidades y mejorar la legibilidad y mantenibilidad.
- El juego cuenta con menús, instrucciones, enemigos y una lógica de juego básica que asegura la interacción fluida con el usuario.

## Requisitos

- Python 3.x
- PyGame (instalar con `pip install pygame`)

## Cómo ejecutar el juego

1. Clona o descarga este repositorio.
2. Asegúrate de tener Python y PyGame instalados.
3. Ejecuta el archivo principal con el siguiente comando:
   ```bash
   python main.py
