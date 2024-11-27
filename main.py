import pygame
import sys
from maze import get_labyrinth  # Importar la función para obtener el laberinto

# Inicializar pygame
pygame.init()

# Configuración de
state = "MENU"  # Puede ser "MENU", "JUEGO", "INSTRUCCIONES"

# Configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configuración de fuente
font = pygame.font.SysFont(None, 36)


CELL_SIZE = 30  # Tamaño de cada celda en píxeles
FPS = 30
frame_count = 0  # Contador de fotogramas
PLAYER_COLOR = (0, 0, 255)
GOAL_COLOR = (0, 255, 0)
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (100, 255, 100)
INSTRUCTION_TEXT_COLOR = (255, 255, 255)

WIDTH, HEIGHT = 600, 400

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Labyrinth")

# Crear reloj
clock = pygame.time.Clock()


def drawMenu():
    screen.fill(WHITE)

    title_text = font.render("Escape Labyrinth", True, BLUE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Opciones del menú
    options = ["Iniciar Juego", "Instrucciones", "Salir"]
    for i, option in enumerate(options):
        option_text = font.render(option, True, BLACK)
        screen.blit(
            option_text, (WIDTH // 2 - option_text.get_width() // 2, 150 + i * 50)
        )

    pygame.display.update()


def drawInstructions():
    screen.fill(WHITE)

    instructions_text = font.render("Instrucciones del Juego", True, GREEN)
    screen.blit(
        instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, 50)
    )

    instructions = [
        "Usa las teclas de flecha para mover al jugador.",
        "Evita los enemigos y llega a la salida.",
        "Los enemigos se mueven de manera predefinida.",
        "Presiona ESC para regresar al menú.",
    ]
    for i, line in enumerate(instructions):
        line_text = font.render(line, True, BLACK)
        screen.blit(line_text, (50, 150 + i * 40))

    pygame.display.update()


def drawGame():
    global frame_count, state
    maze, player_pos, goal_pos, enemies_pos = get_labyrinth()

    # Ajustar tamaño de la ventana según el laberinto
    screen_width = len(maze[0]) * CELL_SIZE
    screen_height = len(maze) * CELL_SIZE
    # Actualizar el objeto screen globalmente
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True
    while running:
        screen.fill((0, 0, 0))

        renderMaze(maze)
        renderPlayer(player_pos)
        renderEnemies(enemies_pos)
        renderGoal(goal_pos)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar el juego
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Regresar al menú si se presiona ESC
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
                    return  # Salir de drawGame y regresar al bucle principal

                # Mover al jugador
                player_pos = playerMovement(event, player_pos, maze)

        # Mover enemigos
        moveEnemies(enemies_pos, maze, frame_count)

        # Verificar si el jugador ha chocado con un enemigo
        if checkCollisions(player_pos, enemies_pos):
            state = "GAME_OVER"  # Cambiar el estado a Game Over
            return state  # Retorna el nuevo estado

        # Verificar si el jugador ha llegado al objetivo
        if player_pos == goal_pos:
            state = "VICTORIA"  # Cambiar el estado a Victoria
            return state  # Retorna el nuevo estado

        # Aumentar el contador de fotogramas
        frame_count += 1

        pygame.display.update()


def drawGameOver():
    global state
    screen.fill(WHITE)

    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2, 50))

    retry_text = font.render("Reintentar", True, BLACK)
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(retry_text, retry_rect)

    back_menu_text = font.render("Volver al menú", True, BLACK)
    back_menu_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(back_menu_text, back_menu_rect)

    # Detectar clic en "Reintentar"
    if pygame.mouse.get_pressed()[0] and retry_rect.collidepoint(
        pygame.mouse.get_pos()
    ):
        state = "JUEGO"  # Cambiar estado a Juego
        return

    # Detectar clic en "Volver al menú"
    if pygame.mouse.get_pressed()[0] and back_menu_rect.collidepoint(
        pygame.mouse.get_pos()
    ):
        state = "MENU"  # Cambiar estado a Menu
        return

    pygame.display.update()


# Funciones del juego
def renderMaze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = (50, 50, 50) if maze[row][col] == 1 else (0, 0, 0)  # Pared o Camino
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))


def renderGoal(goal_pos):
    goal_x = goal_pos[1] * CELL_SIZE
    goal_y = goal_pos[0] * CELL_SIZE
    pygame.draw.rect(screen, GOAL_COLOR, (goal_x, goal_y, CELL_SIZE, CELL_SIZE), 0)


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
    if frame_count % 80 == 0:
        for enemy in enemies_pos:
            direction = enemy[
                2
            ]  # Dirección actual del enemigo (0 = arriba, 1 = abajo, 2 = izquierda, 3 = derecha)
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


def main():
    global state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if state == "MENU":
                    # Verificar si el mouse está sobre alguna opción
                    if 150 <= mouse_y <= 200:
                        state = "JUEGO"  # Iniciar juego
                    elif 200 <= mouse_y <= 250:
                        state = "INSTRUCCIONES"  # Ver instrucciones
                    elif 250 <= mouse_y <= 300:
                        running = False  # Salir del juego

            if event.type == pygame.KEYDOWN:
                if state == "INSTRUCCIONES" and event.key == pygame.K_ESCAPE:
                    state = "MENU"  # Regresar al menú desde instrucciones

        # Dibujar según el estado actual
        if state == "MENU":
            drawMenu()
        elif state == "INSTRUCCIONES":
            drawInstructions()
        elif state == "JUEGO":
            drawGame()
        elif state == "GAME_OVER":
            drawGameOver()

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
