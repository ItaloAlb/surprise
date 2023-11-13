import pygame
from random import randrange
import numpy as np


class Direction:
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


class Game:
    def __init__(self):
        self._CELL_SIZE = 10
        self._GRID_SIZE = (10, 10)
        self._WINDOW_WIDTH = 600
        self._WINDOW_HEIGHT = 400
        self._WINDOW_SIZE = (self._WINDOW_WIDTH, self._WINDOW_HEIGHT)

        self._BACKGROUND_COLOR = "white"
        self._SNAKE_COLOR = (0, 201, 87)  # emerald green
        self._SNAKE_SEC_COLOR = "black"
        self._FOOD_COLOR = "red"

        self._FOOD_POSITIONS = [
            [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 3], [2, 3], [3, 3], [4, 0], [4, 1], [4, 2],
            [4, 3], [4, 4], [4, 5], [4, 6],  # H
            [7, 2], [8, 2], [9, 3], [7, 4], [8, 4], [9, 4], [6, 5], [9, 5], [7, 6], [8, 6], [9, 6],  # a
            [11, 2], [11, 3], [11, 4], [11, 5], [11, 6], [11, 7], [11, 8], [12, 2], [13, 2], [14, 3], [14, 4], [14, 5],
            # p
            [16, 2], [16, 3], [16, 4], [16, 5], [16, 6], [16, 7], [16, 8], [17, 2], [18, 2], [19, 3], [19, 4], [19, 5],
            # p
            [21, 2], [21, 3], [21, 4], [21, 5], [22, 3], [23, 3], [22, 5], [23, 5], [24, 2], [24, 3], [24, 4], [24, 5],
            [24, 6], [24, 7],  # y
            [28, 0], [28, 1], [28, 2], [28, 3], [28, 4], [28, 5], [28, 6], [29, 0], [30, 0], [31, 0], [29, 3], [30, 3],
            [31, 3], [29, 6], [30, 6], [31, 6], [32, 1], [32, 2], [32, 4], [32, 5],  # B
            [34, 0], [34, 1], [34, 2], [34, 3], [34, 4], [34, 5], [34, 6], [35, 0], [36, 0], [35, 6], [36, 6], [37, 1],
            [37, 5], [38, 2], [38, 3], [38, 4],  # D
            [41, 2], [42, 2], [43, 3], [41, 4], [42, 4], [43, 4], [40, 5], [43, 5], [41, 6], [42, 6], [43, 6],  # a
            [45, 2], [45, 3], [45, 4], [45, 5], [46, 3], [47, 3], [46, 5], [47, 5], [48, 2], [48, 3], [48, 4], [48, 5],
            [48, 6], [48, 7]  # y
        ]

        self._SNAKE_SIZE = 3

        pygame.init()
        self.screen = pygame.display.set_mode(self._WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.game_count = 1
        self.score = 0
        self.reward = 0
        self.iteration = 0
        self.snake = []
        self.food = ()
        self.hole = []
        self.direction = Direction.LEFT

        self.reset()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        self._handle_input()

        self._update_snake()

        self._handle_collision()

        self._draw()

        self.clock.tick(60)

    def reset(self):
        self._update_window_name("Surprise!")

        self._FOOD_POSITIONS = [
            [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 3], [2, 3], [3, 3], [4, 0], [4, 1], [4, 2],
            [4, 3], [4, 4], [4, 5], [4, 6],  # H
            [7, 2], [8, 2], [9, 3], [7, 4], [8, 4], [9, 4], [6, 5], [9, 5], [7, 6], [8, 6], [9, 6],  # a
            [11, 2], [11, 3], [11, 4], [11, 5], [11, 6], [11, 7], [11, 8], [12, 2], [13, 2], [14, 3], [14, 4], [14, 5],
            # p
            [16, 2], [16, 3], [16, 4], [16, 5], [16, 6], [16, 7], [16, 8], [17, 2], [18, 2], [19, 3], [19, 4], [19, 5],
            # p
            [21, 2], [21, 3], [21, 4], [21, 5], [22, 5], [23, 5], [22, 7], [23, 7], [24, 2], [24, 3], [24, 4], [24, 5],
            [24, 6], [24, 7],  # y
            [28, 0], [28, 1], [28, 2], [28, 3], [28, 4], [28, 5], [28, 6], [29, 0], [30, 0], [31, 0], [29, 3], [30, 3],
            [31, 3], [29, 6], [30, 6], [31, 6], [32, 1], [32, 2], [32, 4], [32, 5],  # B
            [34, 0], [34, 1], [34, 2], [34, 3], [34, 4], [34, 5], [34, 6], [35, 0], [36, 0], [35, 6], [36, 6], [37, 1],
            [37, 5], [38, 2], [38, 3], [38, 4],  # D
            [41, 2], [42, 2], [43, 3], [41, 4], [42, 4], [43, 4], [40, 5], [43, 5], [41, 6], [42, 6], [43, 6],  # a
            [45, 2], [45, 3], [45, 4], [45, 5], [46, 5], [47, 5], [46, 7], [47, 7], [48, 2], [48, 3], [48, 4], [48, 5],
            [48, 6], [48, 7],  # y
        ]

        self.game_count += 1

        self.score = 0

        self.reward = 0

        self.iteration = 0

        self.hole = []

        self.snake = []
        for i in range(self._SNAKE_SIZE):
            self.snake.append((self._WINDOW_WIDTH / 2 - i * self._CELL_SIZE, self._WINDOW_HEIGHT / 2))

        self._generate_food()

        self.direction = Direction.LEFT

    def _update_direction(self, action):
        if np.array_equal(action, [1, 0, 0]):
            pass
        elif np.array_equal(action, [0, 1, 0]):
            self.direction = (self.direction + 1) % 4
        else:
            self.direction = (self.direction - 1) % 4

    def _update_window_name(self, name):
        pygame.display.set_caption(name)

    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        self._draw()

        self._update_direction(action)

        head = self.snake[-1]

        self._update_snake()

        new_head = self.snake[-1]

        is_closer_to_food = (head[0] - self.food[0]) ** 2 + (head[1] - self.food[1]) ** 2 >= (
                new_head[0] - self.food[0]) ** 2 + (new_head[1] - self.food[1]) ** 2

        has_deadly_collision, has_food_collision = self._handle_collision()

        self._update_reward(has_deadly_collision, has_food_collision, is_closer_to_food)

        done = has_deadly_collision or self.iteration > 100 * len(self.snake)

        self.iteration += 1

        return self.reward, self.get_state(), done, self.score

    def get_state(self):
        head = self.snake[-1]

        head_up = (head[0], head[1] - self._CELL_SIZE)

        head_left = (head[0] - self._CELL_SIZE, head[1])

        head_down = (head[0], head[1] + self._CELL_SIZE)

        head_right = (head[0] + self._CELL_SIZE, head[1])

        is_obstacle_up = (self._check_wall_collision(head_up) or
                          self._check_self_collision(head_up) or
                          self._check_hole_collision(head_up))
        is_obstacle_left = (self._check_wall_collision(head_left) or
                            self._check_self_collision(head_left) or
                            self._check_hole_collision(head_left))
        is_obstacle_down = (self._check_wall_collision(head_down) or
                            self._check_self_collision(head_down) or
                            self._check_hole_collision(head_down))
        is_obstacle_right = (self._check_wall_collision(head_right) or
                             self._check_self_collision(head_right) or
                             self._check_hole_collision(head_right))

        # is_obstacle_up = head[1] == 0
        # is_obstacle_left = head[0] == 0
        # is_obstacle_down = head[1] == self._WINDOW_HEIGHT - self._CELL_SIZE
        # is_obstacle_right = head[0] == self._WINDOW_WIDTH - self._WINDOW_WIDTH

        state = [
            head[1] > self.food[1],
            head[0] > self.food[0],
            head[1] < self.food[1],
            head[0] < self.food[0],
            is_obstacle_up,
            is_obstacle_left,
            is_obstacle_down,
            is_obstacle_right,
            self.direction == Direction.UP,
            self.direction == Direction.LEFT,
            self.direction == Direction.DOWN,
            self.direction == Direction.RIGHT
        ]
        return np.array(state, dtype=int)

    def _update_snake(self):
        self.snake.pop(0)
        self._update_snake_head()

    def _update_snake_head(self):
        head = self.snake[-1]
        if self.direction == Direction.UP:
            head = (head[0], head[1] - self._CELL_SIZE)
        elif self.direction == Direction.LEFT:
            head = (head[0] - self._CELL_SIZE, head[1])
        elif self.direction == Direction.DOWN:
            head = (head[0], head[1] + self._CELL_SIZE)
        elif self.direction == Direction.RIGHT:
            head = (head[0] + self._CELL_SIZE, head[1])
        self.snake.append(head)

    def _update_reward(self, has_deadly_collision, has_food_collision, is_closer_to_food):
        if has_deadly_collision:
            self.reward = -100
        elif has_food_collision:
            self.reward = +50
        elif is_closer_to_food:
            self.reward = +10
        else:
            self.reward = -20

    def _check_wall_collision(self, head):
        return head[0] >= self._WINDOW_WIDTH or head[1] >= self._WINDOW_HEIGHT or head[0] < 0 or head[1] < 0

    def _check_self_collision(self, head):
        return head in self.snake[:-1]

    def _check_hole_collision(self, head):
        return head in self.hole

    def _check_food_collision(self, head):
        return head[0] == self.food[0] and head[1] == self.food[1]

    def _generate_food(self):
        n = len(self._FOOD_POSITIONS)
        done = True
        while done:
            if n > 0:
                index = randrange(0, n)
                pos = self._FOOD_POSITIONS.pop(index)
                self.food = (pos[0] * self._CELL_SIZE + 60, pos[1] * self._CELL_SIZE + 160)
            else:
                self._update_window_name("Happy Birthday!")
                self.food = (randrange(0, self._WINDOW_WIDTH, 10), randrange(0, self._WINDOW_HEIGHT, 10))
            done = self.food in self.snake

    def _handle_collision(self, disable_wall_collision=False, disable_self_collision=False, disable_hole_collision=False):
        head = self.snake[-1]
        has_deadly_collision, has_food_collision = False, False
        if (self._check_wall_collision(head) * (not disable_wall_collision) or
                self._check_self_collision(head) * (not disable_self_collision) or
                self._check_hole_collision(head) * (not disable_hole_collision)):
            has_deadly_collision = True
        elif self._check_food_collision(head):
            has_food_collision = True
            self.score += 1
            self.hole.append(self.food)
            self._generate_food()
            self._update_snake_head()
        return has_deadly_collision, has_food_collision

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif keys[pygame.K_a] and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif keys[pygame.K_s] and self.direction != Direction.UP:
            self.direction = Direction.DOWN
        elif keys[pygame.K_d] and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT

    def _draw(self):
        self.screen.fill(self._BACKGROUND_COLOR)

        for i in range(len(self.snake)):
            pygame.draw.rect(self.screen,
                             self._SNAKE_SEC_COLOR,
                             (self.snake[i], self._GRID_SIZE),
                             5,
                             2)
            pygame.draw.rect(self.screen,
                             self._SNAKE_COLOR,
                             (self.snake[i], self._GRID_SIZE),
                             4,
                             2)

        for i in range(len(self.hole)):
            hole_color = (randrange(0, 256), randrange(0, 256), randrange(0, 256))

            pygame.draw.rect(self.screen,
                             hole_color,
                             (self.hole[i], self._GRID_SIZE),
                             5,
                             2)

        pygame.draw.rect(self.screen,
                         self._FOOD_COLOR,
                         (self.food, self._GRID_SIZE),
                         5,
                         2)

        pygame.display.flip()

    def quit(self):
        pygame.quit()
