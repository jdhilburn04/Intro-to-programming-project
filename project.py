import pygame
import math
import random

pygame.init()

# Variable for frame rate
clock = pygame.time.Clock()
FPS = 60


# Variables for our screen width and hieght (Game window)
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

#define game variables
rows = 5
cols = 5
enemy_cooldown = 1000#bullet cooldown in milliseconds
last_enemy_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0 #0 is no game over, 1 means won, -1 means lost


#define game colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# load image
bg = pygame.image.load("spacebg.png").convert()
bg_width = bg.get_width()

#define function for creating text
def draw_text(text, font, text_col, x, y):
    img =font.render(text, True, text_col)
    screen.blit(img, (x, y))

# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        # set movement speed:
        speed = 8
        #set cooldown variable
        cooldown = 250 #milliseconds
        game_over = 0

        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.y -= speed
        if key[pygame.K_DOWN]:
            self.rect.y += speed
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        #update mask
        self.mask = pygame.mask.from_surface(self.image)


        
        #record current time (for bullet)
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.right, self.rect.centery)
            bullet_group.add(bullet)
            self.last_shot = time_now
        #draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom +10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom +10), int(self.rect.width * (self.health_remaining/ self.health_start)), 15))
        elif self.health_remaining <= 0:
            self.kill()
            game_over = -1
        return game_over
#create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    #delete bullets at the top of the scree
    def update(self):
        self.rect.x += 5
        if self.rect.right > SCREEN_WIDTH - 10:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_ship_group, True):
            self.kill()


#create EnemyShips class
class EnemyShips(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy_ship" + str(random.randint(1,6)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

#create Enemy Bullets class
class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    #delete bullets at the end of the screen
    def update(self):
        self.rect.x -= 2
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            #redue spaceship health
            spaceship.health_remaining -=1

#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_ship_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()


def create_enemy_ships():
    #generate enemyships
    for col in range(cols):
        for item in range(rows):
            enemy_ship = EnemyShips(1000 + item * 100, 80 + col * 105)
            enemy_ship_group.add(enemy_ship)

create_enemy_ships()


#create player
spaceship = Spaceship(int(SCREEN_WIDTH - 1350), SCREEN_HEIGHT / 2, 3)
spaceship_group.add(spaceship)

#define game variables
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
print(tiles)

# (Game loop)
run = True
while run:

    #Frame rate
    clock.tick(FPS)

    #draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    #scrol background
    scroll -= 5

    #reset scroll
    if abs(scroll) > bg_width:
            scroll = 0

    if countdown == 0:
        

        #create random enemy bullets
        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if time_now - last_enemy_shot > enemy_cooldown:
            attacking_enemy = random.choice(enemy_ship_group.sprites())
            enemy_bullet = EnemyBullets(attacking_enemy.rect.centerx, attacking_enemy.rect.bottom)
            enemy_bullet_group.add(enemy_bullet)
            last_enemy_shot = time_now


        #check if all the enemy ships have been killed
        if len(enemy_ship_group) == 0:
            game_over = 1
        if game_over == 0:
            game_over = spaceship.update()

            #update spaceship
            game_over = spaceship.update()

            #ubpdate sprite groups
            bullet_group.update()
            enemy_ship_group.update()
            enemy_bullet_group.update()
        else:
            if game_over == -1:
                    draw_text("GAME OVER", font40, white, int(SCREEN_WIDTH) / 2 - 100, int(SCREEN_HEIGHT) /2)
            if game_over == +1:
                    draw_text("YOU WIN!", font40, white, int(SCREEN_WIDTH) / 2 - 100, int(SCREEN_HEIGHT) /2)

    if countdown > 0:
        draw_text("GET READY!", font40, white, int(SCREEN_WIDTH) / 2 - 100, int(SCREEN_HEIGHT) /2)
        draw_text(str(countdown), font40, white, int(SCREEN_WIDTH) / 2, int(SCREEN_HEIGHT) /2 + 100)
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer



    #draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    enemy_ship_group.draw(screen)
    enemy_bullet_group.draw(screen)

# (Game event handler)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()