import sys
from datetime import datetime

import pygame
from pygame import Surface, Rect
from pygame.constants import K_RETURN, K_BACKSPACE, KEYDOWN, K_ESCAPE
from pygame.font import Font

from Const import C_YELLOW, WIN_WIDTH, SCORE_POS, MENU_OPTION, C_WHITE
from code.DBProxy import DBProxy


class Score:

    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, game_mode: str, player_score: list[int]):

        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)

        db_proxy = DBProxy('DBScore')
        name = ""

        # -------- DEFINIÇÃO SEGURA DE SCORE E TEXTO --------
        if game_mode == MENU_OPTION[0]:
            score = player_score[0]
            text = "Enter Player 1 name (4 characters)"

        elif game_mode == MENU_OPTION[1]:
            score = (player_score[0] + player_score[1]) / 2
            text = "Enter Team name (4 characters)"

        elif game_mode == MENU_OPTION[2]:
            if player_score[0] >= player_score[1]:
                score = player_score[0]
                text = "Enter Player 1 name (4 characters)"
            else:
                score = player_score[1]
                text = "Enter Player 2 name (4 characters)"

        # ---------------- LOOP PRINCIPAL ----------------
        while True:

            self.window.blit(self.surf, self.rect)

            self.score_text(
                50,
                "YOU WIN!!",
                C_YELLOW,
                SCORE_POS['Title']
            )

            self.score_text(
                15,
                text,
                C_WHITE,
                SCORE_POS['EnterName']
            )

            self.score_text(
                15,
                name,
                C_WHITE,
                SCORE_POS['Name']
            )

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == K_RETURN and len(name) == 4:
                        db_proxy.save({
                            'name': name,
                            'score': int(score),
                            'date': get_formatted_date()
                        })
                        self.show()
                        return

                    elif event.key == K_BACKSPACE:
                        name = name[:-1]

                    elif event.unicode.isprintable() and len(name) < 4:
                        name += event.unicode

            pygame.display.flip()
            pass

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(self.surf, self.rect)
        self.score_text(
            48,
            "TOP 10 SCORE",
            C_YELLOW,
            SCORE_POS['Title']
        )
        self.score_text(
            20,
            "NAME     SCORE          DATE       ",
            C_YELLOW,
            SCORE_POS['Label']
        )
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player in list_score:
            id_,name,score,date = player
            self.score_text(
                20,
                f'{name}     {score: 05d}      {date}',
                C_YELLOW,
                SCORE_POS[list_score.index(player)]
            )
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()


    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):

        text_font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)

        text_surf = text_font.render(
            text,
            True,
            text_color
        ).convert_alpha()

        text_rect = text_surf.get_rect(center=text_center_pos)

        self.window.blit(text_surf, text_rect)


def get_formatted_date():
    now = datetime.now()
    return now.strftime("%H:%M - %d/%m/%y")