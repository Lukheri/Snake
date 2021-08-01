import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        self.direction = Vector2(1, 0)
        self.eat = False

    def movement(self):
        if self.eat:
            bodycopy = self.body[:]
            bodycopy.insert(0, bodycopy[0] + self.direction)
            self.body = bodycopy
            self.eat = False
        else:
            bodycopy = self.body[:-1]   
            bodycopy.insert(0, bodycopy[0] + self.direction)
            self.body = bodycopy


    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(int(block.x*cell_size), int(block.y*cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (255, 0, 0), block_rect)

    def addblock(self):
        self.eat = True


class FOOD:
    def __init__(self):
        self.spawn()

    def draw_food(self):
        food_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), food_rect)

    def spawn(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()

    def update(self):
        self.snake.movement()
        self.collision()

    def draw_elements(self):
        self.snake.draw_snake()
        self.food.draw_food()
    
    def collision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.spawn()
            self.snake.addblock()


pygame.init()   
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()

main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and main.snake.direction != Vector2(0, 1):
                main.snake.direction = Vector2(0, -1)
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and main.snake.direction != Vector2(0, -1):
                main.snake.direction = Vector2(0, 1)
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and main.snake.direction != Vector2(1, 0):
                main.snake.direction = Vector2(-1, 0)
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and main.snake.direction != Vector2(-1, 0):
                main.snake.direction = Vector2(1, 0)
    
    screen.fill((175, 215, 70))
    main.draw_elements()
    pygame.display.update()
    clock.tick(60)
