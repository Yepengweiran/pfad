import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 方块大小
block_size = 20

# 设置时钟
clock = pygame.time.Clock()


def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])


def draw_food(food_x, food_y):
    pygame.draw.rect(screen, RED, [food_x, food_y, block_size, block_size])


def game_over():
    font = pygame.font.SysFont(None, 75)
    text = font.render('Game Over', True, BLACK)
    screen.blit(text, [screen_width / 4, screen_height / 3])
    pygame.display.update()
    pygame.time.wait(2000)


def main():
    game_close = False
    game_exit = False

    # 初始位置
    x = screen_width / 2
    y = screen_height / 2

    # 初始移动方向
    x_change = 0
    y_change = 0

    # 蛇身体列表
    snake_list = []
    snake_length = 1

    # 食物位置
    food_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0

    while not game_exit:
        while game_close:
            screen.fill(WHITE)
            game_over()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0

        if x >= screen_width or x < 0 or y >= screen_height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(WHITE)

        draw_food(food_x, food_y)

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, screen_width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, screen_height - block_size) / 20.0) * 20.0
            snake_length += 1

        clock.tick(15)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
