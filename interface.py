
import pygame

# feito com CoPilot
def desenhar_barra_vida(tela, x, y, vida):
    largura = 250 * vida / 100
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura, 12))

    pygame.draw.rect(tela, (255, 0, 0), (x, y, 250, 12))
    pygame.draw.rect(tela, (0, 255, 0), (x, y, largura, 12))