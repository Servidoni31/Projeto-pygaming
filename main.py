import pygame
from interface import (desenhar_barra_vida, desenhar_cronometro, iniciar_musica,
                       carregar_som_soco)
from inicio import (desenhar_inicio, desenhar_selecao_personagem,
                    desenhar_selecao_cenario, desenhar_vitoria, desenhar_fight,
                    desenhar_ko, desenhar_tempo, miniatura_personagem,
                    imagem_vitoria)
from lutador import atualizar_luta, criar_lutador, NENHUMA_TECLA
from personagens import PERSONAGENS
from cenarios import CENARIOS, carregar_cenario
from sons import (carregar_sons, tocar_efeito, tocar_vozes, atualizar_vozes,
                  tocar_musica)

LARGURA, ALTURA = 688, 272
ESCALA = 2
TEMPO_ROUND = 99        # segundos de cada round
TEMPO_FIGHT = 1500      # ms com o "FIGHT!" na tela antes de poder lutar
TEMPO_KO = 2500         # ms com o "K.O." na tela antes da tela de vitoria

pygame.init()
som_soco = carregar_som_soco()
carregar_sons()
fonte_cronometro = pygame.font.Font("assets/fontes/PressStart2P-Regular.ttf", 16)
fonte_menu = pygame.font.Font("assets/fontes/PressStart2P-Regular.ttf", 8)
janela = pygame.display.set_mode((LARGURA * ESCALA, ALTURA * ESCALA))
pygame.display.set_caption("Insper Fighter")
relogio = pygame.time.Clock()
tela = pygame.Surface((LARGURA, ALTURA))

# jogador 1: A/D anda, W pula, F golpe 1, G golpe 2
TECLAS_J1 = {"esquerda": pygame.K_a, "direita": pygame.K_d, "cima": pygame.K_w,
             "golpe1": pygame.K_f, "golpe2": pygame.K_g}
# jogador 2: setas andam, seta para cima pula, virgula golpe 1, ponto golpe 2
TECLAS_J2 = {"esquerda": pygame.K_LEFT, "direita": pygame.K_RIGHT, "cima": pygame.K_UP,
             "golpe1": pygame.K_COMMA, "golpe2": pygame.K_PERIOD}


# ------------------------------------------------------------ imagens dos menus
nomes_personagens = []
miniaturas = []
for p in PERSONAGENS:
    nomes_personagens.append(p["nome"].upper())
    miniaturas.append(miniatura_personagem(p))

nomes_cenarios = []
imagens_cenarios = []
miniaturas_cenarios = []
# largura da miniatura: a mesma conta da carta em inicio.py, menos 12
largura_mini = (640 - 8 * (len(CENARIOS) - 1)) // len(CENARIOS) - 12
altura_mini = largura_mini * ALTURA // LARGURA
for i in range(len(CENARIOS)):
    nomes_cenarios.append(CENARIOS[i]["nome"])
    imagem = carregar_cenario(i)
    imagens_cenarios.append(imagem)
    miniaturas_cenarios.append(pygame.transform.scale(imagem, (largura_mini, altura_mini)))


# ------------------------------------------------------------ estado do jogo
# o jogo passa por estas telas, nesta ordem:
#   "inicio" -> "selecao_j1" -> "selecao_j2" -> "cenario" -> "luta" -> "vitoria"
estado = "inicio"
escolha_j1 = 0
escolha_j2 = 1
escolha_cenario = 1
cursor = 0              # carta destacada no menu atual
vencedor = 0            # 1, 2 ou 0 (empate)
mostrar_caixas = False  # TAB liga e desliga as caixas de colisao
luta_nova = False       # True: na proxima volta do loop, monta uma luta nova

