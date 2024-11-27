import pygame
import sys
from maze import get_labyrinth  # Importar la función para obtener el laberinto

# Inicializar pygame
pygame.init()

# Recuperar laberinto y posiciones
maze, player_pos, enemies_pos = get_labyrinth()
# Configuración de variables
CELL_SIZE = 30  # Tamaño de cada celda en píxeles
ROWS = len(maze)  # Número de filas
COLS = len(maze[0])  # Número de columnas
FPS = 30
ENEMY_MOVE_DELAY = 15  # Número de fotogramas que deben pasar antes de que un enemigo se mueva

frame_count = 0  # Contador de fotogramas

# Crear ventana
screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("Escape Labyrinth")

# Crear reloj
clock = pygame.time.Clock()

# Color del jugador
PLAYER_COLOR = (0, 0, 255)

def renderMaze():
    # Dibujar maze
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if maze[row][col] == 1:
                color = (50, 50, 50)  # Pared
            elif maze[row][col] == 0:
                color = (0, 0, 0)  # Camino
            elif maze[row][col] == "S":
                color = (0, 255, 0)  # Inicio
            elif maze[row][col] == "E":
                color = (255, 0, 0)  # Salida

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))


def renderPlayer(player_pos):
    player_x = player_pos[1] * CELL_SIZE
    player_y = player_pos[0] * CELL_SIZE
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, CELL_SIZE, CELL_SIZE))


def renderEnemies(enemies_pos):
    ENEMY_COLOR = (255, 0, 255)  # Color de los enemigos (púrpura)
    for enemy in enemies_pos:
        enemy_x = enemy[1] * CELL_SIZE
        enemy_y = enemy[0] * CELL_SIZE
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy_x, enemy_y, CELL_SIZE, CELL_SIZE))


def playerMovement(event, player_pos, maze):
    new_pos = player_pos.copy()  # Copiar posición actual
    if event.key == pygame.K_UP:
        new_pos[0] -= 1  # Mover hacia arriba
    elif event.key == pygame.K_DOWN:
        new_pos[0] += 1  # Mover hacia abajo
    elif event.key == pygame.K_LEFT:
        new_pos[1] -= 1  # Mover hacia la izquierda
    elif event.key == pygame.K_RIGHT:
        new_pos[1] += 1  # Mover hacia la derecha

    # Verificar colisiones con paredes
    if maze[new_pos[0]][new_pos[1]] != 1:  # Si no es pared
        return new_pos  # Retorna la nueva posición si es válida
    return player_pos  # Retorna la posición actual si hay colisión


def checkCollisions(player_pos, enemies_pos):
    for enemy in enemies_pos:
        if player_pos == enemy[:2]:  # Comparamos solo las primeras dos coordenadas
            return True  # El jugador ha chocado con un enemigo
    return False



# Función para mover los enemigos
def moveEnemies(enemies_pos, maze, frame_count):
    if frame_count % ENEMY_MOVE_DELAY == 0:
        for enemy in enemies_pos:
            direction = enemy[2]  # Dirección actual del enemigo (0 = arriba, 1 = abajo, 2 = izquierda, 3 = derecha)
            # Movimiento según la dirección
            if direction == 0:  # Arriba
                next_pos = [enemy[0] - 1, enemy[1]]
            elif direction == 1:  # Abajo
                next_pos = [enemy[0] + 1, enemy[1]]
            elif direction == 2:  # Izquierda
                next_pos = [enemy[0], enemy[1] - 1]
            elif direction == 3:  # Derecha
                next_pos = [enemy[0], enemy[1] + 1]

            # Verificar si la nueva posición es una pared o está fuera de los límites
            if (
                0 <= next_pos[0] < len(maze)
                and 0 <= next_pos[1] < len(maze[0])
                and maze[next_pos[0]][next_pos[1]] != 1
            ):
                enemy[0], enemy[1] = next_pos  # Mover al enemigo a la nueva posición
            else:
                # Si choca con una pared, cambiar la dirección
                if direction == 0:
                    enemy[2] = 1  # Cambiar a abajo
                elif direction == 1:
                    enemy[2] = 0  # Cambiar a arriba
                elif direction == 2:
                    enemy[2] = 3  # Cambiar a derecha
                elif direction == 3:
                    enemy[2] = 2  # Cambiar a izquierda


# Bucle principal
def main():
    global player_pos, enemies_pos, frame_count
    running = True
    while running:
        screen.fill((0, 0, 0))

        renderMaze()
        renderPlayer(player_pos)
        renderEnemies(enemies_pos)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar el juego
                running = False

            if event.type == pygame.KEYDOWN:
                player_pos = playerMovement(event, player_pos, maze)

        # Mover enemigos
        moveEnemies(enemies_pos, maze, frame_count)

        # Verificar si el jugador ha chocado con un enemigo
        if checkCollisions(player_pos, enemies_pos):
            print("¡El jugador ha sido alcanzado por un enemigo!")
            running = False

        # Aumentar el contador de fotogramas
        frame_count += 1

        pygame.display.update()
        clock.tick(FPS)  # Limitar los fotogramas por segundo

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
