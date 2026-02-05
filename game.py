import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        screen_flags = pygame.SHOWN
        screen_size = (700, 500)
        self.screen = pygame.display.set_mode(size=screen_size, flags=screen_flags)

        # Tła
        self.left_display = pygame.Surface(size=(350, 500))
        self.right_display = pygame.Surface(size=(350, 500))
        self.clock = pygame.time.Clock()

        # Grafiki
        self.grid = pygame.image.load("files/grid.png").convert_alpha()
        self.grid_pos = (
            350 - self.grid.get_width() / 2,
            250 - self.grid.get_height() / 2 + 30,
        )

        # Teksty (Tylko statyczne)
        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.text_player1 = self.font.render("Player 1\n\n       X", True, "#000000")
        self.text_player2 = self.font.render("Player 2\n\n       O", True, "#000000")

    def run(self):
        self.left_display.fill("#BC3E3E")
        self.right_display.fill("#4C8947")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Rysowanie
            self.screen.blit(source=self.left_display, dest=(0, 0))
            self.screen.blit(source=self.right_display, dest=(350, 0))
            self.screen.blit(source=self.grid, dest=self.grid_pos)

            # Podstawowe teksty
            self.screen.blit(source=self.text_player1, dest=(40, 350))
            self.screen.blit(
                source=self.text_player2,
                dest=(660 - self.text_player2.get_width(), 350),
            )

            pygame.display.update()
            self.clock.tick(20)


Game().run()
