import pygame
from interface import desenhar_barra_vida, desenhar_cronometro, iniciar_musica, carregar_som_soco
from lutador import Lutador, GOLPES_BRAWLER_GIRL, GOLPES_ENEMY_PUNK, atualizar_luta

LARGURA, ALTURA = 688, 272
ESCALA = 2
TEMPO_ROUND = 99    # segundos de cada round; ajustar depois de testar o dano

pygame.init()
som_soco = carregar_som_soco()
iniciar_musica()
fonte_cronometro = pygame.font.Font("assets/fontes/PressStart2P-Regular.ttf", 16)
janela = pygame.display.set_mode((LARGURA * ESCALA, ALTURA * ESCALA))
pygame.display.set_caption("Insper Fighter")
relogio = pygame.time.Clock()

tela = pygame.Surface((LARGURA, ALTURA))

cenario = pygame.image.load("assets/cenario/cenario2.png").convert_alpha()
CHAO = 230          # altura dos pes no cenario 2

# jogador 1: A/D anda, F soco, G chute
TECLAS_J1 = {"esquerda": pygame.K_a, "direita": pygame.K_d,
             "soco": pygame.K_f, "chute": pygame.K_g}
# jogador 2: setas andam, virgula soco, ponto soco forte
TECLAS_J2 = {"esquerda": pygame.K_LEFT, "direita": pygame.K_RIGHT,
             "soco": pygame.K_COMMA, "soco_forte": pygame.K_PERIOD}

jogador1 = Lutador("assets/sprites/brawler-girl", 200, CHAO, TECLAS_J1, GOLPES_BRAWLER_GIRL)
jogador2 = Lutador("assets/sprites/enemy-punk", 488, CHAO, TECLAS_J2, GOLPES_ENEMY_PUNK,
                   desenho_olha_direita=False)

mostrar_caixas = False      # TAB liga e desliga as caixas de colisao

inicio_round = pygame.time.get_ticks()
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_TAB:
            mostrar_caixas = not mostrar_caixas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e or evento.key == pygame.K_RSHIFT:
                som_soco.play()

    # teclas seguradas neste quadro (True/False para cada tecla do teclado)
    teclas = pygame.key.get_pressed()
    atualizar_luta(jogador1, jogador2, teclas)

    agora = pygame.time.get_ticks()
    tempo_passado = (agora - inicio_round) // 1000
    tempo_restante = TEMPO_ROUND - tempo_passado
    if tempo_restante < 0:
        tempo_restante = 0

    tela.fill((20, 20, 30))
    tela.blit(cenario, (0, 0))

    jogador1.desenhar(tela)
    jogador2.desenhar(tela)
    if mostrar_caixas:
        jogador1.desenhar_caixas(tela)
        jogador2.desenhar_caixas(tela)

    # interface por ultimo, para ficar por cima de tudo
    desenhar_barra_vida(tela, 20, 15, jogador1.vida)
    desenhar_barra_vida(tela, 418, 15, jogador2.vida, espelhada=True)
    desenhar_cronometro(tela, fonte_cronometro, tempo_restante)

    janela.blit(pygame.transform.scale(tela, janela.get_size()), (0, 0))
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
