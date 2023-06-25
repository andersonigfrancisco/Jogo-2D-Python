import pygame
import sys
import random
import button
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
coin_sound = pygame.mixer.Sound('assets/audio/coin.wav')

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
            # print('collision')
        else:
            SPEED = 10

        if pygame.sprite.groupcollide(playerGroup, coinsGroup, False, True):
            placar += 1

        if placar % 5 == 0 and placar != 0:
            GAME_SPEED += 0.02
            # print('GAMESPEED ALTERADA')

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
        player.image = pygame.image.load('assets/sprites/player/fly/Fly.png').convert_alpha()
        player.image = pygame.transform.scale(player.image, [100, 100])
        # print('fly')

def fall(player):
    key = pygame.key.get_pressed()
    if not pygame.sprite.groupcollide(playerGroup, groundGroup, False, False) and not key[pygame.K_SPACE]:
        player.image = player.image_fall
        player.image = pygame.transform.scale(player.image, [100, 100])
        # print('falling')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_run = [pygame.image.load('assets/sprites/player/run/Run__000.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__001.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__002.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__003.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__004.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__005.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__006.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__007.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__008.png').convert_alpha(),
                          pygame.image.load('assets/sprites/player/run/Run__009.png').convert_alpha(),
                          ]
        self.image_fall = pygame.image.load('assets/sprites/player/fall/Fall.png').convert_alpha()
        self.image = pygame.image.load('assets/sprites/player/run/Run__000.png').convert_alpha()
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
        self.image = pygame.image.load('assets/sprites/ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(GROUND_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = HEIGHT - GROUND_HEIGHT

    def update(self, *args):
        self.rect[0] -= GAME_SPEED

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/Box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [100, 100])
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.rect[0] = xpos
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[1] = HEIGHT - ysize

    def update(self, *args):
        self.rect[0] -= GAME_SPEED
        # print('obstacle')

class Coins(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [40, 40])
        self.rect = pygame.Rect(100, 100, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[0] = xpos
        self.rect[1] = HEIGHT - ysize

    def update(self, *args):
        self.rect[0] -= GAME_SPEED
        # print('coin')

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
BACKGROUND = pygame.image.load('assets/sprites/background_03.png')
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

# Imagens dos botões
start_img = pygame.image.load('assets/sprites/buttons/start_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/sprites/buttons/restart_btn.png').convert_alpha()
exit_img = pygame.image.load('assets/sprites/buttons/exit_btn.png').convert_alpha()
resume_img = pygame.image.load('assets/sprites/buttons/resume_btn.png').convert_alpha()

# Botões
x = WIDTH / 2 - 150
start_button = button.Button(x, 125, start_img, 1)
exit_button = button.Button(x + 20, 325, exit_img, 1)

# Loop da tela de início
tela_inicio_loop = True

def tela_inicio_loop():
    tela_inicio = True

    bg_image = pygame.image.load("assets/bg.jpg").convert_alpha()
    bg_image = pygame.transform.scale(bg_image,[WIDTH, HEIGHT])
    game_window.blit(bg_image, (0 ,0))

    while tela_inicio:
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
            elif exit_button.draw(game_window):
                pygame.quit()
                sys.exit()
            elif start_button.draw(game_window):
                tela_inicio = False

        pygame.display.update()

tela_inicio_loop()

game_paused = False
# Loop do jogo principal
restart_button = button.Button(x, 300, restart_img, 1)
exit_button = button.Button(x + 20, 450, exit_img, 1)
resume_button = button.Button(x, 160, resume_img, 1)

while gameloop:
    game_window.blit(BACKGROUND, (0, 0))
    font = pygame.font.SysFont('Arial',30)
    text = font.render('Placar', True, [255,255,255])
    game_window.blit(text, [1100, 20])

    paused_font = pygame.font.SysFont('Arial Black',60)
    paused_text = paused_font.render('Pause', True, "orange")
    contador = font.render(f'{placar}', True, [255,255,255])
    game_window.blit(contador, [1125, 50])
    clock.tick(30)

    if game_paused:
        GAME_SPEED = 0
        game_window.blit(paused_text, (x + 30, 50))
        
        if resume_button.draw(game_window):
            game_paused = False
        if restart_button.draw(game_window):
            pass
        if exit_button.draw(game_window):
            gameloop = False
    else:
        GAME_SPEED = 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = not game_paused

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
        # print('collision')
    else:
        SPEED = 10

    if pygame.sprite.groupcollide(playerGroup, coinsGroup, False, True):
        placar += 1
        coin_sound.play()

    if placar % 5 == 0 and placar != 0:
        GAME_SPEED += 0.02
        # print('GAMESPEED ALTERADA')

    if pygame.sprite.groupcollide(playerGroup, obstacleGroup, False, False):
        gameloop = False

    playerGroup.update()
    groundGroup.update()
    obstacleGroup.update()
    coinsGroup.update()

    obstacleGroup.draw(game_window)
    playerGroup.draw(game_window)
    groundGroup.draw(game_window)
    coinsGroup.draw(game_window)

    pygame.display.update()