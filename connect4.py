import pygame
import sys
from engine import Engine

pygame.font.init()
engine = Engine()

# All values are hard coded

class Connect4():
    def __init__(self) -> None:
        self.color_key = {1: (250, 50, 50), -1: (225, 210, 65), 0: (255, 255, 255)}

        self.screen = pygame.display.set_mode((491, 423))  
        pygame.display.set_caption("Connect 4")

        self.slots_centers_list = [[((j * 70) + 36, (i * 70) + 38) for j in range(7)] for i in range(6)]
        self.slots_list = [[pygame.draw.circle(self.screen, self.color_key[0], self.slots_centers_list[i][j], 28) for j in range(7)] for i in range(6)]
        self.occupied_list = []
        self.buttons_list = [pygame.Rect(140, 100, 90, 30), pygame.Rect(250, 100, 90, 30)]

        self.player_color = None  
        self.computer_color = None 

        self.font = pygame.font.SysFont("Arial", 30)

    def reset_screen(self) -> None:
        self.screen.fill("blue")
        for i in range(6):
            for j in range(7):
                pygame.draw.circle(self.screen, self.color_key[0], self.slots_centers_list[i][j], 28)
        engine.reset()
        self.occupied_list = []

    def drop_piece(self, color_code, center, s) -> None:
        pygame.draw.circle(self.screen, self.color_key[color_code], center, 28)
        self.occupied_list.append(s)

    def ask_for_color(self) -> None:
        self.screen.fill("white")

        self.screen.blit(self.font.render("Which color do you want to play as?", False, (0, 0, 0)), (5, 10))
        self.screen.blit(self.font.render("red", False, (0, 0, 0)), (160, 60))
        self.screen.blit(self.font.render("yellow", False, (0, 0, 0)), (250, 60))

        pygame.draw.rect(self.screen, self.color_key[1], (140, 100, 90, 30))
        pygame.draw.rect(self.screen, self.color_key[-1], (250, 100, 90, 30))

        pygame.display.update()

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for i in range(2):
                            if self.buttons_list[i].collidepoint(event.pos):
                                self.screen.fill("white")
                                if i == 0:
                                    self.player_color = 1
                                    self.computer_color = -1
                                else:
                                    self.player_color = -1
                                    self.computer_color = 1
                                return None

            pygame.time.wait(30)

    def should_end_game(self) -> bool:
        is_draw = engine.is_draw()
        if (engine.check_for_winner() in (1, -1)) or is_draw:
            if is_draw:
                end_message = "Draw!"
            elif self.to_move == "player":
                end_message = "Computer Wins!"
            elif self.to_move == "computer":
                end_message = "Player Wins!"

            self.screen.blit(self.font.render(end_message, False, (0, 0, 0)), (140, 10))
            pygame.display.update()
            pygame.time.wait(2000)
            return True
        return False

    def clean_up(self) -> None:
        engine.reset() 
        self.reset_screen()
        self.occupied_list = []
        pygame.display.update()

    def run(self) -> None:
        self.ask_for_color()
        self.reset_screen()

        if self.player_color == 1:
            self.to_move = 'player'
        else:
            self.to_move = 'computer'

        pygame.display.update()

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.to_move == 'player' and event.type == pygame.MOUSEBUTTONUP:
                    for i in range(6):
                        for j in range(7):
                            if self.slots_list[i][j].collidepoint(event.pos) and ((i, j) not in self.occupied_list):

                                    if engine.make_move((i, j)):
                                        self.drop_piece(self.player_color, self.slots_centers_list[i][j], (i, j))
                                        self.to_move = 'computer'

                                        if self.should_end_game():
                                            self.clean_up()
                                            return True
                                         
                                        pygame.display.update()
                                        break

                if self.to_move == 'computer':
                    best_move = engine.get_best_move()
                    try:
                        if best_move == None:
                            i, j = engine.get_all_valid_moves[1]
                        else:
                            i, j = best_move

                        engine.make_move((i, j))   
                        self.drop_piece(self.computer_color, self.slots_centers_list[i][j], (i, j))
                        self.to_move = 'player'

                        if self.should_end_game():
                            self.clean_up()
                            return True

                        pygame.display.update()

                    except TypeError:
                        self.to_move = "computer"

                pygame.time.wait(30)

if __name__ == "__main__":
    connect4 = Connect4()
    while True:
        connect4.run()