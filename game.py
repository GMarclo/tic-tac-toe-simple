import pygame
import sys
import random


# info
# grid size = 400 x 400
# white cell size = 128 x 128
# cross and circle size = 100 x 100
# window size = 700 x 500
# black lines width: 3, 5, 5, 3


class Game:
    def __init__(self):
        # base setup
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        screen_flags = pygame.SHOWN  # | pygame.NOFRAME
        screen_size = (100 * 7, 100 * 5)
        self.screen_scale = 1
        self.screen = pygame.display.set_mode(size=screen_size, flags=screen_flags)
        self.left_display = pygame.Surface(
            size=(self.screen.get_width() / 2, self.screen.get_height())
        )
        self.right_display = pygame.Surface(
            size=(self.screen.get_width() / 2, self.screen.get_height())
        )
        self.clock = pygame.time.Clock()

        # game variables setup
        self.sum_of_moves = 0
        self.turn = random.randint(0, 1)
        self.win_lines_pos = []
        self.start = True
        self.grid_filling = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # graphics setup
        self.grid = pygame.image.load("files/grid.png").convert_alpha()
        self.cross = pygame.image.load("files/cross.png").convert_alpha()
        self.circle = pygame.image.load("files/circle.png").convert_alpha()

        self.grid_pos = (
            self.screen.get_width() / 2 - self.grid.get_width() / 2,
            self.screen.get_height() / 2 - self.grid.get_height() / 2 + 30,
        )

        self.mark_bias = (14, 14)

        self.selected_square_pos = (-1, -1)

        self.white_cells_pos = {
            (0, 0): [3, 3],
            (1, 0): [136, 3],
            (2, 0): [269, 3],
            (0, 1): [3, 136],
            (1, 1): [136, 136],
            (2, 1): [269, 136],
            (0, 2): [3, 269],
            (1, 2): [136, 269],
            (2, 2): [269, 269],
        }
        for key in self.white_cells_pos:
            self.white_cells_pos[key][0] += self.grid_pos[0]
            self.white_cells_pos[key][1] += self.grid_pos[1]

        self.selected_square = pygame.Surface(size=(128, 128))
        self.selected_square.fill("#468FC7")
        self.selected_square.set_alpha(100)

        # text setup

        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.text_player1 = self.font.render("Player 1\n\n       X", True, "#000000")
        self.text_player2 = self.font.render("Player 2\n\n       O", True, "#000000")
        self.font_title = pygame.font.Font("freesansbold.ttf", 28)
        self.middle_text = self.font_title.render(
            f"Player {2-self.turn} makes move", True, "#000000"
        )

    def check_win(self):
        for i in range(0, 3):
            if abs(sum(self.grid_filling[i])) == 3:
                self.start = False
                self.middle_text = self.font_title.render(
                    f"Player {2-(self.turn + 1) % 2} win! Press Enter to start new game.",
                    True,
                    "#000000",
                )
                self.win_lines_pos.append(((i, 0), (i, 2)))
            if (
                abs(
                    self.grid_filling[0][i]
                    + self.grid_filling[1][i]
                    + self.grid_filling[2][i]
                )
                == 3
            ):
                self.start = False
                self.middle_text = self.font_title.render(
                    f"Player {2-(self.turn + 1) % 2} win! Press Enter to start new game.",
                    True,
                    "#000000",
                )
                self.win_lines_pos.append(((0, i), (2, i)))
        if (
            abs(
                self.grid_filling[0][0]
                + self.grid_filling[1][1]
                + self.grid_filling[2][2]
            )
            == 3
        ):
            self.start = False
            self.middle_text = self.font_title.render(
                f"Player {2-(self.turn + 1) % 2} win! Press Enter to start new game.",
                True,
                "#000000",
            )
            self.win_lines_pos.append(((0, 0), (2, 2)))
        if (
            abs(
                self.grid_filling[2][0]
                + self.grid_filling[1][1]
                + self.grid_filling[0][2]
            )
            == 3
        ):
            self.start = False
            self.middle_text = self.font_title.render(
                f"Player {2-(self.turn + 1) % 2} win! Press Enter to start new game.",
                True,
                "#000000",
            )
            self.win_lines_pos.append(((2, 0), (0, 2)))

        if self.start and self.sum_of_moves == 9:
            self.start = False
            self.middle_text = self.font_title.render(
                f"Draw! Press Enter to start new game.", True, "#000000"
            )

    def fill_cell_if_possible(self):
        if self.selected_square_pos == (-1, -1) or not self.start:
            return
        x = self.selected_square_pos[0]
        y = self.selected_square_pos[1]
        if self.grid_filling[x][y] == 0 and self.turn == 1:
            self.grid_filling[x][y] = 1
            self.sum_of_moves += 1
            self.turn = (self.turn + 1) % 2
        elif self.grid_filling[x][y] == 0 and self.turn == 0:
            self.grid_filling[x][y] = -1
            self.sum_of_moves += 1
            self.turn = (self.turn + 1) % 2
        self.check_win()

    def draw_filled_cells(self):
        for x in range(0, 3):
            for y in range(0, 3):
                if self.grid_filling[x][y]:
                    if self.grid_filling[x][y] > 0:
                        self.screen.blit(
                            source=self.cross,
                            dest=(
                                self.white_cells_pos[(x, y)][0] + self.mark_bias[0],
                                self.white_cells_pos[(x, y)][1] + self.mark_bias[1],
                            ),
                        )
                    else:
                        self.screen.blit(
                            source=self.circle,
                            dest=(
                                self.white_cells_pos[(x, y)][0] + self.mark_bias[0],
                                self.white_cells_pos[(x, y)][1] + self.mark_bias[1],
                            ),
                        )

    def draw_basic_texts(self):
        self.screen.blit(source=self.text_player1, dest=(40, 350))
        self.screen.blit(
            source=self.text_player2,
            dest=(self.screen.get_width() - 40 - self.text_player2.get_width(), 350),
        )
        if self.start:
            self.middle_text = self.font_title.render(
                f"Player {2-self.turn} makes move", True, "#000000"
            )
        self.screen.blit(
            source=self.middle_text,
            dest=(self.screen.get_width() / 2 - self.middle_text.get_width() / 2, 30),
        )

    def run(self):
        self.left_display.fill("#BC3E3E")
        self.right_display.fill("#4C8947")
        while True:
            cursor_pos = pygame.mouse.get_pos()

            if (
                cursor_pos[0] > self.grid_pos[0]
                and cursor_pos[0] < self.grid_pos[0] + self.grid.get_width()
                and cursor_pos[1] > self.grid_pos[1]
                and cursor_pos[1] < self.grid_pos[1] + self.grid.get_height()
            ):
                self.selected_square_pos = (
                    int((cursor_pos[0] - 151) / 133),
                    int((cursor_pos[1] - 81) / 133),
                )
            else:
                self.selected_square_pos = (-1, -1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN and not self.start:
                        self.start = True
                        self.sum_of_moves = 0
                        self.turn = random.randint(0, 1)
                        self.win_lines_pos = []
                        self.grid_filling = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                        self.middle_text = self.font.render(
                            f"Player {2-self.turn} makes move", True, "#000000"
                        )
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.fill_cell_if_possible()

            self.screen.blit(source=self.left_display, dest=(0, 0))
            self.screen.blit(
                source=self.right_display, dest=(self.screen.get_width() / 2, 0)
            )
            self.screen.blit(
                source=self.grid,
                dest=self.grid_pos,
            )

            self.draw_basic_texts()

            self.draw_filled_cells()

            if (
                self.selected_square_pos != (-1, -1)
                and not self.grid_filling[self.selected_square_pos[0]][
                    self.selected_square_pos[1]
                ]
                and self.start
            ):
                self.screen.blit(
                    source=self.selected_square,
                    dest=self.white_cells_pos[self.selected_square_pos],
                )

            if not self.start:
                for pos_1, pos_2 in self.win_lines_pos:
                    pygame.draw.line(
                        surface=self.screen,
                        color="#00A3EE",
                        start_pos=(
                            self.white_cells_pos[pos_1][0] + 64,
                            self.white_cells_pos[pos_1][1] + 64,
                        ),
                        end_pos=(
                            self.white_cells_pos[pos_2][0] + 64,
                            self.white_cells_pos[pos_2][1] + 64,
                        ),
                        width=10,
                    )

            pygame.display.update()
            self.clock.tick(20)


Game().run()
