import arcade

import FieldDesign
import constants


class MainMenuScreen(FieldDesign.LevelScreen):

    def __init__(self, theme):
        super().__init__(theme)
        self.snake_track = ((4, 36), (21, 37), (22, 28), (5, 27))
        self.letter_s_col = theme['S']
        self.letter_n_col = theme['N']
        self.letter_a_col = theme['A']
        self.letter_k_col = theme['K']
        self.letter_e_col = theme['E']
        self.arcade = theme['arcade']
        self.small_text_col = theme['small_text']
        self.timer = 0

    def create_menu_board(self, colour):
        menu_board = arcade.create_rectangle_filled(
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2,
            constants.SCREEN_WIDTH - (constants.CELL * 2),
            constants.SCREEN_HEIGHT - (constants.CELL * 2),
            colour
            )
        return menu_board

    def create_menu_board_outline(self, colour):
        menu_board_outline = arcade.create_rectangle_outline(
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2,
            constants.SCREEN_WIDTH - (constants.CELL * 2),
            constants.SCREEN_HEIGHT - (constants.CELL * 2),
            colour,
            2
            )
        return menu_board_outline

    def draw_title(self, col_s, col_n, col_a, col_k, col_e, col_arc):
        """Draw text for the game title."""
        arcade.draw_text('S', 125 + 30, 300, col_s,
                         75, font_name=self.font)
        arcade.draw_text('N', 185 + 30, 300, col_n,
                         75, font_name=self.font)
        arcade.draw_text('A', 250 + 30, 300, col_a,
                         75, font_name=self.font)
        arcade.draw_text('K', 315 + 30, 300, col_k,
                         75, font_name=self.font)
        arcade.draw_text('E', 380 + 30, 300, col_e,
                         75, font_name=self.font)


    def create_shapes(self):
        shape_list = arcade.ShapeElementList()
        border_wall = self.create_border_wall(self.fg_col)
        menu_board = self.create_menu_board(self.bg_col)
        menu_board_outline = self.create_menu_board_outline(self.bg_col)
        shape_list.append(border_wall)
        shape_list.append(menu_board)
        shape_list.append(menu_board_outline)
        return shape_list

    def draw_instructions(self, colour):
        arcade.draw_text('Press Enter to Start', 100, 500, colour,
                         16, font_name=self.font)


    def draw(self):
        self.shape_list.draw()
        self.draw_instructions(self.small_text_col)
        self.draw_title(self.letter_s_col, self.letter_n_col,
                        self.letter_a_col, self.letter_k_col,
                        self.letter_e_col, self.arcade)
