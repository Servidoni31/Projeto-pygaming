import pygame
from interface import (desenhar_barra_vida, desenhar_cronometro, iniciar_musica,
                       carregar_som_soco)
from lutador import atualizar_luta, criar_lutador
from personagens import PERSONAGENS
from sons import carregar_sons, tocar_efeito, tocar_vozes, atualizar_vozes

LARGURA, ALTURA = 688, 272
ESCALA = 2
TEMPO_ROUND = 99    # segundos de cada round; ajustar depois de testar o dano

pygame.init()
som_soco = carregar_som_soco()
iniciar_musica()
carregar_sons()
fonte_cronometro = pygame.font.Font("assets/fontes/PressStart2P-Regular.ttf", 16)
janela = pygame.display.set_mode((LARGURA * ESCALA, ALTURA * ESCALA))
pygame.display.set_caption("Insper Fighter")
relogio = pygame.time.Clock()

tela = pygame.Surface((LARGURA, ALTURA))

cenario = pygame.image.load("assets/cenario/cenario2.png").convert_alpha()
CHAO = 230          # altura dos pes no cenario 2

# jogador 1: A/D anda, F golpe 1, G golpe 2
TECLAS_J1 = {"esquerda": pygame.K_a, "direita": pygame.K_d,
             "golpe1": pygame.K_f, "golpe2": pygame.K_g}
# jogador 2: setas andam, virgula golpe 1, ponto golpe 2
TECLAS_J2 = {"esquerda": pygame.K_LEFT, "direita": pygame.K_RIGHT,
             "golpe1": pygame.K_COMMA, "golpe2": pygame.K_PERIOD}

# qual personagem cada jogador usa (posicao na lista PERSONAGENS);
# depois quem escolhe isso e a tela de selecao
ESCOLHA_J1 = 0      # Lutadora
ESCOLHA_J2 = 1      # Punk

jogador1 = criar_lutador(PERSONAGENS[ESCOLHA_J1], 200, CHAO, TECLAS_J1)
jogador2 = criar_lutador(PERSONAGENS[ESCOLHA_J2], 488, CHAO, TECLAS_J2)

mostrar_caixas = False      # TAB liga e desliga as caixas de colisao

inicio_round = pygame.time.get_ticks()
tocar_vozes(["ready", "fight"])
fim_anunciado = False       # o locutor ja falou quem ganhou?
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
    sons_acertos = atualizar_luta(jogador1, jogador2, teclas)
    for som in sons_acertos:
        tocar_efeito(som)

    agora = pygame.time.get_ticks()
    tempo_passado = (agora - inicio_round) // 1000
    tempo_restante = TEMPO_ROUND - tempo_passado
    if tempo_restante < 0:
        tempo_restante = 0

    # fim do round: alguem foi nocauteado ou o tempo acabou (por enquanto so o
    # locutor anuncia; a tela de K.O. e o proximo round entram aqui depois)
    if not fim_anunciado:
        if jogador1.vida == 0 or jogador2.vida == 0 or tempo_restante == 0:
            fim_anunciado = True
            falas = []
            if tempo_restante == 0:
                falas.append("time")
            if jogador1.vida > jogador2.vida:
                falas += ["player_1", "winner"]
            elif jogador2.vida > jogador1.vida:
                falas += ["player_2", "winner"]
            else:
                falas.append("empate")
            tocar_vozes(falas)
    atualizar_vozes()

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
