import pygame
import sys
import random
# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
largura = 800
altura = 600

# Configuração da tela de início
tela_inicio = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Tela de Início")

# Fonte para o texto
fonte = pygame.font.Font(None, 40)

def desenhar_tela_inicio():
    tela_inicio.fill(BRANCO)
    
    # Texto "Iniciar Jogo"
    texto_iniciar = fonte.render("Iniciar Jogo", True, PRETO)
    pos_texto_iniciar = texto_iniciar.get_rect(center=(largura/2, altura/2 - 50))
    tela_inicio.blit(texto_iniciar, pos_texto_iniciar)
    
    # Texto "Sair"
    texto_sair = fonte.render("Sair", True, PRETO)
    pos_texto_sair = texto_sair.get_rect(center=(largura/2, altura/2 + 50))
    tela_inicio.blit(texto_sair, pos_texto_sair)
    
    pygame.display.flip()

def tela_jogo():
    global gameloop
    gameloop = True
    while gameloop:
        game_window.blit(BACKGROUND, (0, 0))
        font = pygame.font.SysFont('Arial',30)
        text = font.render('Placar', True, [255,255,255])
        game_window.blit(text, [1100, 20])
        contador = font.render(f'{placar}', True, [255,255,255])
        game_window.blit(contador, [1125, 50])
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                sys.exit()

        if is_off_screen(groundGroup.sprites()[0]):
            groundGroup.remove(groundGroup.sprites()[0])
            newGround = Ground(WIDTH - 40)
            groundGroup.add(newGround)

        if is_off_screen(obstacleGroup.sprites()[0]):
            obstacleGroup.remove(obstacleGroup.sprites()[0])
            newObstacle = get_random_obstacles(WIDTH * 1.5)
            obstacleGroup.add(newObstacle)
            newCoin = get_random_coins(WIDTH * 2)
            newCoin1 = get_random_coins(WIDTH * 2.2)
            newCoin2 = get_random_coins(WIDTH * 2.4)
            newCoin3 = get_random_coins(WIDTH * 2.6)
            newCoin4 = get_random_coins(WIDTH * 2.8)
            coinsGroup.add(newCoin)
            coinsGroup.add(newCoin1)
            coinsGroup.add(newCoin2)
            coinsGroup.add(newCoin3)
            coinsGroup.add(newCoin4)

        if pygame.sprite.groupcollide(playerGroup, groundGroup, False, False):
            SPEED = 0
            print('collision')
        else:
            SPEED = 10

        if pygame.sprite.groupcollide(playerGroup, coinsGroup, False, True):
            placar += 1

        if placar % 5 == 0 and placar != 0:
            GAME_SPEED += 0.02
            print('GAMESPEED ALTERADA')

        if pygame.sprite.groupcollide(playerGroup, obstacleGroup, False, False):
            gameloop = False

        
        pygame.display.update()

def move_player(player):
    key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        player.rect[0] += GAME_SPEED
    if key[pygame.K_a]:
        player.rect[0] -= GAME_SPEED
    player.current_image = (player.current_image + 1) % 10
    player.image = player.image_run[player.current_image]
    player.image = pygame.transform.scale(player.image,[100, 100])

def fly(player):
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        player.rect[1] -= 30
        player.image = pygame.image.load('sprites/Fly.png').convert_alpha()
        player.image = pygame.transform.scale(player.image, [100, 100])
        print('fly')

def fall(player):
    key = pygame.key.get_pressed()
    if not pygame.sprite.groupcollide(playerGroup, groundGroup, False, False) and not key[pygame.K_SPACE]:
        player.image = player.image_fall
        player.image = pygame.transform.scale(player.image, [100, 100])
        print('falling')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_run = [pygame.image.load('sprites/Run__000.png').convert_alpha(),
                          pygame.image.load('sprites/Run__001.png').convert_alpha(),
                          pygame.image.load('sprites/Run__002.png').convert_alpha(),
                          pygame.image.load('sprites/Run__003.png').convert_alpha(),
                          pygame.image.load('sprites/Run__004.png').convert_alpha(),
                          pygame.image.load('sprites/Run__005.png').convert_alpha(),
                          pygame.image.load('sprites/Run__006.png').convert_alpha(),
                          pygame.image.load('sprites/Run__007.png').convert_alpha(),
                          pygame.image.load('sprites/Run__008.png').convert_alpha(),
                          pygame.image.load('sprites/Run__009.png').convert_alpha(),
                          ]
        self.image_fall = pygame.image.load('sprites/Fall.png').convert_alpha()
        self.image = pygame.image.load('sprites/Run__000.png').convert_alpha()
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.mask = pygame.mask.from_surface(self.image)
        self.current_image = 0

    def update(self, *args):
        move_player(self)
        self.rect[1] += SPEED
        fly(self)
        fall(self)

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(GROUND_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = HEIGHT - GROUND_HEIGHT

    def update(self, *args):
        self.rect[0] -= GAME_SPEED

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/Box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [100, 100])
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.rect[0] = xpos
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[1] = HEIGHT - ysize

    def update(self, *args):
        self.rect[0] -= GAME_SPEED
        print('obstacle')

