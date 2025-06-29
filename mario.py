import pygame
import sys

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Bros")

# Cores
PINK = (255, 105, 180)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
BROWN = (150, 75, 0)
ENEMY_COLOR = (0, 0, 0)

# --- Sprites animados do Mario NES ---
# Salve os arquivos: mario_idle.png, mario_run1.png, mario_run2.png, mario_jump.png na mesma pasta deste script!
mario_idle = pygame.image.load("mario_idle.png").convert_alpha()
mario_run1 = pygame.image.load("mario_run1.png").convert_alpha()
mario_run2 = pygame.image.load("mario_run2.png").convert_alpha()
mario_jump = pygame.image.load("mario_jump.png").convert_alpha()
# Redimensiona todos para 40x40
mario_idle = pygame.transform.scale(mario_idle, (40, 40))
mario_run1 = pygame.transform.scale(mario_run1, (40, 40))
mario_run2 = pygame.transform.scale(mario_run2, (40, 40))
mario_jump = pygame.transform.scale(mario_jump, (40, 40))
# -------------------------------------

def reset_game():
    global mario, y_velocity, on_ground, enemies, game_over, you_win
    mario = pygame.Rect(100, 300, 40, 40)
    y_velocity = 0
    on_ground = False
    enemies = [
        {"rect": pygame.Rect(250, 210, 40, 40), "dir": 2, "range": (200, 320)},
        {"rect": pygame.Rect(420, 140, 40, 40), "dir": -2, "range": (400, 500)}
    ]
    game_over = False
    you_win = False

# Plataformas (chão + outras)
platforms = [
    pygame.Rect(0, 350, WIDTH, 50),           # chão
    pygame.Rect(200, 250, 120, 15),           # plataforma 1
    pygame.Rect(400, 180, 100, 15),           # plataforma 2
    pygame.Rect(600, 120, 80, 15)             # plataforma 3
]

clock = pygame.time.Clock()
reset_game()

font_obj = pygame.font.SysFont(None, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Reinicia o jogo ao pressionar R após o game over ou vitória
        if event.type == pygame.KEYDOWN and (game_over or you_win):
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over and not you_win:
        # Movimento lateral
        if keys[pygame.K_RIGHT]:
            mario.x += 5
        if keys[pygame.K_LEFT]:
            mario.x -= 5

        # Pulo
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
            y_velocity = -18
            on_ground = False

        # Gravidade
        y_velocity += 1
        mario.y += y_velocity

        # Colisão com plataformas
        on_ground = False
        for plat in platforms:
            if mario.colliderect(plat) and y_velocity >= 0:
                mario.y = plat.y - mario.height
                y_velocity = 0
                on_ground = True

        # Movimento dos inimigos
        for enemy in enemies:
            enemy["rect"].x += enemy["dir"]
            if enemy["rect"].x < enemy["range"][0] or enemy["rect"].x > enemy["range"][1]:
                enemy["dir"] *= -1

        # Colisão com inimigos (elimina se pular em cima, senão Game Over)
        for enemy in enemies[:]:
            if mario.colliderect(enemy["rect"]):
                if y_velocity > 0 and mario.bottom - enemy["rect"].top < 20:
                    enemies.remove(enemy)
                    y_velocity = -12
                else:
                    game_over = True

        # Vitória: todos os inimigos eliminados
        if not enemies:
            you_win = True

        # Limites da tela
        if mario.x < 0: mario.x = 0
        if mario.x > WIDTH - mario.width: mario.x = WIDTH - mario.width

    # Desenho
    screen.fill(BLUE)
    
    for plat in platforms:
        pygame.draw.rect(screen, BROWN if plat != platforms[0] else GREEN, plat)
    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, enemy["rect"])

    # --- Escolhe o sprite animado do Mario NES ---
    if not on_ground:
        mario_img = mario_jump
    elif keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
        # Alterna entre os frames de corrida
        if (pygame.time.get_ticks() // 150) % 2 == 0:
            mario_img = mario_run1
        else:
            mario_img = mario_run2
    else:
        mario_img = mario_idle
    screen.blit(mario_img, (mario.x, mario.y))
    # ---------------------------------------------

    if game_over:
        font = pygame.font.SysFont(None, 80)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (WIDTH//2 - 200, HEIGHT//2 - 40))
        font2 = pygame.font.SysFont(None, 40)
        text2 = font2.render("Pressione R para reiniciar", True, (0, 0, 0))
        screen.blit(text2, (WIDTH//2 - 170, HEIGHT//2 + 40))

    if you_win:
        font = pygame.font.SysFont(None, 80)
        text = font.render("YOU WIN!", True, (0, 180, 0))
        screen.blit(text, (WIDTH//2 - 170, HEIGHT//2 - 40))
        font2 = pygame.font.SysFont(None, 40)
        text2 = font2.render("Pressione R para reiniciar", True, (0, 0, 0))
        screen.blit(text2, (WIDTH//2 - 170, HEIGHT//2 + 40))

    pygame.display.flip()
    clock.tick(60)