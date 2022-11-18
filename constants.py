import arcade

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Snake Game"
CELL = 16

STR = SCREEN_HEIGHT // CELL
COL = SCREEN_WIDTH // CELL

BOARD_LEFT = 2
BOARD_RIGHT = COL - 1
BOARD_UP = STR - 6
BOARD_DOWN = 2

CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 3

BACKGROUND_COLOR = arcade.csscolor.FOREST_GREEN
OUTLINE_COLOR = arcade.csscolor.SADDLE_BROWN
SNAKE_COLOR = arcade.csscolor.RED
EYES_COLOR = arcade.csscolor.BLUE

FPS = 60

col_1 = (0, 255, 145)
col_2 = (160, 255, 145)
col_3 = (215, 255, 145)
col_purple = (34, 4, 70)
col_tint = (89, 67, 116)
white = (255, 255, 255)

gr = {'board': col_purple,
          'bg': col_purple,
          'fg': col_tint,
          'head': col_1,
          'eye': col_1,
          'pupil': col_purple,
          'snake_body_1': col_2,
          'snake_body_2': col_3,
          'snake_body_3': col_1,
          'snake_border': col_purple,
          'food': white,
          'food_border': col_purple,
          'scoreboard': col_purple,
          'score_text': col_1,
          'score_num': white,
          'game_over': col_1,
          'small_text': white,
          'arcade': white,
          'S': col_1,
          'N': col_2,
          'A': col_3,
          'K': col_2,
          'E': col_1
          }

themes = [gr]
