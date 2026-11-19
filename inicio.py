import pygame

BRANCO = (255, 255, 255)
ESCURO = (12, 10, 24)
CINZA = (170, 177, 202)
AMARELO = (255, 207, 92)
AZUL = (40, 220, 210)


def desenhar_texto(tela, fonte, texto, x, y, cor, escala=1):
    imagem = fonte.render(texto, False, cor)
    contorno = fonte.render(texto, False, ESCURO)
    largura = imagem.get_width() * escala
    altura = imagem.get_height() * escala
    imagem = pygame.transform.scale(imagem, (largura, altura))
    contorno = pygame.transform.scale(contorno, (largura, altura))
    posicao = imagem.get_rect(center=(x, y))

    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                tela.blit(contorno, (posicao.x + dx, posicao.y + dy))

    tela.blit(imagem, posicao)


def desenhar_fundo(tela):
    tela.fill(ESCURO)

    for x in range(-272, 688, 64):
        pontos = [
            (x, 272),
            (x + 28, 272),
            (x + 300, 0),
            (x + 272, 0)
        ]
        pygame.draw.polygon(tela, (22, 23, 43), pontos)

    pygame.draw.rect(tela, AMARELO, (12, 12, 664, 248), 1)
    pygame.draw.line(tela, AZUL, (24, 218), (664, 218), 2)


def desenhar_inicio(tela, fonte):
    desenhar_fundo(tela)
    desenhar_texto(tela, fonte, "INSPER", 344, 68, AMARELO, 4)
    desenhar_texto(tela, fonte, "FIGHTER", 344, 115, BRANCO, 5)
    desenhar_texto(tela, fonte, "GUILHERME TREVES | JOAO DAMIANI | JOAO SERVIDONI",
                   344, 153, AZUL)
    desenhar_texto(tela, fonte, "DOIS JOGADORES. UMA ARENA.", 344, 176, BRANCO)
    desenhar_texto(tela, fonte, "APERTE ENTER PARA COMECAR", 344, 204, AMARELO)
    desenhar_texto(tela, fonte, "ESC: SAIR", 344, 239, CINZA)


# feito pelo Treves, ajustado com Claude (IA)
def desenhar_fight(tela, fonte):
    desenhar_texto(tela, fonte, "FIGHT!", 344, 120, AMARELO, 5)


# feito pelo Treves, ajustado com Claude (IA)
def desenhar_ko(tela, fonte):
    desenhar_texto(tela, fonte, "K.O.", 344, 120, AMARELO, 6)


# feito com Claude (IA)
def desenhar_tempo(tela, fonte):
    desenhar_texto(tela, fonte, "TEMPO!", 344, 120, AMARELO, 5)


# feito pelo Treves, adaptado com Claude (IA)
def desenhar_selecao_personagem(tela, fonte, nomes, imagens, selecionado, jogador,
                                escolha_j1=None, descricao=""):
    desenhar_fundo(tela)
    desenhar_texto(tela, fonte, "ESCOLHA SEU LUTADOR", 344, 26, BRANCO, 2)
    desenhar_texto(tela, fonte, "JOGADOR " + str(jogador), 344, 50, AZUL)

    # cartas em grade: 3 por linha (cabem os 6 personagens em 2 linhas)
    for i in range(len(nomes)):
        coluna = i % 3
        linha = i // 3
        x = 32 + coluna * 212
        y = 62 + linha * 76
        cor = CINZA

        if i == selecionado:
            cor = AMARELO

        pygame.draw.rect(tela, (28, 30, 52), (x, y, 200, 70))
        pygame.draw.rect(tela, cor, (x, y, 200, 70), 2)
        posicao = imagens[i].get_rect(midbottom=(x + 44, y + 66))
        tela.blit(imagens[i], posicao)
        desenhar_texto(tela, fonte, nomes[i], x + 134, y + 35, cor)

        # na vez do jogador 2, marca quem o jogador 1 ja escolheu
        if escolha_j1 == i:
            desenhar_texto(tela, fonte, "J1", x + 184, y + 12, AZUL)

    # descricao do personagem destacado, logo abaixo das cartas
    desenhar_texto(tela, fonte, descricao, 344, 229, AMARELO)

    desenhar_texto(tela, fonte, "SETAS: ESCOLHER   ENTER: CONFIRMAR   ESC: VOLTAR",
                   344, 246, BRANCO)


