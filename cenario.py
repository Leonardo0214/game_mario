import pygame

def desenhar_cenario_especial(screen, WIDTH, HEIGHT):
    # Chão de blocos
    for i in range(0, WIDTH, 40):
        pygame.draw.rect(screen, (188, 108, 37), (i, HEIGHT - 40, 40, 40))
        pygame.draw.rect(screen, (222, 173, 110), (i+5, HEIGHT - 35, 30, 10))

    # Blocos suspensos (linha do meio)
    blocos = [
        pygame.Rect(WIDTH//2 - 60, HEIGHT - 160, 40, 40)
        pygame.Rect(WIDTH//2 - 20, HEIGHT - 160, 40, 40),
        pygame.Rect(WIDTH//2 + 20, HEIGHT - 160, 40, 40),
    ]
    for bloco in blocos:
        pygame.draw.rect(screen, (188, 108, 37), bloco)
        pygame.draw.rect(screen, (255, 221, 77), (bloco.x+10, bloco.y+10, 20, 20))

    # Moeda acima do bloco central
    pygame.draw.circle(screen, (255, 215, 0), (WIDTH//2 + 20, HEIGHT - 180), 10)

    # Inimigos: Goomba e Koopa
    goomba_rect = pygame.Rect(WIDTH//2 + 60, HEIGHT - 80, 32, 32)
    koopa_rect = pygame.Rect(WIDTH//2 + 110, HEIGHT - 80, 32, 32)
    pygame.draw.ellipse(screen, (139, 69, 19), goomba_rect)
    pygame.draw.rect(screen, (0, 0, 0), (goomba_rect.x+8, goomba_rect.y+24, 16, 8))
    pygame.draw.ellipse(screen, (0, 200, 0), koopa_rect)
    pygame.draw.rect(screen, (255, 255, 255), (koopa_rect.x+8, koopa_rect.y+24, 16, 8))

    # Nuvens
    pygame.draw.ellipse(screen, (255, 255, 255), (80, 60, 60, 30))
    pygame.draw.ellipse(screen, (255, 255, 255), (WIDTH-140, 40, 60, 30))

    # Arbusto
    pygame.draw.ellipse(screen, (0, 200, 0), (WIDTH//2 - 80, HEIGHT - 60, 60, 30))
    pygame.draw.ellipse(screen, (0, 200, 0), (WIDTH//2 - 50, HEIGHT - 70, 60, 40))

    return blocos, goomba_rect, koopa_rect