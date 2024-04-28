import pygame

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAYER_ONE_COLOR = (0, 130, 255)
PLAYER_TWO_COLOR = (0, 180, 0)


class Renderer:

    def __init__(self, square_size, column, row, player_1, player_2):
        self.font = None
        self.screen = None
        self.square_size = square_size
        self.width_offset = 4
        self.height_offset = 2
        self.width = (column + self.width_offset) * square_size
        self.height = (row + self.height_offset) * square_size
        self.window_size = (self.width, self.height)
        self.player_1 = player_1
        self.player_2 = player_2
        self.action_button = None
        self.buttons = None
        pygame.init()
        pygame.fastevent.init()
        self.screen = pygame.display.set_mode(self.window_size)
        self.font = pygame.font.SysFont("monospace", 40)
        icon = pygame.image.load("assets/4C.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption('4 Connect Tournament by Coding Buddies')

    def init_board(self, board):
        self.__draw_background()
        self.__draw_blocks(board)
        self.draw_chips(board)
        self.__draw_speed_buttons()

    def draw_chips(self, board):
        for c in range(board.get_columns_amount()):
            for r in range(board.get_row_amount()):
                if board.get_field()[r][c] == self.player_1.get_id():
                    self.__draw_square_img("assets/blue_chip.png", c, r)
                elif board.get_field()[r][c] == self.player_2.get_id():
                    self.__draw_square_img("assets/green_chip.png", c, r)
        pygame.display.update()

    def draw_player_names(self, color_1=PLAYER_ONE_COLOR, color_2=PLAYER_TWO_COLOR):
        self.__draw_text(str(self.player_1.get_name()), color_1, "topleft", (10, 10), self.font)
        self.__draw_text(str(self.player_2.get_name()), color_2, "topright", (self.width - 10, 10), self.font)

    def draw_wins_amount(self):
        self.__draw_text(str(self.player_1.get_wins()), PLAYER_ONE_COLOR, "topleft", (10, 50), self.font)
        self.__draw_text(str(self.player_2.get_wins()), PLAYER_TWO_COLOR, "topright", (self.width - 10, 50), self.font)

    def hype_winner(self, player):
        line_height = 120
        x = self.width // 2
        y = (self.height // 2) - (line_height // 2)
        winner_font = pygame.font.Font(None, line_height)
        lines = ["Winner is", player.get_name()]
        winner_text = []
        for line in lines:
            text = winner_font.render(line, True, WHITE)
            winner_text.append(text)

        for text in winner_text:
            winner_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, winner_rect)
            y += line_height

        pygame.display.update()

    def draw_winner_move(self, move):
        radius = self.square_size // 2
        for f in move:
            pygame.draw.circle(self.screen, RED, (
                int((f[1] + (self.width_offset // 2)) * self.square_size + self.square_size / 2),
                self.height - int((f[0] + (self.height_offset // 2)) * self.square_size + self.square_size / 2)),
                               radius, 4)
        pygame.display.update()

    def draw_invalid_move(self, column, winner):
        top = 5.5
        if winner.get_id() == self.player_1.get_id():
            self.__draw_square_img("assets/green_chip.png", column, top)
        else:
            self.__draw_square_img("assets/blue_chip.png", column, top)
        self.__draw_square_img("assets/cross.png", column, top)
        pygame.display.update()

    def draw_start_screen(self, rounds):
        inner_boarder = 20
        bold_font = pygame.font.SysFont("monospace", 40, bold=True)

        self.__draw_background()
        self.__draw_header("Upcoming Match", inner_boarder, bold_font)

        self.__draw_text("Game Rounds: " + str(rounds), WHITE, "topleft",
                         (inner_boarder, 250), self.font)

        self.__draw_action_button("Start Game")
        pygame.display.update()

    def draw_summary(self, game_statistic):
        inner_boarder = 20
        bold_font = pygame.font.SysFont("monospace", 40, bold=True)

        self.__draw_background()
        self.__draw_header("Game Summary", inner_boarder, bold_font)

        self.__draw_text("Wins: " + str(game_statistic.get_total_wins(self.player_1)), WHITE, "topleft",
                         (inner_boarder, 250), self.font)
        self.__draw_text("Wins: " + str(game_statistic.get_total_wins(self.player_2)), WHITE, "topright",
                         (self.width - inner_boarder, 250), self.font)

        self.__draw_text("Ratio: " + str(game_statistic.get_win_ratio(self.player_1)), WHITE, "topleft",
                         (inner_boarder, 320),
                         self.font)
        self.__draw_text("Ratio: " + str(game_statistic.get_win_ratio(self.player_2)), WHITE, "topright",
                         (self.width - inner_boarder, 320), self.font)

        winner = game_statistic.get_winner()
        if not winner:
            self.__draw_text("Draw!", WHITE, "center", (self.width // 2, 500), bold_font)
        elif winner.get_id() == self.player_1.get_id():
            self.__draw_text("WINNER IS: " + self.player_1.get_name(), PLAYER_ONE_COLOR, "center",
                             (self.width // 2, 500), bold_font)
        else:
            self.__draw_text("WINNER IS: " + self.player_2.get_name(), PLAYER_TWO_COLOR, "center",
                             (self.width // 2, 500), bold_font)

        self.__draw_action_button("quit")
        pygame.display.update()

    def __draw_header(self, header_text, inner, bold_font):
        big_bold_font = pygame.font.SysFont("monospace", 70, bold=True)

        self.__draw_text(header_text, WHITE, "center", (self.width // 2, 50), big_bold_font)

        self.__draw_text(self.player_1.get_name(), PLAYER_ONE_COLOR, "topleft", (inner, 150), bold_font)
        self.__draw_text("vs", WHITE, "center", (self.width // 2, 150), self.font)
        self.__draw_text(self.player_2.get_name(), PLAYER_TWO_COLOR, "topright", (self.width - inner, 150),
                         bold_font)

        pygame.draw.line(self.screen, WHITE, (30, 200), (self.width - 30, 200))

    def has_user_emit_button(self, event):
        return self.action_button.collidepoint(event.pos)

    def __draw_blocks(self, board):
        for c in range(board.get_columns_amount()):
            for r in range(board.get_row_amount()):
                self.__draw_square_img("assets/block_empty.png", c, r)
        pygame.display.update()

    def __draw_background(self):
        image = pygame.image.load("assets/background.png")
        scaled_image = pygame.transform.scale(image, (self.width, self.height))
        image_rect = scaled_image.get_rect()
        image_rect.center = (self.width // 2, self.height // 2)
        self.screen.blit(scaled_image, image_rect.topleft)

    def __draw_text(self, text, color, position_type, position_params, font):
        text_object = font.render(text, True, color)
        match position_type:
            case "topleft":
                text_rect = text_object.get_rect(topleft=position_params)
            case "topright":
                text_rect = text_object.get_rect(topright=position_params)
            case _:
                text_rect = text_object.get_rect(center=position_params)
        self.screen.blit(text_object, text_rect)

    def __draw_square_img(self, image_path, column, row):
        image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(image, (self.square_size, self.square_size))
        image_rect = scaled_image.get_rect()
        image_rect.center = (
            int((column + (self.width_offset // 2)) * self.square_size + self.square_size / 2),
            self.height - int((row + (self.height_offset // 2)) * self.square_size + self.square_size / 2))
        self.screen.blit(scaled_image, image_rect.topleft)

    def __draw_action_button(self, action):
        quit_button_font = pygame.font.Font(None, 36)
        quit_button_text = quit_button_font.render(action, True, WHITE)
        self.action_button = quit_button_text.get_rect(center=(self.width // 2, 600))

        pygame.draw.rect(self.screen, RED,
                         (self.action_button.x - 10, self.action_button.y - 10, self.action_button.width + 20,
                          self.action_button.height + 20),
                         border_radius=10)
        self.screen.blit(quit_button_text, self.action_button)

    def __draw_speed_buttons(self):
        self.buttons = pygame.sprite.Group()
        button_configs = [("Pause", "assets/pause.png"), ("Play", "assets/play.png"), ("Faster", "assets/forward.png")]
        x_coord = self.width / 2 - 50
        for config in button_configs:
            button = pygame.sprite.Sprite()
            button.name = config[0]
            button.image = pygame.image.load(config[1]).convert_alpha()
            button.rect = button.image.get_rect()
            button.rect.center = (x_coord, 50)
            x_coord += 50
            self.buttons.add(button)

        self.buttons.draw(self.screen)

    def is_speed_button_pressed(self):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.rect.left < pos[0] < button.rect.right and button.rect.top < pos[1] < button.rect.bottom:
                return button.name

