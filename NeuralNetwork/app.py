
import pygame
import random
from models import Apple, NeuralNetwork_Snake
import numpy as np
import pickle
from keras.models import load_model

pygame.init()
screenx = 200
screeny = 200
white = (0, 0, 0)
black = (255, 255, 255)
yellow = (255, 165, 0)
showScreen = pygame.display.set_mode((screenx, screeny))
pygame.display.set_caption("SnakeAI")
time = pygame.time.Clock()
snakeImg = pygame.image.load('snakehead.png')
appleImg = pygame.image.load('apple.png')
pygame.display.flip()
b_size = 10
FPS = 2000
moves = ["up", "left", "right"]

def trainSnake(times = 40000):
    train_data = []
    for i in range(times):
        print(i)
        pygame.event.pump()
        failed = False
        lead_x = 70
        lead_y = 70
        snake = NeuralNetwork_Snake(showScreen, screenx, screeny, snakeImg, lead_x, lead_y)
        apple = Apple(showScreen, screenx, screeny, b_size, appleImg, snake.snake_list)
        apple_x, apple_y = apple.apple_pos()
        act = "up"
        state = snake.state([apple_x, apple_y], act)
        former_distance = snake.distance([apple_x, apple_y])
        while not failed:
            apple_x, apple_y = apple.apple_pos()
            snake.update_snake_list(apple_x, apple_y)
            distance = snake.distance([apple_x, apple_y])
            score = 0
            if snake.is_alive() is False:
                failed = True
                score = -1
            showScreen.fill(white)
            if snake.eaten is True:  apple.update_apple_pos(snake.snake_list)
            if snake.eaten is True or  distance < former_distance: score = 1
            train_data.append([np.array(state), score])
            act = random.choice(moves)
            apple_x, apple_y = apple.apple_pos()
            former_distance = snake.distance([apple_x, apple_y])
            state = snake.state([apple_x, apple_y], act)
            snake.set_direction(act)
            apple.display()
            snake.eaten = False
            snake.display()
            snake.display_score()
            pygame.display.update()
            time.tick(FPS)

    print(len(train_data))
    f = open("train_data.txt", "wb")
    pickle.dump(train_data, f)
    f.close()

def test(times = 10):
    model = load_model('my_model.h5')
    s = []
    for i in range(times):
        print(i)
        pygame.event.pump()
        failed = False
        lead_x = 70
        lead_y = 70
        snake = NeuralNetwork_Snake(showScreen, screenx, screeny, snakeImg, lead_x, lead_y)
        apple = Apple(showScreen, screenx, screeny, b_size, appleImg, snake.snake_list)
        while not failed:
            apple_x, apple_y = apple.apple_pos()
            snake.update_snake_list(apple_x, apple_y)
            if snake.is_alive() is False:
                failed = True
                s.append(snake.snake_length)
            showScreen.fill(white)
            if snake.eaten is True:
                apple.update_apple_pos(snake.snake_list)
            apple_x, apple_y = apple.apple_pos()
            allPredictions = {}
            for act in moves:
               state = snake.state([apple_x, apple_y], act)
               allPredictions[act] = model.predict(np.array(state).reshape(-1, 5))[0][0]
            act = max(allPredictions, key=allPredictions.get)
            snake.set_direction(act)

            apple.display()
            snake.eaten = False
            snake.display()
            snake.display_score()
            pygame.display.update()
            time.tick(FPS)
    print("Avg is: {}".format(sum(s)/len(s)))

if __name__ == "__main__":
     #trainSnake(20000)
     test()
