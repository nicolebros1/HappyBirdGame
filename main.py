import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 600, 400
FPS = 30
WHITE = (255, 255, 255)
GROUND_HEIGHT = 50

# Inicialização da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Bird")

# Relógio para controlar a taxa de quadros por segundo
clock = pygame.time.Clock()

# Carregamento de imagens
bird_image = pygame.image.load("bird.png")
background_image = pygame.image.load("background.png")
pipe_image = pygame.image.load("pipe.png")
ground_image = pygame.image.load("ground.png")


#Redimensionamento das imagens
BIRD_IMAGE_SIZE = (50, 50)
bird_image = pygame.transform.scale(bird_image, BIRD_IMAGE_SIZE)
PIPE_IMAGE_SIZE = (100,350)
pipe_image = pygame.transform.scale(pipe_image,PIPE_IMAGE_SIZE)


# Classe do pássaro
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

# Classe dos canos
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.height = random.randint(100, 200)
        self.rect.x = x
        self.rect.y = 0
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Grupo de sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Adiciona o pássaro ao grupo de sprites
bird = Bird()
all_sprites.add(bird)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    # Adiciona novos canos a cada 1000 milissegundos
    if pygame.time.get_ticks() % 50  == 0:
        pipe = Pipe(WIDTH)
        pipes.add(pipe)
        all_sprites.add(pipe)

    # Atualiza todos os sprites
    all_sprites.update()

    # Verifica colisões
    hits = pygame.sprite.spritecollide(bird, pipes, False)
    if hits:
        running = False


    # Desenha a tela
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Desenha o solo
    screen.blit(ground_image, (0, HEIGHT - GROUND_HEIGHT))

    # Atualiza a tela
    pygame.display.flip()

    # Limita a taxa de quadros por segundo
    clock.tick(FPS)

# Encerra o Pygame
pygame.quit()
sys.exit()

