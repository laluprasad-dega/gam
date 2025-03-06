import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set up display and window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Heavy Advanced Snake Game')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)
PURPLE = (128, 0, 128)

# Snake and game configurations
SNAKE_SIZE = 10
SNAKE_SPEED = 15
BLOCK_SIZE = 10
FONT = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)

# Initialize game clock
clock = pygame.time.Clock()

# Function to display score
def display_score(score):
    value = SCORE_FONT.render(f"Score: {score}", True, YELLOW)
    screen.blit(value, [0, 0])

# Function to draw snake
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

# Function to display messages
def display_message(msg, color, y_offset=0):
    message = FONT.render(msg, True, color)
    screen.blit(message, [WIDTH / 6, HEIGHT / 3 + y_offset])

# Function to generate food
def generate_food():
    return round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0, round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

# Function to generate a power-up
def generate_power_up():
    return round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0, round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_body = []
    length_of_snake = 1

    food_x, food_y = generate_food()
    power_up_x, power_up_y = generate_power_up()

    speed_boost = False
    speed_timer = 0
    obstacle_list = []

    # Generate obstacles
    for i in range(5):
        obs_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
        obs_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
        obstacle_list.append([obs_x, obs_y])

    while not game_over:

        while game_close:
            screen.fill(BLUE)
            display_message("You Lost! Press C to Play Again or Q to Quit", RED)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Snake movement
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)

        # Draw obstacles
        for obs in obstacle_list:
            pygame.draw.rect(screen, PURPLE, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])

        # Draw food
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Draw power-up
        if not speed_boost:
            pygame.draw.circle(screen, YELLOW, (power_up_x, power_up_y), 8)

        # Check if snake eats food
        snake_head = [x1, y1]
        snake_body.append(snake_head)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        draw_snake(snake_body)
        display_score(length_of_snake - 1)

        # Check if snake hits itself
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_close = True

        # Check if snake eats food
        if x1 == food_x and y1 == food_y:
            food_x, food_y = generate_food()
            length_of_snake += 1

        # Check if snake hits power-up
        if x1 == power_up_x and y1 == power_up_y and not speed_boost:
            speed_boost = True
            speed_timer = time.time()

        # Remove power-up after some time
        if speed_boost and time.time() - speed_timer > 5:
            speed_boost = False
            power_up_x, power_up_y = generate_power_up()

        # Check if snake hits obstacle
        for obs in obstacle_list:
            if x1 == obs[0] and y1 == obs[1]:
                game_close = True

        pygame.display.update()

        # Control the snake's speed
        if speed_boost:
            clock.tick(SNAKE_SPEED + 5)  # Increase speed during power-up
        else:
            clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# Start the game
game_loop()
