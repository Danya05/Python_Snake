import arcade

import constants


class Snake():

    def __init__(self, theme, size=constants.CELL, speed=8, head_pos=[0, 0],
                 direction='UP', change_direction=''):
        self.size = size
        self.head_colour = theme['head']
        self.body_colour_1 = theme['snake_body_1']
        self.body_colour_2 = theme['snake_body_2']
        self.body_colour_3 = theme['snake_body_3']
        self.border_colour = theme['snake_border']
        self.eye_colour = theme['eye']
        self.pupil_colour = theme['pupil']
        self.direction = direction
        self.change_direction = change_direction
        self.last_direction = ''
        self.head_pos = head_pos
        self.previous_pos = [self.head_pos[0], self.head_pos[1]]
        self.body_segment_list = self.align()
        self.offset = constants.CELL / 2
        self.speed = speed
        self.min_speed = 6
        self.max_speed = 16
        self.eating = False
        self.dead = False
        self.time_dead = 0
        self.shape_list = self.create_snake()

    def set_direction(self):
        if self.change_direction == 'UP' and \
           self.direction != 'DOWN':
            self.direction = 'UP'
        elif self.change_direction == 'DOWN' \
                and self.direction != 'UP':
            self.direction = 'DOWN'
        elif self.change_direction == 'LEFT' \
                and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif self.change_direction == 'RIGHT' \
                and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def align(self):
        if self.direction == 'LEFT' or self.direction == '':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0] + 1, self.head_pos[1]],
                             [self.head_pos[0] + 2, self.head_pos[1]]]
        elif self.direction == 'RIGHT':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0] - 1, self.head_pos[1]],
                             [self.head_pos[0] - 2, self.head_pos[1]]]
        elif self.direction == 'UP':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0], self.head_pos[1] - 1],
                             [self.head_pos[0], self.head_pos[1] - 2]]
        elif self.direction == 'DOWN':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0], self.head_pos[1] + 1],
                             [self.head_pos[0], self.head_pos[1] + 2]]
        return aligned_snake

    def move(self, dt):
        if not self.dead:
            if self.direction == 'UP':
                self.head_pos[1] += (self.speed * dt)
                if self.get_distance_travelled()[1] >= 1:
                    self.head_pos[1] = int(self.head_pos[1])
                    self.previous_pos[1] += 1
                    self.update_body()
                    self.set_direction()
            elif self.direction == 'DOWN':
                self.head_pos[1] -= (self.speed * dt)
                if self.get_distance_travelled()[1] >= 1:
                    self.head_pos[1] = int(self.head_pos[1] + 1)
                    self.previous_pos[1] -= 1
                    self.update_body()
                    self.set_direction()
            elif self.direction == 'LEFT':
                self.head_pos[0] -= (self.speed * dt)
                if self.get_distance_travelled()[0] >= 1:
                    self.head_pos[0] = int(self.head_pos[0] + 1)
                    self.previous_pos[0] -= 1
                    self.update_body()
                    self.set_direction()
            elif self.direction == 'RIGHT':
                self.head_pos[0] += (self.speed * dt)
                if self.get_distance_travelled()[0] >= 1:
                    self.head_pos[0] = int(self.head_pos[0])
                    self.previous_pos[0] += 1
                    self.update_body()
                    self.set_direction()

    def get_distance_travelled(self):
        x_dist = abs(self.previous_pos[0] - self.head_pos[0])
        y_dist = abs(self.previous_pos[1] - self.head_pos[1])
        return x_dist, y_dist

    def loop(self, top_l, top_r, bot_r, bot_l):
        if self.head_pos[0] == bot_l[0] and self.head_pos[1] == bot_l[1]:
            self.change_direction = 'UP'
        elif self.head_pos[0] == top_l[0] and self.head_pos[1] == top_l[1]:
            self.change_direction = 'RIGHT'
        elif self.head_pos[0] == top_r[0] and self.head_pos[1] == top_r[1]:
            self.change_direction = 'DOWN'
        elif self.head_pos[0] == bot_r[0] and self.head_pos[1] == bot_r[1]:
            self.change_direction = 'LEFT'

    def check_body_collisions(self):
        if self.head_pos in self.body_segment_list[1:-1]:
            self.dead = True

    def grow_body(self):
        self.body_segment_list.insert(0, list(self.head_pos))

    def update_body(self):
        if self.eating:
            self.grow_body()
        else:
            self.body_segment_list.insert(0, list(self.head_pos))
            self.body_segment_list.pop()
            self.shape_list = self.create_snake()

    def flash_body(self, interval, theme):
        self.time_dead += 1
        if self.time_dead > 5 and self.time_dead <= interval:
            self.head_colour = theme['bg']
            self.body_colour_1 = theme['bg']
            self.body_colour_2 = theme['bg']
            self.body_colour_3 = theme['bg']
            self.border_colour = theme['bg']
            self.eye_colour = theme['bg']
            self.pupil_colour = theme['bg']
            self.shape_list = self.create_snake()
        elif self.time_dead > interval:
            self.time_dead = 0
            self.head_colour = theme['head']
            self.body_colour_1 = theme['snake_body_1']
            self.body_colour_2 = theme['snake_body_2']
            self.body_colour_3 = theme['snake_body_3']
            self.border_colour = theme['snake_border']
            self.eye_colour = theme['eye']
            self.pupil_colour = theme['pupil']
            self.shape_list = self.create_snake()

    def get_grid_coords(self):
        grid_coords = []
        for position in self.body_segment_list:
            x = (position[0] * self.size) - self.offset
            y = (position[1] * self.size) - self.offset
            offset_coords = (x, y)
            grid_coords.append(offset_coords)
        return grid_coords

    def get_segment_points(self, position, width=constants.CELL,
                           height=constants.CELL):
        segment_points = arcade.get_rectangle_points(
            position[0],
            position[1],
            width,
            height,
            )
        return segment_points

    def create_segment_border(self, position, colour, width=constants.CELL,
                              height=constants.CELL):
        segment_border = arcade.create_rectangle_outline(
            position[0],
            position[1],
            width,
            height,
            colour,
            2
            )
        return segment_border

    def create_body_segment_fills(self, body_segments):
        "Красивый расскрас змейки"
        body_segment_point_list = []
        body_segment_colour_list = []
        for segment_xy in body_segments[:1]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.head_colour)
        for segment_xy in body_segments[1::3]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.body_colour_1)
        for segment_xy in body_segments[2::3]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.body_colour_2)
        for segment_xy in body_segments[3::3]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.body_colour_3)
        body_segment_fills = arcade.create_rectangles_filled_with_colors(
            body_segment_point_list,
            body_segment_colour_list
            )
        return body_segment_fills

    def create_body_segment_borders(self, body_segments):
        body_segments_border_list = []
        for segment in body_segments:
            body_segments_border_list.append(
                self.create_segment_border(segment, self.border_colour))
        return body_segments_border_list

    def get_eye_points(self):
        eye_point_list = []
        if self.direction == 'UP' or self.direction == '':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 12,
                width=self.size / 4,
                height=self.size / 3,
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 12,
                width=self.size / 4,
                height=self.size / 3
                 )
        elif self.direction == 'DOWN':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 12,
                width=self.size / 4,
                height=self.size / 3
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 12,
                width=self.size / 4,
                height=self.size / 3
                 )
        elif self.direction == 'LEFT':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
        elif self.direction == 'RIGHT':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
        for point in left_eye_fill:
            eye_point_list.append(point)
        for point in right_eye_fill:
            eye_point_list.append(point)
        return eye_point_list

    def create_eye_borders(self, colour):
        eye_borders_list = []
        if self.direction == 'UP' or self.direction == '':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
        elif self.direction == 'DOWN':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
        elif self.direction == 'LEFT':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
        elif self.direction == 'RIGHT':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                + self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * constants.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * constants.CELL) - self.offset)
                - self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
        eye_borders_list.append(left_eye_border)
        eye_borders_list.append(right_eye_border)
        return eye_borders_list

    def create_eye_fills(self, eye_point_list, colour):
        eye_fill_point_list = []
        eye_fill_colour_list = []
        for point in eye_point_list:
            eye_fill_point_list.append(point)
            eye_fill_colour_list.append(colour)
        eye_fills = arcade.create_rectangles_filled_with_colors(
            eye_fill_point_list,
            eye_fill_colour_list
        )
        return eye_fills

    def create_snake(self):
        shape_list = arcade.ShapeElementList()
        body_fills = self.create_body_segment_fills(self.get_grid_coords())
        body_borders = self.create_body_segment_borders(self.get_grid_coords())
        eyes = self.create_eye_fills(self.get_eye_points(),
                                     self.pupil_colour)
        eye_borders = self.create_eye_borders(self.eye_colour)
        shape_list.append(body_fills)
        for border in body_borders:
            shape_list.append(border)
        shape_list.append(eyes)
        for border in eye_borders:
            shape_list.append(border)
        return shape_list
