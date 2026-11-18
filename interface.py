
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

    pygame.draw.polygon(tela, (30, 25, 45), pontos)

    largura = round(250 * max(0, min(vida, 100)) / 100)

    if espelhada:
        inicio_x = x + 250 - largura
    else:
        inicio_x = x

    recorte_anterior = tela.get_clip()
    tela.set_clip((inicio_x, y, largura, 25))

    pygame.draw.polygon(tela, (40, 220, 210), pontos)

    tela.set_clip(recorte_anterior)

    # borda por cima de tudo, desenhada depois do preenchimento:
    # contorno escuro grosso que separa a barra do cenario,
    # e um filete dourado por cima, que continua visivel com a barra vazia
    pygame.draw.polygon(tela, (12, 10, 24), pontos, 4)
    pygame.draw.polygon(tela, (255, 207, 92), pontos, 1)

# feito com CoPilot
def desenhar_cronometro(tela, fonte, tempo_restante):
    numero = str(tempo_restante)
    # antialias False: fonte pixelada fica nitida, sem borrar
    imagem_texto = fonte.render(numero, False, (255, 255, 255))
    posicao = imagem_texto.get_rect(center=(344, 27))
    tela.blit(imagem_texto, posicao)

# feito com CoPilot
def iniciar_musica():
    pygame.mixer.music.load("assets/som/trilha.ogg")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)


def carregar_som_soco():
    som = pygame.mixer.Sound("assets/som/efeitos/golpe_medio2.ogg")
    som.set_volume(1.0)
    return som