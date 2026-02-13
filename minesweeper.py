import pygame
import random
import sys

pygame.init()

CELL_SIZE = 60
GRID_WIDTH = 16
GRID_HEIGHT = 16
MINES_COUNT = 40
MARGIN = 80

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE + MARGIN

COLORS = {
    "bg": (192, 192, 192),
    "cell": (128, 128, 128),
    "cell_pressed": (200, 200, 200),
    "mine": (255, 0, 0),
    "flag": (255, 0, 0),
    "1": (0, 0, 255),
    "2": (0, 128, 0),
    "3": (255, 0, 0),
    "4": (0, 0, 128),
    "5": (128, 0, 0),
    "6": (0, 128, 128),
    "7": (0, 0, 0),
    "8": (128, 128, 128),
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("踩地雷")
font = pygame.font.SysFont("arial", 30, bold=True)
big_font = pygame.font.SysFont("arial", 40, bold=True)


class Minesweeper:
    def __init__(self):
        self.reset()

    def reset(self):
        self.game_over = False
        self.won = False
        self.first_click = True
        self.start_time = None
        self.elapsed_time = 0
        self.flags = 0
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.flagged = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def place_mines(self, exclude_x, exclude_y):
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[y][x] != -1 and (x != exclude_x or y != exclude_y):
                if abs(x - exclude_x) <= 1 and abs(y - exclude_y) <= 1:
                    continue
                self.grid[y][x] = -1
                mines_placed += 1

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != -1:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                                if self.grid[ny][nx] == -1:
                                    count += 1
                    self.grid[y][x] = count

    def reveal(self, x, y):
        if self.flagged[y][x] or self.revealed[y][x]:
            return

        if self.first_click:
            self.place_mines(x, y)
            self.first_click = False
            self.start_time = pygame.time.get_ticks()

        self.revealed[y][x] = True

        if self.grid[y][x] == -1:
            self.game_over = True
            return

        if self.grid[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                        if not self.revealed[ny][nx] and not self.flagged[ny][nx]:
                            self.reveal(nx, ny)

        self.check_win()

    def toggle_flag(self, x, y):
        if self.revealed[y][x]:
            return
        self.flagged[y][x] = not self.flagged[y][x]
        if self.flagged[y][x]:
            self.flags += 1
        else:
            self.flags -= 1

    def chord(self, x, y):
        if not self.revealed[y][x]:
            return
        if self.grid[y][x] <= 0:
            return

        flag_count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                    if self.flagged[ny][nx]:
                        flag_count += 1

        if flag_count == self.grid[y][x]:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                        if not self.revealed[ny][nx] and not self.flagged[ny][nx]:
                            self.reveal(nx, ny)

    def check_win(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return
        self.won = True
        self.game_over = True

    def draw(self):
        screen.fill(COLORS["bg"])

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE
                )

                if self.revealed[y][x]:
                    pygame.draw.rect(screen, COLORS["cell_pressed"], rect)
                    pygame.draw.rect(screen, (100, 100, 100), rect, 1)

                    if self.grid[y][x] == -1:
                        pygame.draw.circle(
                            screen, COLORS["mine"], rect.center, CELL_SIZE // 3
                        )
                    elif self.grid[y][x] > 0:
                        text = font.render(
                            str(self.grid[y][x]), True, COLORS[str(self.grid[y][x])]
                        )
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, COLORS["cell"], rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
                    pygame.draw.rect(screen, (64, 64, 64), rect, 1)

                    if self.flagged[y][x]:
                        flag_points = [
                            (rect.left + 5, rect.top + 8),
                            (rect.left + 5, rect.bottom - 5),
                            (rect.right - 5, rect.centery),
                        ]
                        pygame.draw.polygon(screen, COLORS["flag"], flag_points, 2)

        if self.start_time and not self.game_over:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

        time_text = font.render(f"Time: {self.elapsed_time}", True, (0, 0, 0))
        screen.blit(time_text, (10, 15))

        mines_left = MINES_COUNT - self.flags
        mines_text = font.render(f"Mines: {mines_left}", True, (0, 0, 0))
        screen.blit(mines_text, (WIDTH - 100, 15))

        if self.game_over:
            if self.won:
                msg = big_font.render("YOU WIN!", True, (0, 200, 0))
            else:
                msg = big_font.render("GAME OVER!", True, (200, 0, 0))
            msg_rect = msg.get_rect(center=(WIDTH // 2, MARGIN // 2))
            screen.blit(msg, msg_rect)

            restart_text = font.render("Press R to restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 20))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()


def main():
    game = Minesweeper()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                x, y = event.pos
                grid_x = x // CELL_SIZE
                grid_y = (y - MARGIN) // CELL_SIZE

                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    if event.button == 1:
                        if game.revealed[grid_y][grid_x]:
                            game.chord(grid_x, grid_y)
                        else:
                            game.reveal(grid_x, grid_y)
                    elif event.button == 3:
                        game.toggle_flag(grid_x, grid_y)

        game.draw()
        clock.tick(30)


if __name__ == "__main__":
    main()
