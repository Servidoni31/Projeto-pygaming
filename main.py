import pygame
from interface import desenhar_barra_vida, desenhar_cronometro, iniciar_musica

LARGURA, ALTURA = 688, 272
ESCALA = 2
TEMPO_ROUND = 99    # segundos de cada round; ajustar depois de testar o dano

pygame.init()
iniciar_musica()
fonte_cronometro = pygame.font.Font("assets/fontes/PressStart2P-Regular.ttf", 16)
janela = pygame.display.set_mode((LARGURA * ESCALA, ALTURA * ESCALA))
pygame.display.set_caption("Insper Fighter")
relogio = pygame.time.Clock()

tela = pygame.Surface((LARGURA, ALTURA))

cenario = pygame.image.load("assets/cenario/cenario2.png").convert_alpha()

# folha de 4 quadros de 96x63, ampliada 2x -> quadros de 192x126
folha_idle = pygame.image.load("assets/sprites/brawler-girl/idle.png").convert_alpha()
folha_idle = pygame.transform.scale(folha_idle, (384 * 2, 63 * 2))
QUADRO_L, QUADRO_A = 96 * 2, 63 * 2

CHAO = 230          # altura dos pes no cenario 2
lutadora_x = 200    # centro do corpo da lutadora

iniciar_musica()

inicio_round = pygame.time.get_ticks()
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    agora = pygame.time.get_ticks()
    tempo_passado = (agora - inicio_round) // 1000
    tempo_restante = TEMPO_ROUND - tempo_passado
    if tempo_restante < 0:
        tempo_restante = 0

    tela.fill((20, 20, 30))
    tela.blit(cenario, (0, 0))

    # desenha o primeiro quadro: canto calculado a partir do centro e dos pes
    canto_x = lutadora_x - QUADRO_L // 2
    canto_y = CHAO - QUADRO_A
    tela.blit(folha_idle, (canto_x, canto_y), pygame.Rect(0, 0, QUADRO_L, QUADRO_A))

    # --- o resto do jogo entra aqui ---

    # interface por ultimo, para ficar por cima de tudo
    desenhar_barra_vida(tela, 20, 15, 100)
    desenhar_barra_vida(tela, 418, 15, 100, espelhada=True)
    desenhar_cronometro(tela, fonte_cronometro, tempo_restante)

    janela.blit(pygame.transform.scale(tela, janela.get_size()), (0, 0))
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
