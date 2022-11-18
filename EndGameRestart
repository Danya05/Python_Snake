import arcade

import FieldDesign
import constants


class GameOverScreen(FieldDesign.LevelScreen):

    def __init__(self, theme):
        super().__init__(theme)
        self.game_over_text_col = theme['game_over']
        self.small_text_col = theme['food']

    def update_theme(self, theme):
        self.bg_col = theme['bg']
        self.fg_col = theme['fg']
        self.game_over_text_col = theme['game_over']
        self.small_text_col = theme['food']
        self.shape_list = self.create_shapes()

    def create_message_box(self, colour):
        message_box = arcade.create_rectangle_filled(
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + constants.CELL,
            constants.SCREEN_WIDTH - (constants.CELL * 10),
            (constants.SCREEN_HEIGHT / 2) - (constants.CELL * 7),
            colour
            )
        return message_box

    def create_message_box_overlay(self, colour):
        message_box_overlay = arcade.create_rectangle_filled(
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + constants.CELL,
            constants.SCREEN_WIDTH - (constants.CELL * 10),
            (constants.SCREEN_HEIGHT / 2) - (constants.CELL * 7),
            self.get_overlay_values(colour, 50)
            )
        return message_box_overlay

    def create_message_box_outline(self, colour):
        message_box_outline = arcade.create_rectangle_outline(
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + constants.CELL,
            constants.SCREEN_WIDTH - (constants.CELL * 10),
            (constants.SCREEN_HEIGHT / 2) - (constants.CELL * 7),
            colour,
            6
            )
        return message_box_outline

    def create_shapes(self):
        shape_list = arcade.ShapeElementList()
        game_board_overlay = self.create_game_board(
            self.get_overlay_values(self.bg_col, 192)
            )
        game_board_overlay_outline = self.create_game_board_outline(
            self.get_overlay_values(self.bg_col, 192)
        )
        message_box_outline = self.create_message_box_outline(self.fg_col)
        message_box = self.create_message_box(self.bg_col)
        message_box_overlay = self.create_message_box_overlay(self.fg_col)
        shape_list.append(game_board_overlay)
        shape_list.append(game_board_overlay_outline)
        shape_list.append(message_box_outline)
        shape_list.append(message_box)
        shape_list.append(message_box_overlay)
        return shape_list

    def draw_game_over(self, colour):
        arcade.draw_text('GAME', 190, 350, colour,
                         64, font_name=self.font)
        arcade.draw_text('OVER', 190, 250, colour,
                         64, font_name=self.font)

    def draw_restart(self, colour):
        arcade.draw_text('RESTART Y/N?', 100, 200, colour,
                         16, font_name=self.font)

    def draw(self):
        self.shape_list.draw()
        self.draw_game_over(self.game_over_text_col)
        self.draw_restart(self.small_text_col)
