import pygame
import math

pygame.init()

# Variable for frame rate
clock = pygame.time.Clock()
FPS = 60

# Variables for our screen width and hieght (Game window)
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load image
bg = pygame.image.load("spacebg.png").convert()
bg_width = bg.get_width()

# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def update(self):
        # set movement speed:
        speed = 8

        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.y -= speed
        if key[pygame.K_DOWN]:
            self.rect.y += speed

#create sprite groups
spaceship_group = pygame.sprite.Group()

#create player
spaceship = Spaceship(int(SCREEN_WIDTH - 1350), SCREEN_HEIGHT / 2)
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

# (Game event handler)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update spaceship
    spaceship.update()

    #draw sprite groups
    spaceship_group.draw(screen)


    pygame.display.update()

pygame.quit()