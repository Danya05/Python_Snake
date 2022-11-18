import arcade

import constants


class LevelScreen():

    def __init__(self, theme):
        self.bg_col = theme['bg']
        self.fg_col = theme['fg']
        self.board_col = theme['board']
        self.scoreboard_col = theme['scoreboard']
        self.score_text_col = theme['score_text']
        self.score_num_col = theme['score_num']
        self.font = 'prolamina_2_update'
        self.shape_list = self.create_shapes()

    def create_border_wall(self, colour):
        border_wall = arcade.create_rectangle_outline(
            constants.SCREEN_HEIGHT / 2,
            constants.SCREEN_HEIGHT / 2,
            constants.SCREEN_HEIGHT - (constants.CELL * 2),
            constants.SCREEN_HEIGHT - (constants.CELL * 2),
            colour,
            8
            )
        return border_wall

    def create_scoreboard_backing(self, colour):
        scoreboard_backing = arcade.create_rectangle_filled(
            constants.SCREEN_HEIGHT / 2,
            (constants.SCREEN_HEIGHT - constants.CELL * 4)
            + constants.CELL / 2,
            constants.SCREEN_HEIGHT - (constants.CELL * 1.875),
            constants.CELL * 5.125,
            colour
            )
        return scoreboard_backing

    def create_scoreboard_overlay(self, colour):
        scoreboard_overlay = arcade.create_rectangle_filled(
            constants.SCREEN_HEIGHT / 2,
            (constants.SCREEN_HEIGHT - constants.CELL * 4)
            + constants.CELL / 2,
            constants.SCREEN_HEIGHT - (constants.CELL * 1.75),
            constants.CELL * 5.125,
            self.get_overlay_values(colour, 50)
            )
        return scoreboard_overlay

    def create_divider(self, colour):
        divider = arcade.create_line(
             constants.CELL - (constants.CELL / 8),
             constants.SCREEN_HEIGHT - (constants.CELL * 6),
             constants.SCREEN_HEIGHT - (constants.CELL - (constants.CELL / 8)),
             constants.SCREEN_HEIGHT - (constants.CELL * 6),
             colour,
             8)
        return divider

    def create_game_board(self, colour):
        game_board = arcade.create_rectangle_filled(
            constants.SCREEN_HEIGHT / 2,
            ((constants.SCREEN_HEIGHT / 2) - (constants.CELL * 3))
            + constants.CELL / 2,
            constants.SCREEN_HEIGHT - (constants.CELL * 2),
            constants.SCREEN_HEIGHT - (constants.CELL * 7),
            colour
            )
        return game_board

    def create_game_board_outline(self, colour):
        game_board_outline = arcade.create_rectangle_outline(
            constants.SCREEN_HEIGHT / 2,
            ((constants.SCREEN_HEIGHT / 2) - (constants.CELL * 3))
            + constants.CELL / 2,
            constants.SCREEN_HEIGHT - (constants.CELL * 2),
            constants.SCREEN_HEIGHT - (constants.CELL * 7),
            colour,
            2
            )
        return game_board_outline

    def get_overlay_values(self, input_colour, alpha):
        start_colour = list(input_colour)
        start_colour.append(alpha)
        output_colour = tuple(start_colour)
        return output_colour

    def create_shapes(self):
        shape_list = arcade.ShapeElementList()
        border_wall = self.create_border_wall(self.fg_col)
        scoreboard_backing = self.create_scoreboard_backing(
            self.scoreboard_col)
        scoreboard_overlay = self.create_scoreboard_overlay(self.fg_col)
        divider = self.create_divider(self.fg_col)
        game_board = self.create_game_board(self.bg_col)
        game_board_outline = self.create_game_board_outline(self.bg_col)
        shape_list.append(border_wall)
        shape_list.append(scoreboard_backing)
        shape_list.append(scoreboard_overlay)
        shape_list.append(divider)
        shape_list.append(game_board)
        shape_list.append(game_board_outline)
        return shape_list

    def draw_score_text(self, colour):
        arcade.draw_text('SCORE:', 20, 564, colour,
                         40, font_name=self.font)

    def draw_score_num(self, score, colour):
        arcade.draw_text(score, 400, 564, colour,
                         30, font_name=self.font)

    def draw(self, score):
        self.shape_list.draw()
        self.draw_score_text(self.score_text_col)
        self.draw_score_num(score, self.score_num_col)
