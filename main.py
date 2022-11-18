import random
import arcade

import FieldDesign
import Player
import apples
import constants
import Design
import EndGameRestart
import type



class Game(arcade.Window):

    def __init__(self, width, height, title, fullscreen=True):
        super().__init__(width, height, title)
        super().set_update_rate(1 / constants.FPS)
        super().set_mouse_visible(False)
        self.game_state = type.GAME_STATES['main_menu']
        self.score = None
        self.themes = constants.themes
        "Пока всего один вид, возможно потом добавлю еще"
        self.theme = constants.themes[0]
        arcade.set_background_color(self.theme['bg'])
        self.mode = type.GAME_MODES['normal']


    def setup_game(self):
        self.snake_p1 = Player.Snake(
            self.theme, size=constants.CELL, speed=6,
            head_pos=[self.get_random_board_coords(pad_left=2,
                                                   pad_right=2)[0],
                      self.get_random_board_coords(pad_bottom=5,
                                                   pad_top=14)[1]]
            )
        self.spawn_food_randomly(self.snake_p1, self.food)
        self.score = Score(100, 500)

    def setup_screens(self):
        self.level = FieldDesign.LevelScreen(self.theme)
        self.main_menu = Design.MainMenuScreen(self.theme)
        self.start_title_loop = False
        self.game_over_screen = EndGameRestart.GameOverScreen(self.theme)
        self.snake_p1 = Player.Snake(self.theme, size=constants.CELL,
                                    speed=12, head_pos=[12, 27],
                                    direction='')
        self.food = apples.Food(self.theme, constants.CELL,
                              self.snake_p1, pos=[6, 27])

    def menu_mode(self, delta_time):
        if self.snake_p1.direction == '' and not self.start_title_loop:
            self.main_menu.timer += 1
            if self.main_menu.timer == 60:
                self.main_menu.timer = 0
                self.start_title_loop = True
                self.snake_p1.direction = 'LEFT'
        if self.snake_p1.direction == '' and self.start_title_loop:
            self.pause_title_loop = True
            self.main_menu.timer += 1
            if self.main_menu.timer == 30:
                self.main_menu.timer = 0
                self.pause_title_loop = False
                self.snake_p1.direction = self.snake_p1.last_direction
        self.check_food_collisions(self.snake_p1, self.food.position)
        if self.snake_p1.eating and len(self.snake_p1.body_segment_list) <= 16:
            self.snake_p1.grow_body()
            self.snake_p1.eating = False
            self.food.position = self.place_food_along_track(
                self.snake_p1,
                self.main_menu.snake_track,
                6
                )
            self.food.shape_list = self.food.create_food()
        elif self.snake_p1.eating and \
                len(self.snake_p1.body_segment_list) > 16:
            self.snake_p1.eating = False
            self.food.position = self.place_food_along_track(
                self.snake_p1,
                self.main_menu.snake_track,
                6
                )
            self.food.shape_list = self.food.create_food()
        self.snake_p1.loop(
            self.main_menu.snake_track[0],
            self.main_menu.snake_track[1],
            self.main_menu.snake_track[2],
            self.main_menu.snake_track[3],
        )
        self.snake_p1.move(delta_time)

    def normal_mode(self, delta_time):
        self.check_food_collisions(self.snake_p1, self.food.position)
        self.check_wall_collisions(self.snake_p1)
        self.snake_p1.check_body_collisions()
        if self.snake_p1.eating:
            self.snake_p1.grow_body()
            self.food.food_eaten += 1
            self.snake_p1.eating = False
            self.spawn_food_randomly(self.snake_p1, self.food)
            self.score.add_food_points()
            self.score.get_padded_str()
        if self.snake_p1.dead:
            self.snake_p1.flash_body(30, self.theme)
            self.game_state = type.GAME_STATES['game_over']
        self.snake_p1.move(delta_time)

    def get_random_board_coords(self, pad_left=0, pad_right=0,
                                pad_bottom=0, pad_top=0):
        x = random.randint((constants.BOARD_LEFT + pad_left),
                           (constants.BOARD_RIGHT - pad_right))
        y = random.randint((constants.BOARD_DOWN + pad_bottom),
                           (constants.BOARD_UP - pad_top))
        return x, y

    def spawn_food_randomly(self, snake, food):
        new_pos_xy = [self.get_random_board_coords()[0],
                      self.get_random_board_coords()[1]]
        food.position = new_pos_xy
        while food.position in snake.body_segment_list:
            self.spawn_food_randomly(snake, food)
        food.shape_list = food.create_food()
        food.food_spawned += 1
        return new_pos_xy

    def place_food_along_track(self, p1_snake, track, distance):
        global new_pos_x
        global new_pos_y
        top_l = (track[0])
        top_r = (track[1])
        bot_r = (track[2])
        bot_l = (track[3])
        if p1_snake.direction == 'LEFT':
            new_pos_x = p1_snake.head_pos[0] - distance
            new_pos_y = p1_snake.head_pos[1]
            if new_pos_x < bot_l[0]:
                overshoot = abs(new_pos_x - bot_l[0])
                new_pos_y = bot_l[1] + overshoot
                new_pos_x = bot_l[0] - 1
        elif p1_snake.direction == 'RIGHT':
            new_pos_x = p1_snake.head_pos[0] + distance
            new_pos_y = p1_snake.head_pos[1]
            if new_pos_x > top_r[0]:
                overshoot = abs(new_pos_x - top_r[0])
                new_pos_y = top_r[1] - overshoot
                new_pos_x = top_r[0] + 1
        elif p1_snake.direction == 'UP':
            new_pos_y = p1_snake.head_pos[1] + distance
            new_pos_x = p1_snake.head_pos[0]
            if new_pos_y > top_l[1]:
                overshoot = abs(new_pos_y - top_l[1])
                new_pos_x = top_l[0] + overshoot
                new_pos_y = top_l[1] + 1
        elif p1_snake.direction == 'DOWN':
            new_pos_y = p1_snake.head_pos[1] - distance
            new_pos_x = p1_snake.head_pos[0]
            if new_pos_y < bot_r[1]:
                overshoot = abs(new_pos_y - bot_r[1])
                new_pos_x = bot_r[0] - overshoot
                new_pos_y = bot_r[1] - 1
        new_food_pos = [new_pos_x, new_pos_y]
        return new_food_pos

    def check_food_collisions(self, snake, food):
        if snake.head_pos[0] == food[0] and snake.head_pos[1] == food[1]:
            snake.eating = True

    def check_wall_collisions(self, snake):
        if snake.head_pos[0] < constants.BOARD_LEFT:
            snake.dead = True
        elif snake.head_pos[0] > constants.BOARD_RIGHT:
            snake.dead = True
        elif snake.head_pos[1] > constants.BOARD_UP:
            snake.dead = True
        elif snake.head_pos[1] < constants.BOARD_DOWN:
            snake.dead = True

    def draw_game(self):
        arcade.set_background_color(self.theme['bg'])
        self.level.draw(self.score.get_padded_str())
        self.snake_p1.shape_list.draw()
        self.food.shape_list.draw()

    def draw_main_menu(self):
        arcade.set_background_color(self.theme['bg'])
        self.main_menu.draw()
        self.snake_p1.shape_list.draw()
        self.food.shape_list.draw()

    def draw_game_over_screen(self):
        self.draw_game()
        self.game_over_screen.draw()

    def on_draw(self):
        arcade.start_render()

        if self.game_state == 'main_menu':
            self.draw_main_menu()
        elif self.game_state == 'running':
            self.draw_game()
        elif self.game_state == 'paused':
            self.draw_game()
        elif self.game_state == 'game_over':
            self.draw_game_over_screen()

    def update(self, delta_time):
        if self.game_state == 'main_menu':
            self.menu_mode(delta_time)
        elif self.game_state == 'running':
            if self.mode == 'normal':
                self.normal_mode(delta_time)
        elif self.game_state == 'paused':
            if self.mode == 'normal':
                self.normal_mode(delta_time)
        elif self.game_state == 'game_over':
            if self.mode == 'normal':
                self.normal_mode(delta_time)

    def handle_main_menu_input(self, key):
        if key == arcade.key.ENTER:
            self.setup_game()
            self.game_state = type.GAME_STATES['running']

    def handle_gameplay_input(self, key):
        if key == arcade.key.UP or key == arcade.key.W:
            self.snake_p1.change_direction = 'UP'
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.snake_p1.change_direction = 'DOWN'
        elif key == arcade.key.LEFT or key == arcade.key.D:
            self.snake_p1.change_direction = 'LEFT'
        elif key == arcade.key.RIGHT or key == arcade.key.A:
            self.snake_p1.change_direction = 'RIGHT'


    def handle_game_over_input(self, key):
        if key == arcade.key.Y:
            self.setup_game()
            self.game_state = type.GAME_STATES['running']
        elif key == arcade.key.N:
            self.setup_screens()
            self.game_state = type.GAME_STATES['main_menu']

    def on_key_press(self, key, key_modifiers):
        if self.game_state == 'main_menu':
            self.handle_main_menu_input(key)
        elif self.game_state == 'running':
            self.handle_gameplay_input(key)
        elif self.game_state == 'paused':
            self.handle_pause_input(key)
        elif self.game_state == 'game_over':
            self.handle_game_over_input(key)


class Score():

    def __init__(self, food_points, milestone_amount, score=0):
        self.score = score
        self.food_points = food_points
        self.milestone_amount = milestone_amount
        self.milestone_checkpoint = 0

    def add_food_points(self):
        self.score += self.food_points

    def check_milestone(self):

        if self.milestone_amount is not None:
            if self.score - self.milestone_amount == self.milestone_checkpoint:
                self.milestone_checkpoint += self.milestone_amount
                return True
            else:
                return False

    def get_padded_str(self):
        padded_score_str = str(self.score).zfill(6)
        return padded_score_str


def main():
    game = Game(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    game.setup_screens()
    arcade.run()


if __name__ == "__main__":
    main()
