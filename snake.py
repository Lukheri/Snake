import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(6,14), Vector2(5,14), Vector2(4,14)]
        self.direction = Vector2(1, 0)
        self.eat = False

        self.head_up = pygame.image.load("Graphics/Snake_Body/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/Snake_Body/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/Snake_Body/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/Snake_Body/head_right.png").convert_alpha()

        self.body_bl = pygame.image.load("Graphics/Snake_Body/body_bl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/Snake_Body/body_br.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/Snake_Body/body_tl.png").convert_alpha()
        self.body_tr = pygame.image.load("Graphics/Snake_Body/body_tr.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/Snake_Body/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/Snake_Body/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/Snake_Body/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/Snake_Body/tail_right.png").convert_alpha()

        self.body_vertical = pygame.image.load("Graphics/Snake_Body/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("Graphics/Snake_Body/body_horizontal.png").convert_alpha()

        self.bump = pygame.mixer.Sound("Sounds/bump.wav")
        self.eat_sound = pygame.mixer.Sound("Sounds/crunch.wav")
        self.eat_sound.set_volume(0.3)

    # def idle(self):
    #     bodycopy = self.body[:-1]   
    #     bodycopy.insert(0, bodycopy[0] + self.direction)
    #     self.body = bodycopy

    #     if self.body[0] == Vector2(18, 14):
    #         self.direction = Vector2(0, 1)
    #     elif self.body[0] == Vector2(18, 18):
    #         self.direction = Vector2(-1, 0)
    #     elif self.body[0] == Vector2(2, 18):
    #         self.direction = Vector2(0, -1)
    #     elif self.body[0] == Vector2(2, 14):
    #         self.direction = Vector2(1, 0)
    #     pass

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
        self.update_head()
        self.update_tail()

        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x*cell_size), int(block.y*cell_size), cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            
            else:
                prev_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (prev_block.x == -1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (prev_block.x ==-1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (prev_block.x == 1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)
        
    def update_tail(self):
        tailr = self.body[len(self.body)-2] - self.body[len(self.body)-1]
        if tailr == Vector2(1, 0): self.tail = self.tail_left
        elif tailr == Vector2(-1, 0): self.tail = self.tail_right
        elif tailr == Vector2(0, 1): self.tail = self.tail_up
        elif tailr == Vector2(0, -1): self.tail = self.tail_down

    def update_head(self):
        headr = self.body[1] - self.body[0]
        if headr == Vector2(1, 0): self.head = self.head_left
        elif headr == Vector2(-1, 0): self.head = self.head_right
        elif headr == Vector2(0, 1): self.head = self.head_up
        elif headr == Vector2(0, -1): self.head = self.head_down

    def play_eat_sound(self):
        self.eat_sound.play()

    def addblock(self):
        self.eat = True

class FOOD:
    def __init__(self):
        self.spawn()

    def draw_food(self):
        food_rect = pygame.Rect((self.pos.x*cell_size)+3, (self.pos.y*cell_size)+3, cell_size, cell_size)
        screen.blit(self.image, food_rect)

    def spawn(self):
        apple = pygame.image.load("Graphics/Food/apple.png").convert_alpha()
        bananas = pygame.image.load("Graphics/Food/bananas.png").convert_alpha()
        grapes = pygame.image.load("Graphics/Food/grapes.png").convert_alpha()
        orange = pygame.image.load("Graphics/Food/orange.png").convert_alpha()

        self.image = random.choice([apple, bananas, grapes, orange])
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()
        self.game_active = False
        self.score = 0
        self.bgm = pygame.mixer.Sound("Sounds/bgm.wav")
        self.bgm.set_volume(0.4)
        self.gameover = pygame.mixer.Sound("Sounds/gameover.wav")
        self.gameover.set_volume(0.8)

    def update(self):
        self.snake.movement()
        self.collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.food.draw_food()
        self.show_score()

    def collision(self):
        if self.food.pos == self.snake.body[0]:
            self.score += 1
            self.food.spawn()
            self.snake.addblock()
            self.snake.play_eat_sound()
        
        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.spawn()
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_active = False
            self.snake.body = [Vector2(6,14), Vector2(5,14), Vector2(4,14)]
            self.snake.direction = Vector2(1, 0)
            self.snake.eat = False
            self.food.spawn()
            self.snake.bump.play()
            self.bgm.fadeout(600)
            self.gameover.play()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_active = False
                self.snake.body = [Vector2(6,14), Vector2(5,14), Vector2(4,14)]
                self.snake.direction = Vector2(1, 0)
                self.snake.eat = False
                self.food.spawn()
                self.snake.bump.play()
                self.bgm.fadeout(600)
                self.gameover.play()

    def draw_grass(self):
        dark_grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row%2 == 0:
                for col in range(cell_number):
                    if col%2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, dark_grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col%2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, dark_grass_color, grass_rect)                 

    def show_score(self):
        font = pygame.font.Font("Font/Snake Chan.ttf", 30)
        score = font.render("Score: " + str(self.score), True, (38, 59, 44))
        screen.blit(score, (0, 3))

class MENU:
    def __init__(self):
        self.title_font = pygame.font.Font("Font/Snake Chan.ttf", 175)
        self.title = self.title_font.render("SNAKE", True, (3, 145, 41))
        self.title_rect = self.title.get_rect(center = (400, 200))
        self.play_img = pygame.image.load("Graphics/multimedia.png").convert_alpha()
        self.play_rect = self.play_img.get_rect(center = (400, 400))
    
    def draw(self):
        screen.blit(self.title, self.title_rect)
        screen.blit(self.play_img, self.play_rect)

pygame.init()   
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()

main = MAIN()
menu = MENU()

pressing = False

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not main.game_active:
            # if event.type == SCREEN_UPDATE:
            #     main.snake.idle()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse1 = pygame.mouse.get_pressed()
                if menu.play_rect.collidepoint(event.pos) and mouse1 == (True, False, False):
                    main.game_active = True
                    main.score = 0
                    main.bgm.play(loops = -1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main.game_active = True
                    main.score = 0  
                    main.bgm.play(loops = -1)

        else:  
            if event.type == SCREEN_UPDATE:
                main.update()
                pressing = False  
            if event.type == pygame.KEYDOWN:
                if not pressing:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and main.snake.direction != Vector2(0, 1):
                        main.snake.direction = Vector2(0, -1)
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and main.snake.direction != Vector2(0, -1):
                        main.snake.direction = Vector2(0, 1)
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and main.snake.direction != Vector2(1, 0):
                        main.snake.direction = Vector2(-1, 0)
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and main.snake.direction != Vector2(-1, 0):
                        main.snake.direction = Vector2(1, 0)
                    pressing = True

        

    screen.fill((175, 215, 70))
    main.draw_grass()

    if not main.game_active:
        menu.draw()
        main.show_score()
        # main.snake.draw_snake()

    else:
        main.draw_elements()
        
    pygame.display.update()
    clock.tick(60)
