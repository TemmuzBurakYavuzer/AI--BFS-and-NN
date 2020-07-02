import random

class Apple:
    def __init__(self, showScreen, screenx, screeny, b_size, img, snake_list, apple_size = 10):
        self.showScreen = showScreen
        self.screenx = screenx
        self.screeny = screeny
        self.b_size = b_size
        self.apple = img
        self.apple_size = apple_size
        
        self.rand_apple_x = random.randint(0, self.screenx/self.b_size - 1) * 10
        self.rand_apple_y = random.randint(0, self.screeny/self.b_size - 1) * 10

        while [self.rand_apple_x, self.rand_apple_y] in snake_list:
            self.rand_apple_x = random.randint(0, self.screenx/self.b_size - 1) * 10
            self.rand_apple_y = random.randint(0, self.screeny/self.b_size - 1) * 10

    def update_apple_pos(self, snake_list):
        self.rand_apple_x = random.randint(0, self.screenx/self.b_size - 1) * 10
        self.rand_apple_y = random.randint(0, self.screeny/self.b_size - 1) * 10

        while [self.rand_apple_x, self.rand_apple_y] in snake_list:
            self.rand_apple_x = random.randint(0, self.screenx/self.b_size - 1) * 10
            self.rand_apple_y = random.randint(0, self.screeny/self.b_size - 1) * 10

    def get_apple_pos(self):  return self.rand_apple_x, self.rand_apple_y

    def display(self):        
        self.showScreen.blit(self.apple, [self.rand_apple_x, self.rand_apple_y, self.apple_size, self.apple_size])

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
                or self.snake_list[-1][1] < 0:  return False
        elif self.snake_list[-1] in self.snake_list[:-1]:  return False
        else:  return True

    def eat_apple(self, rand_apple_x, rand_apple_y):
        if self.snake_list[-1][0] == rand_apple_x and self.snake_list[-1][1] == rand_apple_y:  return True
        else:  return False

    def display_score(self):
        from app import black, pygame
        score = self.snake_length - 1
        text = pygame.font.SysFont("Comic Sans MS", 15).render("Length: " + str(score), True, black)
        self.showScreen.blit(text, [0, 0])

    def get_snake_head(self): return self.snake_list[-1][0], self.snake_list[-1][1]

    def update_snake_list(self, rand_apple_x, rand_apple_y):
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

        if self.eat_apple(rand_apple_x, rand_apple_y):
            self.snake_length += 1
            self.eaten = True

        if len(self.snake_list) > self.snake_length:  del self.snake_list[0]

    def display(self):
        from app import pygame, yellow
        self.showScreen.blit(self.head, (self.snake_list[-1][0], self.snake_list[-1][1]))

        for XnY in self.snake_list[:-1]:
            pygame.draw.rect(self.showScreen, yellow,
                            [XnY[0], XnY[1], self.b_size, self.b_size])
