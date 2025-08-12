import pygame
import sys
from cenario import desenhar_cenario_especial

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

# Variável para tela inicial/menu
tela_menu = True
opcao_selecionada = 0  # 0 = Continue, 1 = Novo Jogo

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

# NOVO: Variável para controlar se está no cenário vazio
cenario_vazio = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Menu inicial: navegação e seleção
        if tela_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    opcao_selecionada = (opcao_selecionada - 1) % 2
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    opcao_selecionada = (opcao_selecionada + 1) % 2
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if opcao_selecionada == 0:
                        tela_menu = False  # Continue
                    elif opcao_selecionada == 1:
                        reset_game()
                        tela_menu = False  # Novo Jogo
        # Reinicia o jogo ao pressionar R após o game over ou vitória
        if event.type == pygame.KEYDOWN and (game_over or you_win):
            if event.key == pygame.K_r:
                reset_game()
                cenario_vazio = False  # Volta para o cenário normal

    # TELA MENU PRETA
    if tela_menu:
        screen.fill((0, 0, 0))
        font_titulo = pygame.font.SysFont(None, 80)
        titulo = font_titulo.render("MARIO BROS", True, (255, 255, 255))
        screen.blit(titulo, (WIDTH//2 - 200, HEIGHT//2 - 120))

        font_menu = pygame.font.SysFont(None, 50)
        cor_continue = (255, 255, 0) if opcao_selecionada == 0 else (180, 180, 180)
        cor_novo = (255, 255, 0) if opcao_selecionada == 1 else (180, 180, 180)
        txt_continue = font_menu.render("Continue", True, cor_continue)
        txt_novo = font_menu.render("Novo Jogo", True, cor_novo)
        screen.blit(txt_continue, (WIDTH//2 - 100, HEIGHT//2 - 10))
        screen.blit(txt_novo, (WIDTH//2 - 100, HEIGHT//2 + 50))

        font_hint = pygame.font.SysFont(None, 30)
        hint = font_hint.render("Use ↑/↓ ou W/S e ENTER para selecionar", True, (200, 200, 200))
        screen.blit(hint, (WIDTH//2 - 170, HEIGHT//2 + 120))

        pygame.display.flip()
        clock.tick(60)
        continue
    # FIM DA TELA MENU

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

        # Colisão com plataformas (apenas se não estiver no cenário vazio)
        on_ground = False
        if not cenario_vazio:
            for plat in platforms:
                if mario.colliderect(plat) and y_velocity >= 0:
                    mario.y = plat.y - mario.height
                    y_velocity = 0
                    on_ground = True
        else:
            # No cenário vazio, Mario para no chão da tela
            if mario.y + mario.height >= HEIGHT - 40:
                mario.y = HEIGHT - 40 - mario.height
                y_velocity = 0
                on_ground = True
            # Blocos suspensos do cenário especial
            blocos, goomba_rect, koopa_rect = desenhar_cenario_especial(screen, WIDTH, HEIGHT)
            for bloco in blocos:
                if mario.colliderect(bloco) and y_velocity >= 0:
                    mario.y = bloco.y - mario.height
                    y_velocity = 0
                    on_ground = True

        # Movimento dos inimigos (apenas se não estiver no cenário vazio)
        if not cenario_vazio:
            for enemy in enemies:
                enemy["rect"].x += enemy["dir"]
                if enemy["rect"].x < enemy["range"][0] or enemy["rect"].x > enemy["range"][1]:
                    enemy["dir"] *= -1

            # Colisão com inimigos (apenas se não estiver no cenário vazio)
            for enemy in enemies[:]:
                if mario.colliderect(enemy["rect"]):
                    if y_velocity > 0 and mario.bottom - enemy["rect"].top < 20:
                        enemies.remove(enemy)
                        y_velocity = -12
                    else:
                        game_over = True
        else:
            # Colisão com inimigos do cenário especial
            if mario.colliderect(goomba_rect) or mario.colliderect(koopa_rect):
                game_over = True

        # Limites da tela
        if mario.x < 0:
            mario.x = 0
        if mario.x > WIDTH - mario.width:
            mario.x = WIDTH - mario.width
            # Se encostar no canto direito, vai para o cenário vazio
            cenario_vazio = True
            # Opcional: leva Mario para o lado esquerdo do novo cenário
            mario.x = 0
            # Remove gravidade extra se estiver caindo
            y_velocity = 0

    # Desenho
    if cenario_vazio:
        blocos, goomba_rect, koopa_rect = desenhar_cenario_especial(screen, WIDTH, HEIGHT)

    else:
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

    # Removido bloco de vitória, pois não há objetivo

    pygame.display.flip()
    clock.tick(50)