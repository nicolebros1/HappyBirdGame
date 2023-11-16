import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
FPS = 30
GROUND_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Bird")

clock = pygame.time.Clock()

bird_image = pygame.image.load("bird.png")
background_image = pygame.image.load("background.png")
pipe_image = pygame.image.load("pipe.png")
ground_image = pygame.image.load("ground.png")

BIRD_IMAGE_SIZE = (50, 50)
bird_image = pygame.transform.scale(bird_image, BIRD_IMAGE_SIZE)
PIPE_IMAGE_SIZE = (90, 350)
pipe_image = pygame.transform.scale(pipe_image, PIPE_IMAGE_SIZE)

try:
    mask_bird = pygame.mask.from_surface(bird_image)
    mask_pipe = pygame.mask.from_surface(pipe_image)
except pygame.error as e:
    print("Erro ao criar máscaras:", e)
    pygame.quit()
    sys.exit()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.y_speed = 2

    def update(self):
        self.y_speed += 1
        self.rect.y += self.y_speed

        if self.rect.bottom > HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.y_speed = 0

    def jump(self):
        self.y_speed = -15

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.height = random.randint(150, 200)
        self.rect.x = x
        self.rect.y = random.randint(0, HEIGHT - GROUND_HEIGHT - self.rect.height)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
            self.rect.y = random.randint(0, HEIGHT - GROUND_HEIGHT - self.rect.height)

all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

bird = Bird()
all_sprites.add(bird)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    if pygame.time.get_ticks() % 500 == 0:
        pipe = Pipe(WIDTH)
        pipes.add(pipe)
        all_sprites.add(pipe)

    all_sprites.update()

    for pipe in pipes:
        if pygame.sprite.collide_mask(bird, pipe):
            running = False


    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)


    screen.blit(ground_image, (0, HEIGHT - GROUND_HEIGHT))


    pygame.display.flip()


    clock.tick(FPS)


pygame.quit()
sys.exit()