tocar_musica("assets/som/menu.ogg", 0.3)
rodando = True
while rodando:
    agora = pygame.time.get_ticks()

    # ---------------------------------------------------------- eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type != pygame.KEYDOWN:
            continue
        tecla = evento.key

        if estado == "inicio":
            if tecla == pygame.K_RETURN:
                estado = "selecao_j1"
                cursor = escolha_j1
            elif tecla == pygame.K_ESCAPE:
                rodando = False

        elif estado == "selecao_j1" or estado == "selecao_j2":
            # setas andam na grade de 3 colunas x 2 linhas
            if tecla == pygame.K_RIGHT or tecla == pygame.K_d:
                cursor = (cursor + 1) % len(PERSONAGENS)
            elif tecla == pygame.K_LEFT or tecla == pygame.K_a:
                cursor = (cursor - 1) % len(PERSONAGENS)
            elif tecla == pygame.K_DOWN or tecla == pygame.K_s:
                cursor = (cursor + 3) % len(PERSONAGENS)
            elif tecla == pygame.K_UP or tecla == pygame.K_w:
                cursor = (cursor - 3) % len(PERSONAGENS)
            elif tecla == pygame.K_RETURN:
                if estado == "selecao_j1":
                    escolha_j1 = cursor
                    estado = "selecao_j2"
                    cursor = escolha_j2
                else:
                    escolha_j2 = cursor
                    estado = "cenario"
                    cursor = escolha_cenario
            elif tecla == pygame.K_ESCAPE:
                if estado == "selecao_j1":
                    estado = "inicio"
                else:
                    estado = "selecao_j1"
                    cursor = escolha_j1

        elif estado == "cenario":
            if tecla == pygame.K_RIGHT or tecla == pygame.K_d:
                cursor = (cursor + 1) % len(CENARIOS)
            elif tecla == pygame.K_LEFT or tecla == pygame.K_a:
                cursor = (cursor - 1) % len(CENARIOS)
            elif tecla == pygame.K_RETURN:
                escolha_cenario = cursor
                estado = "luta"
                luta_nova = True
            elif tecla == pygame.K_ESCAPE:
                estado = "selecao_j2"
                cursor = escolha_j2

        elif estado == "luta":
            if tecla == pygame.K_TAB:
                mostrar_caixas = not mostrar_caixas
            elif tecla == pygame.K_e or tecla == pygame.K_RSHIFT:
                som_soco.play()
            elif tecla == pygame.K_ESCAPE:
                estado = "inicio"
                tocar_musica("assets/som/menu.ogg", 0.3)

        elif estado == "vitoria":
            if tecla == pygame.K_RETURN:          # revanche
                estado = "luta"
                luta_nova = True
            elif tecla == pygame.K_c:             # nova selecao
                estado = "selecao_j1"
                cursor = escolha_j1
                tocar_musica("assets/som/menu.ogg", 0.3)
            elif tecla == pygame.K_ESCAPE:
                estado = "inicio"
                tocar_musica("assets/som/menu.ogg", 0.3)

    # ---------------------------------------------------------- telas de menu
    if estado == "inicio":
        desenhar_inicio(tela, fonte_menu)

    elif estado == "selecao_j1":
        desenhar_selecao_personagem(tela, fonte_menu, nomes_personagens, miniaturas,
                                    cursor, 1, None, PERSONAGENS[cursor]["descricao"])

    elif estado == "selecao_j2":
        desenhar_selecao_personagem(tela, fonte_menu, nomes_personagens, miniaturas,
                                    cursor, 2, escolha_j1, PERSONAGENS[cursor]["descricao"])

    elif estado == "cenario":
        desenhar_selecao_cenario(tela, fonte_menu, nomes_cenarios,
                                 miniaturas_cenarios, cursor)

    elif estado == "vitoria":
        if vencedor == 1:
            p = PERSONAGENS[escolha_j1]
        else:
            p = PERSONAGENS[escolha_j2]
        desenhar_vitoria(tela, fonte_menu, vencedor, p["nome"].upper(),
                         imagem_vitoria(p))

    # ---------------------------------------------------------- luta
    elif estado == "luta":
        # comeco de luta (depois da arena ou na revanche): cria os lutadores
        # escolhidos e zera o round
        if luta_nova:
            luta_nova = False
            chao = CENARIOS[escolha_cenario]["chao"]
            jogador1 = criar_lutador(PERSONAGENS[escolha_j1], 200, chao, TECLAS_J1)
            jogador2 = criar_lutador(PERSONAGENS[escolha_j2], 488, chao, TECLAS_J2)
            inicio_round = agora
            fim_round = None            # quando o round acabou (ms), ou None
            fim_anunciado = False       # o locutor ja falou quem ganhou?
            iniciar_musica()
            tocar_vozes(["ready", "fight"])

        tempo_passado = (agora - inicio_round) // 1000
        tempo_restante = TEMPO_ROUND - tempo_passado
        if tempo_restante < 0:
            tempo_restante = 0
        if fim_round is not None:       # o cronometro para quando o round acaba
            tempo_restante = max(0, TEMPO_ROUND - (fim_round - inicio_round) // 1000)

        # durante o "FIGHT!" ninguem se mexe; depois do K.O., so a animacao
        teclas = pygame.key.get_pressed()
        if agora - inicio_round < TEMPO_FIGHT or fim_round is not None:
            teclas = NENHUMA_TECLA
        sons_acertos = atualizar_luta(jogador1, jogador2, teclas)
        for som in sons_acertos:
            tocar_efeito(som)

        # fim do round: alguem foi nocauteado ou o tempo acabou
        if fim_round is None:
            if jogador1.vida == 0 or jogador2.vida == 0 or tempo_restante == 0:
                fim_round = agora
                if jogador1.vida > jogador2.vida:
                    vencedor = 1
                elif jogador2.vida > jogador1.vida:
                    vencedor = 2
                else:
                    vencedor = 0
        if fim_round is not None and not fim_anunciado:
            fim_anunciado = True
            falas = []
            if tempo_restante == 0:
                falas.append("time")
            if vencedor == 1:
                falas += ["player_1", "winner"]
            elif vencedor == 2:
                falas += ["player_2", "winner"]
            else:
                falas.append("empate")
            tocar_vozes(falas)
        if fim_round is not None and agora - fim_round > TEMPO_KO:
            estado = "vitoria"

        tela.blit(imagens_cenarios[escolha_cenario], (0, 0))
        jogador1.desenhar(tela)
        jogador2.desenhar(tela)
        if mostrar_caixas:
            jogador1.desenhar_caixas(tela)
            jogador2.desenhar_caixas(tela)

        # interface por ultimo, para ficar por cima de tudo
        desenhar_barra_vida(tela, 20, 15, jogador1.vida)
        desenhar_barra_vida(tela, 418, 15, jogador2.vida, espelhada=True)
        desenhar_cronometro(tela, fonte_cronometro, tempo_restante)
        if agora - inicio_round < TEMPO_FIGHT:
            desenhar_fight(tela, fonte_menu)
        if fim_round is not None:
            if jogador1.vida == 0 or jogador2.vida == 0:
                desenhar_ko(tela, fonte_menu)
            else:
                desenhar_tempo(tela, fonte_menu)

    atualizar_vozes()
    janela.blit(pygame.transform.scale(tela, janela.get_size()), (0, 0))
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
