"""
Interfaz Pygame para jugar contra la IA entrenada con Q-Learning.
Tablero interactivo, turnos, estadísticas y visualización de resultados.
Requiere el archivo q_table_20000.pkl generado por el entrenamiento.
"""

import sys
import time
import pygame
from qlearning_agente import GameState

pygame.init()

# --- CONSTANTES Y COLORES ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PRIMARY_BLUE = (25, 130, 196)
ACCENT_YELLOW = (255, 200, 50)
PLAYER_X_COLOR = (220, 60, 60)   # Rojo (Humano)
PLAYER_O_COLOR = (60, 130, 220)  # Azul (IA)
BACKGROUND = (25, 15, 55)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

BOARD_SIZE = 3
CELL_SIZE = 120
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE

BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_OFFSET_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2 - 30

# Fuentes
font_title = pygame.font.SysFont('Arial Black', 44, bold=True)
font_medium = pygame.font.SysFont('Arial', 26)
font_small = pygame.font.SysFont('Arial', 20)
font_tiny = pygame.font.SysFont('Arial', 16)


class GameGUI:
    """Clase principal para la interfaz gráfica del juego Tres en Raya."""

    def __init__(self):
        """Inicializa la interfaz gráfica del juego."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tres en Raya - Q-Learning")
        self.clock = pygame.time.Clock()
        self.state = GameState()

        # Cargar agente entrenado
        if not self.state.agent.load_q_table():
            print("ERROR: Ejecuta primero 'entrenamiento_q_learning_20000.py'")
            time.sleep(3)
            pygame.quit()
            sys.exit()

        # Botón centrado debajo del tablero
        button_width = 180
        button_height = 40
        button_x = BOARD_OFFSET_X + (BOARD_WIDTH - button_width) // 2
        button_y = BOARD_OFFSET_Y + BOARD_HEIGHT + 50
        self.new_game_button = pygame.Rect(button_x, button_y,
                                           button_width, button_height)

    def draw_background(self):
        """Dibuja el fondo de la ventana."""
        self.screen.fill(BACKGROUND)

    def draw_board(self):
        """Dibuja el tablero de juego con todas las celdas y marcas."""
        # Fondo del tablero
        board_rect = pygame.Rect(
            BOARD_OFFSET_X - 5, BOARD_OFFSET_Y - 5,
            BOARD_WIDTH + 10, BOARD_HEIGHT + 10
        )
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 2)

        # Líneas del tablero
        line_width = 4
        for i in range(1, BOARD_SIZE):
            x_pos = BOARD_OFFSET_X + i * CELL_SIZE
            pygame.draw.line(
                self.screen, BLACK,
                (x_pos, BOARD_OFFSET_Y),
                (x_pos, BOARD_OFFSET_Y + BOARD_HEIGHT),
                line_width
            )
            y_pos = BOARD_OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(
                self.screen, BLACK,
                (BOARD_OFFSET_X, y_pos),
                (BOARD_OFFSET_X + BOARD_WIDTH, y_pos),
                line_width
            )

        # Dibujar X y O
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_x = (BOARD_OFFSET_X + col * CELL_SIZE +
                          (CELL_SIZE // 2))
                cell_y = (BOARD_OFFSET_Y + row * CELL_SIZE +
                          (CELL_SIZE // 2))

                if self.state.board[row][col] == 'X':
                    pygame.draw.line(
                        self.screen, PLAYER_X_COLOR,
                        (cell_x - 40, cell_y - 40),
                        (cell_x + 40, cell_y + 40), 8
                    )
                    pygame.draw.line(
                        self.screen, PLAYER_X_COLOR,
                        (cell_x + 40, cell_y - 40),
                        (cell_x - 40, cell_y + 40), 8
                    )
                elif self.state.board[row][col] == 'O':
                    pygame.draw.circle(
                        self.screen, PLAYER_O_COLOR,
                        (cell_x, cell_y), 40, 8
                    )

        # Título
        title_text = "TRES EN RAYA - Q-LEARNING"
        title = font_title.render(title_text, True, ACCENT_YELLOW)
        self.screen.blit(title,
                         (WINDOW_WIDTH // 2 - title.get_width() // 2, 30))

        # Subtítulo
        subtitle_text = "Humano (X) vs IA (O)"
        subtitle = font_medium.render(subtitle_text, True, WHITE)
        self.screen.blit(subtitle,
                         (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 85))

    def draw_game_status(self):
        """Dibuja el estado actual del juego (turno o resultado)."""
        status_y = BOARD_OFFSET_Y + BOARD_HEIGHT + 20

        if self.state.game_over:
            if self.state.winner == 'X':
                status_text = "¡GANASTE!"
                color = PLAYER_X_COLOR
            elif self.state.winner == 'O':
                status_text = "GANA LA IA"
                color = PLAYER_O_COLOR
            else:
                status_text = "EMPATE"
                color = ACCENT_YELLOW
        else:
            if self.state.current_player == 'X':
                status_text = "Tu turno (X) - Haz clic"
                color = PLAYER_X_COLOR
            else:
                status_text = "Turno de la IA (O)"
                color = PLAYER_O_COLOR

        status = font_medium.render(status_text, True, color)
        self.screen.blit(
            status,
            (WINDOW_WIDTH // 2 - status.get_width() // 2, status_y)
        )

        # Mostrar movimientos
        moves_text = font_small.render(
            f"Movimiento: {self.state.moves_made}/9", True, WHITE
        )
        self.screen.blit(
            moves_text,
            (WINDOW_WIDTH // 2 - moves_text.get_width() // 2, status_y + 30)
        )

    def draw_stats(self):
        """Dibuja el panel de estadísticas del juego."""
        stats_x = WINDOW_WIDTH - 240
        stats_y = 120
        stats_width = 230
        stats_height = 260

        # Fondo simple
        stats_rect = pygame.Rect(stats_x, stats_y, stats_width, stats_height)
        pygame.draw.rect(self.screen, (40, 50, 90), stats_rect)
        pygame.draw.rect(self.screen, PRIMARY_BLUE, stats_rect, 1)

        # Título
        stats_title = font_medium.render("ESTADÍSTICAS", True, ACCENT_YELLOW)
        self.screen.blit(
            stats_title,
            (stats_x + (stats_width - stats_title.get_width()) // 2,
             stats_y + 10)
        )

        # Línea separadora
        pygame.draw.line(
            self.screen, ACCENT_YELLOW,
            (stats_x + 20, stats_y + 40),
            (stats_x + stats_width - 20, stats_y + 40), 1
        )

        # Estadísticas
        stats = self.state.agent.stats
        total = stats['total_games']

        if total > 0:
            win_rate = (stats['wins'] / total) * 100
        else:
            win_rate = 0

        # Lista de estadísticas
        stat_lines = [
            f"Partidas: {total}",
            f"Victorias IA: {stats['wins']}",
            f"Derrotas IA: {stats['losses']}",
            f"Empates: {stats['ties']}",
            f"Efectividad: {win_rate:.0f}%",
            f"Estados: {stats['states_learned']:,}",
            "Entrenamiento: 20k"
        ]

        line_y = stats_y + 45
        for i, line in enumerate(stat_lines):
            if i == 0:
                color = ACCENT_YELLOW
            elif "Efectividad" in line:
                if win_rate >= 60:
                    color = (150, 255, 150)
                elif win_rate >= 40:
                    color = (255, 255, 150)
                else:
                    color = (255, 150, 150)
            else:
                color = WHITE

            text = font_small.render(line, True, color)
            self.screen.blit(text, (stats_x + 15, line_y))
            line_y += 32

        # Barra de efectividad
        if total > 0:
            bar_width = 200
            bar_height = 10
            bar_x = stats_x + 15
            bar_y = line_y + 5

            pygame.draw.rect(
                self.screen, (60, 60, 80),
                (bar_x, bar_y, bar_width, bar_height), border_radius=3
            )

            effective_width = int(bar_width * (win_rate / 100))
            pygame.draw.rect(
                self.screen, (100, 200, 100),
                (bar_x, bar_y, effective_width, bar_height), border_radius=3
            )

    def draw_buttons(self):
        """Dibuja los botones interactivos de la interfaz."""
        mouse_pos = pygame.mouse.get_pos()

        # Botón Nuevo Juego CENTRADO
        if self.new_game_button.collidepoint(mouse_pos):
            button_color = (30, 160, 80)
        else:
            button_color = (30, 140, 70)

        pygame.draw.rect(self.screen, button_color,
                         self.new_game_button, border_radius=6)

        text = font_small.render("NUEVO JUEGO", True, WHITE)
        self.screen.blit(
            text,
            (self.new_game_button.centerx - text.get_width() // 2,
             self.new_game_button.centery - text.get_height() // 2)
        )

    def get_cell_from_pos(self, pos):
        """
        Convierte coordenadas de pantalla a coordenadas de celda del tablero.
        """
        x, y = pos
        if (BOARD_OFFSET_X <= x <= BOARD_OFFSET_X + BOARD_WIDTH and
                BOARD_OFFSET_Y <= y <= BOARD_OFFSET_Y + BOARD_HEIGHT):
            col = (x - BOARD_OFFSET_X) // CELL_SIZE
            row = (y - BOARD_OFFSET_Y) // CELL_SIZE
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return row, col
        return None

    def run(self):
        """Bucle principal del juego que maneja eventos y actualizaciones."""
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Botón nuevo juego
                    if self.new_game_button.collidepoint(mouse_pos):
                        self.state.reset()

                    # Movimiento del humano
                    if (not self.state.game_over and
                            not self.state.ia_thinking and
                            self.state.current_player == 'X'):
                        cell = self.get_cell_from_pos(mouse_pos)
                        if cell and self.state.make_move(*cell, 'X'):
                            self.state.winner = self.state.check_winner()
                            if self.state.winner:
                                self.state.game_over = True
                                self.state.agent.update_stats(
                                    self.state.winner
                                )
                            else:
                                self.state.current_player = 'O'
                                self.state.ia_thinking = True

            # Dibujar todo
            self.draw_background()
            self.draw_board()
            self.draw_game_status()
            self.draw_stats()
            self.draw_buttons()

            # Turno de la IA
            if (not self.state.game_over and
                    self.state.current_player == 'O' and
                    self.state.ia_thinking):
                pygame.display.flip()
                pygame.time.delay(500)

                best_move = self.state.agent.get_best_move(
                    self.state.board
                )

                if best_move:
                    self.state.make_move(best_move[0], best_move[1], 'O')
                    self.state.winner = self.state.check_winner()
                    if self.state.winner:
                        self.state.game_over = True
                        self.state.agent.update_stats(self.state.winner)
                    else:
                        self.state.current_player = 'X'

                self.state.ia_thinking = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GameGUI()
    game.run()