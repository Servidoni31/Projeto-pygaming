
import pygame

# feito com CoPilot
import pygame

# feito com CoPilot
def desenhar_barra_vida(tela, x, y, vida, espelhada=False):
    pontos = [
        (x,       y + 16),
        (x + 35,  y + 14),
        (x + 55,  y + 10),
        (x + 70,  y + 5),
        (x + 80,  y),
        (x + 250, y),
        (x + 250, y + 24),
        (x + 80,  y + 24),
        (x + 45,  y + 23),
        (x,       y + 22),
    ]

    if espelhada:
        pontos_espelhados = []

        for ponto_x, ponto_y in pontos:
            novo_x = x + 250 - (ponto_x - x)
            pontos_espelhados.append((novo_x, ponto_y))

        pontos = pontos_espelhados

    pygame.draw.polygon(tela, (40, 220, 210), pontos)