# feito pelo Treves, adaptado com Claude (IA)
def desenhar_selecao_cenario(tela, fonte, nomes, miniaturas, selecionado):
    desenhar_fundo(tela)
    desenhar_texto(tela, fonte, "ESCOLHA A ARENA", 344, 34, BRANCO, 2)
    desenhar_texto(tela, fonte, "ONDE VAI SER A DISPUTA?", 344, 58, AZUL)

    # arenas lado a lado; a largura da carta depende de quantas sao, e a
    # miniatura tem a largura da carta menos 12 (6 de cada lado)
    largura = (640 - 8 * (len(nomes) - 1)) // len(nomes)
    for i in range(len(nomes)):
        x = 24 + i * (largura + 8)
        cor = CINZA

        if i == selecionado:
            cor = AMARELO

        altura = miniaturas[i].get_height() + 34
        pygame.draw.rect(tela, (28, 30, 52), (x, 84, largura, altura))
        tela.blit(miniaturas[i], (x + 6, 90))
        pygame.draw.rect(tela, cor, (x, 84, largura, altura), 2)
        desenhar_texto(tela, fonte, nomes[i], x + largura // 2, 84 + altura - 13, cor)

    desenhar_texto(tela, fonte, "SETAS: ESCOLHER   ENTER: CONFIRMAR   ESC: VOLTAR", 344, 239, BRANCO)


def desenhar_vitoria(tela, fonte, vencedor, nome_personagem, imagem):
    desenhar_fundo(tela)

    if vencedor == 0:
        desenhar_texto(tela, fonte, "EMPATE", 344, 80, AMARELO, 4)
        desenhar_texto(tela, fonte, "A RIVALIDADE CONTINUA!", 344, 145, BRANCO)
    else:
        desenhar_texto(tela, fonte, "VITORIA!", 344, 43, AMARELO, 3)
        posicao = imagem.get_rect(midbottom=(205, 204))
        tela.blit(imagem, posicao)
        desenhar_texto(tela, fonte, "JOGADOR " + str(vencedor), 451, 108, BRANCO, 2)
        desenhar_texto(tela, fonte, nome_personagem, 451, 145, AZUL)
        desenhar_texto(tela, fonte, "VENCEU O ROUND", 451, 172, AMARELO)

    desenhar_texto(tela, fonte, "ENTER: REVANCHE   C: NOVA SELECAO   ESC: INICIO", 344, 239, BRANCO)








# feito com Claude (IA)
def primeiro_quadro_parado(personagem):
    """Primeiro quadro do 'parado' do personagem, recortado (sem a sobra
    transparente em volta), no tamanho original da folha."""
    folha = pygame.image.load(personagem["pasta"] + "/idle.png").convert_alpha()
    largura = 192 // personagem["escala"]
    quadro = folha.subsurface((0, 0, largura, folha.get_height()))
    return quadro.subsurface(quadro.get_bounding_rect())


# feito com Claude (IA)
def miniatura_personagem(personagem):
    """Desenho do personagem no tamanho da carta da tela de selecao."""
    quadro = primeiro_quadro_parado(personagem)
    fator = personagem["escala"] / 2      # escala 3 fica 1,5x maior
    return pygame.transform.scale_by(quadro, fator)


# feito com Claude (IA)
def imagem_vitoria(personagem):
    """Desenho do personagem no tamanho da luta, para a tela de vitoria."""
    quadro = primeiro_quadro_parado(personagem)
    imagem = pygame.transform.scale_by(quadro, personagem["escala"])
    if not personagem["olha_direita"]:
        imagem = pygame.transform.flip(imagem, True, False)
    return imagem
