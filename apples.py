import arcade

import constants


class Food():
    food_spawned = 0
    food_eaten = 0

    def __init__(self, theme, size, snake, pos=[0, 0]):
        self.size = size
        self.fill_colour = theme['food']
        self.border_colour = theme['food_border']
        self.position = pos
        self.offset = constants.CELL / 2
        self.shape_list = self.create_food()

    def update_theme(self, theme):
        self.fill_colour = theme['food']
        self.border_colour = theme['food_border']
        self.shape_list = self.create_food()

    def get_grid_coords(self):
        x = (self.position[0] * self.size) - self.offset
        y = (self.position[1] * self.size) - self.offset
        grid_coords = (x, y)
        return grid_coords

    def get_food_points(self, position, width=constants.CELL,
                        height=constants.CELL):
        food_points = arcade.get_rectangle_points(
            position[0],
            position[1],
            width,
            height,
            )
        return food_points

    def create_food_border(self, position, colour, width=constants.CELL,
                           height=constants.CELL):
        food_border = arcade.create_rectangle_outline(
            position[0],
            position[1],
            width,
            height,
            colour,
            2
            )
        return food_border

    def create_food_fill(self):
        food_point_list = []
        food_colour_list = []
        food_points = self.get_food_points(self.get_grid_coords())
        for point in food_points:
            food_point_list.append(point)
            food_colour_list.append(self.fill_colour)
        food_fill = arcade.create_rectangles_filled_with_colors(
            food_point_list,
            food_colour_list
            )
        return food_fill

    def create_food(self):
        shape_list = arcade.ShapeElementList()
        food_fill = self.create_food_fill()
        food_border = self.create_food_border(self.get_grid_coords(),
                                              self.border_colour)
        shape_list.append(food_fill)
        shape_list.append(food_border)
        return shape_list
