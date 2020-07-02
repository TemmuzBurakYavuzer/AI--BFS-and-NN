import pygame
import random
from bfs import BreathFirstSearch
from models import Apple, Snake

pygame.init()
screenx = 300
screeny = 300
white = (0, 0, 0)
black = (255, 255, 255)
yellow = (255, 165, 0)
showScreen = pygame.display.set_mode((screenx, screeny))
pygame.display.set_caption("Snake Game")
time = pygame.time.Clock()
snakeImg = pygame.image.load('snakehead.png')
appleImg = pygame.image.load('apple.png')
pygame.display.flip()
b_size = 10
FPS = 30

def one_game():
    pygame.event.pump()
    game_over = False
    lead_x = 150
    lead_y = 150
    snake = Snake(showScreen, screenx, screeny, snakeImg, lead_x, lead_y)
    apple = Apple(showScreen, screenx, screeny, b_size, appleImg, snake.snake_list)

    while not game_over:
        x, y = apple.get_apple_pos()
        snake.update_snake_list(x, y)

        if snake.is_alive() is False: game_over = True
        showScreen.fill(white)
        if snake.eaten is True: apple.update_apple_pos(snake.snake_list)

        apple.display()
        snake.eaten = False
        snake.display()
        snake.display_score()
        pygame.display.update()

        a_x, a_y = apple.get_apple_pos()
        s_x, s_y = snake.get_snake_head()

        visited = snake.snake_list.copy()
        visited.remove([s_x, s_y])
        result = BreathFirstSearch(screenx, screeny, b_size, visited, [a_x, a_y], [s_x, s_y])

        next_cell = result[1]

        x_diff = next_cell[0] - s_x
        y_diff = next_cell[1] - s_y

        if x_diff > 0:  snake.direction = "right"
        elif x_diff < 0:  snake.direction = "left"
        elif y_diff > 0:  snake.direction = "down"
        elif y_diff < 0:  snake.direction = "up"

        time.tick(FPS)

if __name__ == "__main__":
    one_game()
