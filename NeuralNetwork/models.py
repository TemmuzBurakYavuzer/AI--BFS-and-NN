import random
import math
import numpy as np

class Apple:
    def __init__(self, showScreen, screenx, screeny, b_size, img, snake_list, apple_size = 10):
        self.showScreen = showScreen
        self.screenx = screenx
        self.screeny = screeny
        self.b_size = b_size
        self.apple = img
        self.apple_size = apple_size
        self.rand_appleX = random.randint(0, self.screenx/self.b_size - 1) * 10
        self.rand_appleY = random.randint(0, self.screeny/self.b_size - 1) * 10

        while [self.rand_appleX, self.rand_appleY] in snake_list:
            self.rand_appleX = random.randint(0, self.screenx/self.b_size - 1) * 10
            self.rand_appleY = random.randint(0, self.screeny/self.b_size - 1) * 10

    def update_apple_pos(self, snake_list):
        self.rand_appleX = random.randint(0, self.screenx/self.b_size - 1) * 10
        self.rand_appleY = random.randint(0, self.screeny/self.b_size - 1) * 10
        while [self.rand_appleX, self.rand_appleY] in snake_list:
            self.rand_appleX = random.randint(0, self.screenx/self.b_size - 1) * 10
            self.rand_appleY = random.randint(0, self.screeny/self.b_size - 1) * 10

    def apple_pos(self):  return self.rand_appleX, self.rand_appleY

    def display(self):        
        self.showScreen.blit(self.apple, [self.rand_appleX, self.rand_appleY, self.apple_size,self.apple_size])

class Snake:
    def __init__(self, showScreen, screenx, screeny, img, x, y, b_size =10):
        self.showScreen = showScreen
        self.screenx = screenx
        self.screeny = screeny
        self.head = img
        self.snake_length = 1
        self.snake_list = [[x, y]]
        self.b_size = b_size
        self.eaten = False
        self.direction = "right"

    def is_alive(self):
        if self.snake_list[-1][0] >= self.screenx or self.snake_list[-1][0] < 0 or self.snake_list[-1][1] >= self.screeny\
                or self.snake_list[-1][1] < 0:
            return False
        elif self.snake_list[-1] in self.snake_list[:-1]: return False
        else: return True

    def eat_apple(self, rand_appleX, rand_appleY):
        if self.snake_list[-1][0] == rand_appleX and self.snake_list[-1][1] == rand_appleY: return True
        else:  return False

    def display_score(self):
        from app import black, pygame
        score = self.snake_length - 1
        text = pygame.font.SysFont("Comic Sans MS", 15).render("Length: " + str(score), True, black)
        self.showScreen.blit(text, [0, 0])

    def get_snake_head(self):
        return self.snake_list[-1][0], self.snake_list[-1][1]

    def update_snake_list(self, rand_appleX, rand_appleY):
        if self.direction == "left":
            lead_x_change = -self.b_size
            lead_y_change = 0
        elif self.direction == "right":
            lead_x_change = self.b_size
            lead_y_change = 0
        elif self.direction == "up":
            lead_y_change = -self.b_size
            lead_x_change = 0
        elif self.direction == "down":
            lead_y_change = self.b_size
            lead_x_change = 0

        snake_head = []
        snake_head.append(self.snake_list[-1][0] + lead_x_change)
        snake_head.append(self.snake_list[-1][1] + lead_y_change)
        self.snake_list.append(snake_head)

        if self.eat_apple(rand_appleX, rand_appleY):
            self.snake_length += 1
            self.eaten = True

        if len(self.snake_list) > self.snake_length:  del self.snake_list[0]

    def display(self):
        from app import pygame, yellow
        self.showScreen.blit(self.head, (self.snake_list[-1][0], self.snake_list[-1][1]))

        for XnY in self.snake_list[:-1]:
            pygame.draw.rect(self.showScreen, yellow,
                            [XnY[0], XnY[1], self.b_size, self.b_size])

class NeuralNetwork_Snake(Snake):
    def state(self, target, action):
        head_x, head_y = self.get_snake_head()
        start = [head_x, head_y]
        if self.direction == "up":
            options = [[start[0] - self.b_size, start[1]], [start[0], start[1] - self.b_size], [start[0] + self.b_size, start[1]]]
        elif self.direction == "right":
            options = [[start[0], start[1] - self.b_size], [start[0] + self.b_size, start[1]], [start[0], start[1] + self.b_size]]
        elif self.direction == "down":
            options = [[start[0] + self.b_size, start[1]], [start[0], start[1] + self.b_size], [start[0] - self.b_size, start[1]]]
        elif self.direction == "left":
            options = [[start[0], start[1] + self.b_size], [start[0] - self.b_size, start[1]], [start[0], start[1] - self.b_size]]

        state = []
        for o in options:
            result = None
            if [o[0], o[1]] in self.snake_list or o[0] < 0 or o[0] >= self.screenx or o[1] <0 or o[1] >= self.screeny:
                result = 1
            else:  result = 0
            state.append(result)

        quadrant = [target[0] - start[0], target[1] - start[1]]

        if self.direction == "up": pointer = [0, -1]
        elif self.direction == "right":  pointer = [1, 0]
        elif self.direction == "down": pointer = [0, 1]
        elif self.direction == "left":  pointer = [-1, 0]
        
        x = np.array(pointer)
        y = np.array(quadrant)
        
        if quadrant==[0,0]:
            angle = 0
        else:
            angle = np.arccos(x.dot(y) / (np.sqrt(x.dot(x)) * np.sqrt(y.dot(y))))
            if np.cross(x, y) > 0:
                angle = 2 * math.pi - angle
        state.append(angle)
        look_up = {"up": 0, "right": 1, "left": -1}
        state.append(look_up[action])
        return state

    def distance(self, target):
        head_x, head_y = self.get_snake_head()
        start = [head_x, head_y]
        quadrant = [target[0] - start[0], target[1] - start[1]]
        return math.hypot(quadrant[0], quadrant[1])

    def set_direction(self, action):
        look_up = {"up": 0, "right": 1, "left": -1}
        value = look_up[action]
        if self.direction == "up":
            if value != 0:
                self.direction = ("left" if value == -1 else "right")
            else: self.direction = "up"
        elif self.direction == "right":
            if value != 0:
                self.direction = ("up" if value == -1 else "down")
            else: self.direction = "right"
        elif self.direction == "down":
            if value != 0:
                self.direction = ("right" if value == -1 else "left")
            else: self.direction = "down"
        elif self.direction == "left":
            if value != 0:
                self.direction = ("down" if value == -1 else "up")
            else: self.direction = "left"
