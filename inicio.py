# CONFIGURAÇÕES
import pygame

LARGURA = 1280
ALTURA = 720
FPS = 60

NOME_JOGO = "Insper Fighter"

INTEGRANTES = [
    "Guilherme Treves",
    "Joao Pedro Damiani",
    "Joao Servidoni",
]

BRANCO = [245, 241, 229]
CINZA = [158, 164, 189]
ESCURO = [10, 13, 27]
LARANJA = [255, 112, 62]
AMARELO = [255, 207, 92]
AZUL = [66, 219, 236]

pygame.init()

janela = pygame.display.set_mode([LARGURA, ALTURA])
pygame.display.set_caption(NOME_JOGO)



