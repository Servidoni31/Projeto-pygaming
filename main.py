import pygame

LARGURA, ALTURA = 688, 272
ESCALA = 2

pygame.init()
janela = pygame.display.set_mode((LARGURA * ESCALA, ALTURA * ESCALA))
pygame.display.set_caption("Nome do Jogo")
relogio = pygame.time.Clock()

tela = pygame.Surface((LARGURA, ALTURA))

cenario = pygame.image.load("assets/cenario/cenario2.png").convert_alpha()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((20, 20, 30))

    tela.blit(cenario, (0, 0))

    # --- o resto do jogo entra aqui ---

    janela.blit(pygame.transform.scale(tela, janela.get_size()), (0, 0))
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
