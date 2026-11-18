import pygame

# As arenas do jogo. "chao" e a altura (em pixels da tela de 688x272) em que
# ficam os pes dos lutadores naquele cenario.
CENARIOS = [
    {"nome": "CENTRO",  "chao": 256},
    {"nome": "BECO",    "chao": 230},
    {"nome": "TELHADO", "chao": 194},
]


def montar_centro():
    """O cenario 1 vem em camadas: fundo e meio sao pedacos que se repetem
    na horizontal; a frente ja tem a largura da tela."""
    tela = pygame.Surface((688, 272))
    fundo = pygame.image.load("assets/cenario/back.png").convert_alpha()
    meio = pygame.image.load("assets/cenario/middle.png").convert_alpha()
    frente = pygame.image.load("assets/cenario/foreground.png").convert_alpha()
    for x in range(0, 688, fundo.get_width()):
        tela.blit(fundo, (x, 0))
    for x in range(0, 688, meio.get_width()):
        tela.blit(meio, (x, 0))
    tela.blit(frente, (0, 0))
    return tela


def carregar_cenario(numero):
    """Devolve a imagem (688x272) do cenario numero 0, 1 ou 2."""
    if numero == 0:
        return montar_centro()
    if numero == 1:
        return pygame.image.load("assets/cenario/cenario2.png").convert()
    return pygame.image.load("assets/cenario/cenario3.png").convert()
