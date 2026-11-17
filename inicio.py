# CONFIGURAÇÕES
import pygame

BRANCO = (255, 255, 255)
ESCURO = (12, 10, 24)
CINZA = (170, 177, 202)
AMARELO = (255, 207, 92)
AZUL = (40, 220, 210)
VERMELHO = (238, 76, 92)


def desenhar_texto(tela, fonte, texto, x, y, cor, escala=1):
    imagem = fonte.render(texto, False, cor)
    contorno = fonte.render(texto, False, ESCURO)
    tamanho = (imagem.get_width() * escala, imagem.get_height() * escala)
    imagem = pygame.transform.scale(imagem, tamanho)
    contorno = pygame.transform.scale(contorno, tamanho)
    posicao = imagem.get_rect(center=(x, y))
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                tela.blit(contorno, (posicao.x + dx, posicao.y + dy))
    tela.blit(imagem, posicao)

def desenhar_fundo(tela):
    tela.fill(ESCURO)
    for x in range(-272, 688, 64):
        pygame.draw.polygon(tela, (22, 23, 43), [
            (x, 272), (x + 28, 272), (x + 300, 0), (x + 272, 0)
        ])
    pygame.draw.rect(tela, AMARELO, (12, 12, 664, 248), 1)
    pygame.draw.line(tela, AZUL, (24, 218), (664, 218), 2)

def desenhar_inicio(tela, fonte):
    desenhar_fundo(tela)
    desenhar_texto(tela, fonte, "INSPER", 344, 68, AMARELO, 4)
    desenhar_texto(tela, fonte, "FIGHTER", 344, 115, BRANCO, 5)
    desenhar_texto(tela, fonte, "GUILHERME TREVES | JOAO DAMIANI | JOAO SERVIDONI",344, 153, AZUL)
    desenhar_texto(tela, fonte, "DOIS JOGADORES. UMA ARENA.", 344, 176, BRANCO)
    desenhar_texto(tela, fonte, "APERTE ENTER PARA COMECAR", 344, 204, AMARELO)
    desenhar_texto(tela, fonte, "ESC: SAIR", 344, 239, CINZA)


def desenhar_fight(tela, fonte):
    desenhar_texto(tela, fonte, "FIGHT!", 344, 136, BRANCO)


def desenhar_ko(tela, fonte):
    desenhar_texto(tela, fonte, "K.O.", 344, 136, BRANCO)


def desenhar_selecao_personagem(tela, fonte, nomes, imagens, selecionado, jogador):
    desenhar_fundo(tela)
    desenhar_texto(tela, fonte, "ESCOLHA SEU LUTADOR", 344, 34, BRANCO, 2)
    desenhar_texto(tela, fonte, "JOGADOR " + str(jogador), 344, 58, AZUL)

    for i in range(len(nomes)):
            x = 114 + i * 240
        cor = CINZA
        if i == selecionado:
            cor = AMARELO
        pygame.draw.rect(tela, (28, 30, 52), (x, 74, 220, 136))
        pygame.draw.rect(tela, cor, (x, 74, 220, 136), 2)
        posicao = imagens[i].get_rect(midbottom=(x + 110, 186))
        tela.blit(imagens[i], posicao)
        desenhar_texto(tela, fonte, nomes[i], x + 110, 196, cor)

    desenhar_texto(tela, fonte, "SETAS: ESCOLHER   ENTER: CONFIRMAR   ESC: VOLTAR", 344, 239, BRANCO)
    