class Coins(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [40, 40])
        self.rect = pygame.Rect(100, 100, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[0] = xpos
        self.rect[1] = HEIGHT - ysize

    def update(self, *args):
        self.rect[0] -= GAME_SPEED
        print('coin')

def get_random_obstacles(xpos):
    size = random.randint(120, 600)
    box = Obstacles(xpos, size)
    return box

def get_random_coins(xpos):
    size = random.randint(60, 500)
    coin = Coins(xpos, size)
    return coin

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

# Variáveis do jogo
WIDTH = 1280
HEIGHT = 720
GROUND_WIDTH = 1280
GROUND_HEIGHT = 40
GAME_SPEED = 10
SPEED = 0




# Inicialização da janela de jogo
game_window = pygame.display.set_mode([WIDTH, HEIGHT])
game_window_rect = game_window.get_rect()
game_window_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2)
pygame.display.set_caption('Jogo 01')

# Carregamento das imagens
BACKGROUND = pygame.image.load('sprites/background_03.png')
BACKGROUND = pygame.transform.scale(BACKGROUND,[WIDTH, HEIGHT])

# Grupos de sprites
playerGroup = pygame.sprite.Group()
player = Player()
playerGroup.add(player)

groundGroup = pygame.sprite.Group()
for i in range(2):
    ground = Ground(WIDTH * i)
    groundGroup.add(ground)

coinsGroup = pygame.sprite.Group()
for i in range(2):
    coin = get_random_coins(WIDTH * i + 1000)
    coinsGroup.add(coin)

obstacleGroup = pygame.sprite.Group()
for i in range(2):
    obstacle = get_random_obstacles(WIDTH * i + 1000)
    obstacleGroup.add(obstacle)

# Loop do jogo
gameloop = True
placar = 0
clock = pygame.time.Clock()

# Loop da tela de início
tela_inicio_loop = True
def desenhar_tela_inicio():
    game_window.fill((0, 0, 0))  # Preenche a tela com a cor preta
    font = pygame.font.SysFont('Arial', 30)
    texto_iniciar = font.render('Pressione qualquer tecla para iniciar o jogo', True, (255, 255, 255))
    pos_texto_iniciar = (WIDTH // 2 - texto_iniciar.get_width() // 2, HEIGHT // 2 - texto_iniciar.get_height() // 2)
    game_window.blit(texto_iniciar, pos_texto_iniciar)
    texto_sair = font.render('Pressione ESC para sair', True, (255, 255, 255))
    pos_texto_sair = (WIDTH // 2 - texto_sair.get_width() // 2, HEIGHT // 2 + 50)
    game_window.blit(texto_sair, pos_texto_sair)
    return pos_texto_iniciar, pos_texto_sair  # Retorna as posições dos textos de início e sair

def tela_inicio_loop():
    tela_inicio = True

    while tela_inicio:
        pos_texto_iniciar, pos_texto_sair = desenhar_tela_inicio()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if tela_inicio:
                    tela_inicio = False  # Sai da tela de início quando qualquer tecla for pressionada
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pos_texto_iniciar.collidepoint(event.pos):
                    tela_inicio = False
                    break
                elif pos_texto_sair.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

tela_inicio_loop()

# Loop do jogo principal
while gameloop:
    game_window.blit(BACKGROUND, (0, 0))
    font = pygame.font.SysFont('Arial',30)
    text = font.render('Placar', True, [255,255,255])
    game_window.blit(text, [1100, 20])
    contador = font.render(f'{placar}', True, [255,255,255])
    game_window.blit(contador, [1125, 50])
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if is_off_screen(groundGroup.sprites()[0]):
        groundGroup.remove(groundGroup.sprites()[0])
        newGround = Ground(WIDTH - 40)
        groundGroup.add(newGround)

    if is_off_screen(obstacleGroup.sprites()[0]):
        obstacleGroup.remove(obstacleGroup.sprites()[0])
        newObstacle = get_random_obstacles(WIDTH * 1.5)
        obstacleGroup.add(newObstacle)
        newCoin = get_random_coins(WIDTH * 2)
        newCoin1 = get_random_coins(WIDTH * 2.2)
        newCoin2 = get_random_coins(WIDTH * 2.4)
        newCoin3 = get_random_coins(WIDTH * 2.6)
        newCoin4 = get_random_coins(WIDTH * 2.8)
        coinsGroup.add(newCoin)
        coinsGroup.add(newCoin1)
        coinsGroup.add(newCoin2)
        coinsGroup.add(newCoin3)
        coinsGroup.add(newCoin4)

    if pygame.sprite.groupcollide(playerGroup, groundGroup, False, False):
        SPEED = 0
        print('collision')
    else:
        SPEED = 10

    if pygame.sprite.groupcollide(playerGroup, coinsGroup, False, True):
        placar += 1

    if placar % 5 == 0 and placar != 0:
        GAME_SPEED += 0.02
        print('GAMESPEED ALTERADA')

    if pygame.sprite.groupcollide(playerGroup, obstacleGroup, False, False):
        gameloop = False

    playerGroup.update()
    groundGroup.update()
    obstacleGroup.update()
    coinsGroup.update()

    playerGroup.draw(game_window)
    groundGroup.draw(game_window)
    obstacleGroup.draw(game_window)
    coinsGroup.draw(game_window)

    pygame.display.update()