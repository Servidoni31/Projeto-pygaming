import os
import pygame

# os golpes e os dados de cada personagem ficam em personagens.py; os dois
# primeiros sao importados aqui tambem para o codigo antigo continuar
# funcionando (from lutador import GOLPES_BRAWLER_GIRL, ...)
from personagens import GOLPES_BRAWLER_GIRL, GOLPES_ENEMY_PUNK  # noqa: F401

ESCALA = 2                  # escala padrao (personagens do Streets of Fight)
QUADRO_L = 192              # largura de um quadro na tela, ja ampliado
QUADRO_A = 126              # altura de um quadro na tela, ja ampliado
# na folha, o quadro tem QUADRO_L / escala de largura: 96x63 nos de escala 2
# e 64x42 nos de escala 3 (agente e renegade, que sao desenhados menores)

VELOCIDADE = 3              # pixels por quadro; a 60 quadros/s da 180 px/s
MEIO_CORPO = 24             # metade da largura do corpo (12 px x 2)
ALTURA_CORPO = 92           # altura do corpo (46 px x 2)
LIMITE_ESQ = MEIO_CORPO             # parede invisivel da esquerda
LIMITE_DIR = 688 - MEIO_CORPO       # parede invisivel da direita
EMPURRAO = 10               # quanto quem apanha e jogado para tras
FORCA_PULO = 10             # velocidade para cima no inicio do pulo (px por quadro)
GRAVIDADE = 0.5             # quanto a velocidade para cima diminui a cada quadro
# com esses numeros o pulo sobe 10 + 9,5 + 9 + ... = uns 105 px e dura uns 40
# quadros (0,7 s): da para passar por cima de um soco

# milissegundos que cada quadro fica na tela, por estado; golpe usa o padrao
TEMPO_QUADRO = {"parado": 110, "andando": 90, "apanhando": 110, "pulando": 120}
TEMPO_QUADRO_GOLPE = 70

# estados que repetem em loop; os outros tocam uma vez e acabam
ESTADOS_EM_LOOP = ["parado", "andando", "derrotado"]


def tecla_apertada(teclas, tecla):
    """Diz se a tecla esta apertada. "tecla" pode ser uma tecla so, uma lista
    de teclas (qualquer uma delas serve) ou None (golpe sem tecla)."""
    if tecla is None:
        return False
    if isinstance(tecla, list):
        for t in tecla:
            if teclas[t]:
                return True
        return False
    return teclas[tecla]


def carregar_folha(caminho, escala=ESCALA):
    """Carrega uma folha de sprites e devolve a lista dos quadros, ja ampliados.

    Os quadros ficam lado a lado na folha, cada um com QUADRO_L / escala de
    largura; o numero de quadros e a largura da folha dividida por isso.
    """
    folha = pygame.image.load(caminho).convert_alpha()
    n_quadros = folha.get_width() // (QUADRO_L // escala)
    folha = pygame.transform.scale(
        folha, (folha.get_width() * escala, folha.get_height() * escala)
    )
    quadros = []
    for i in range(n_quadros):
        recorte = pygame.Rect(i * QUADRO_L, 0, QUADRO_L, QUADRO_A)
        quadros.append(folha.subsurface(recorte))
    return quadros


class Lutador:
    """Um lutador: posicao, vida, teclas, golpes, animacao e desenho."""

    def __init__(self, pasta, x, chao, teclas, golpes, desenho_olha_direita=True,
                 escala=ESCALA):
        # cada estado tem a sua lista de quadros
        apanhando = carregar_folha(pasta + "/hurt.png", escala)
        self.animacoes = {
            "parado": carregar_folha(pasta + "/idle.png", escala),
            "andando": carregar_folha(pasta + "/walk.png", escala),
            "apanhando": apanhando,
        }
        # caido: usa o ko.png se o personagem tiver; senao, fica parado no
        # ultimo quadro do "apanhando"
        if os.path.exists(pasta + "/ko.png"):
            self.animacoes["derrotado"] = carregar_folha(pasta + "/ko.png", escala)
        else:
            self.animacoes["derrotado"] = [apanhando[-1]]
        # pulo: usa o jump.png se tiver; senao, pula com o 1o quadro do parado
        if os.path.exists(pasta + "/jump.png"):
            self.animacoes["pulando"] = carregar_folha(pasta + "/jump.png", escala)
        else:
            self.animacoes["pulando"] = [self.animacoes["parado"][0]]
        for nome in golpes:
            self.animacoes[nome] = carregar_folha(pasta + "/" + golpes[nome]["arquivo"],
                                                  escala)
        self.golpes = golpes
        # o 1o golpe do personagem usa a tecla "golpe1", o 2o usa "golpe2";
        # assim as mesmas teclas servem para qualquer personagem. Se o
        # dicionario de teclas usar o nome do golpe ("soco", "chute"), como no
        # codigo antigo, tambem funciona
        self.tecla_do_golpe = {}
        numero = 1
        for nome in golpes:
            tecla = teclas.get("golpe" + str(numero))
            if tecla is None:
                tecla = teclas.get(nome)
            self.tecla_do_golpe[nome] = tecla
            numero += 1

        sombra = pygame.image.load("assets/sprites/shadow.png").convert_alpha()
        self.sombra = pygame.transform.scale(sombra, (20 * ESCALA, 8 * ESCALA))

        self.x = x                  # centro do corpo (nao o canto do quadro)
        self.chao = chao            # altura dos pes
        self.teclas = teclas        # {"esquerda", "direita", "cima", "golpe1", "golpe2"}
        self.vida = 100
        self.altura = 0             # quanto esta acima do chao (pulando)
        self.vel_y = 0              # velocidade vertical (positiva = subindo)

        self.estado = "parado"
        self.quadro = 0                             # qual quadro da animacao
        self.ultima_troca = pygame.time.get_ticks() # quando o quadro mudou
        self.golpe_conferido = False    # o golpe atual ja tentou acertar?
        self.golpes_segurados = []      # teclas de golpe seguradas no quadro anterior

        self.olhando_direita = True
        # para que lado o desenho original da folha olha; a brawler-girl
        # olha para a direita, o enemy-punk (inimigo do pacote) para a esquerda
        self.desenho_olha_direita = desenho_olha_direita

    # ------------------------------------------------------------ estado
    def mudar_estado(self, novo):
        """Troca de estado e recomeca a animacao do primeiro quadro."""
        if novo != self.estado:
            self.estado = novo
            self.quadro = 0
            self.ultima_troca = pygame.time.get_ticks()

    def ocupado(self):
        """Enquanto golpeia, apanha ou esta no chao, nao anda nem golpeia."""
        return (self.estado in self.golpes
                or self.estado == "apanhando"
                or self.estado == "derrotado")

    # ------------------------------------------------------------ caixas
    def pes(self):
        """Altura dos pes na tela: o chao, menos o quanto subiu no pulo."""
        return self.chao - self.altura

    def caixa_corpo(self):
        """Retangulo onde o lutador pode ser atingido (sobe junto no pulo)."""
        return pygame.Rect(self.x - MEIO_CORPO, self.pes() - ALTURA_CORPO,
                           2 * MEIO_CORPO, ALTURA_CORPO)

    def caixa_golpe(self):
        """Retangulo que o golpe atual atinge, na frente do corpo."""
        alcance = self.golpes[self.estado]["alcance"]
        topo = self.pes() - 90      # no chao: da altura do peito a da cintura
        altura = 50
        if self.altura > 0:         # no ar: o golpe vai para baixo, ate os pes
            topo = self.pes() - 50
            altura = 60
        if self.olhando_direita:
            return pygame.Rect(self.x, topo, alcance, altura)
        return pygame.Rect(self.x - alcance, topo, alcance, altura)

    # ------------------------------------------------------------ a cada quadro
    def atualizar(self, teclas, outro):
        """Le as teclas, golpeia ou anda, avanca a animacao e confere acerto."""
        # 1) golpe novo: so quando a tecla acabou de ser apertada (estava solta
        #    no quadro anterior); segurar a tecla nao repete o golpe
        #    (golpe sem tecla definida e ignorado, em vez de travar o jogo)
        if not self.ocupado():
            for nome in self.golpes:
                apertada = tecla_apertada(teclas, self.tecla_do_golpe[nome])
                if apertada and nome not in self.golpes_segurados:
                    self.mudar_estado(nome)
                    self.golpe_conferido = False
                    break

        self.golpes_segurados = []
        for nome in self.golpes:
            if tecla_apertada(teclas, self.tecla_do_golpe[nome]):
                self.golpes_segurados.append(nome)

        # 2) andar, so se estiver livre (no ar tambem da para ir para os lados)
        if not self.ocupado():
            andou = False
            if teclas[self.teclas["esquerda"]]:
                self.x -= VELOCIDADE
                andou = True
            if teclas[self.teclas["direita"]]:
                self.x += VELOCIDADE
                andou = True
            if self.altura == 0 and self.estado != "pulando":
                if andou:
                    self.mudar_estado("andando")
                else:
                    self.mudar_estado("parado")

            # pular: so quem esta no chao
            tecla_cima = self.teclas.get("cima")
            if tecla_cima is not None and teclas[tecla_cima] and self.altura == 0:
                self.vel_y = FORCA_PULO
                self.mudar_estado("pulando")

        # fisica do pulo: sobe, a gravidade freia, desce e para no chao.
        # Vale em qualquer estado (quem apanha no ar tambem cai)
        if self.altura > 0 or self.vel_y > 0:
            self.altura += self.vel_y
            self.vel_y -= GRAVIDADE
            if self.altura <= 0:
                self.altura = 0
                self.vel_y = 0
                if self.estado == "pulando":
                    self.mudar_estado("parado")

        # investida: golpes com "investida" andam essa quantidade de pixels por
        # quadro para a frente, ate chegar no quadro do acerto
        if self.estado in self.golpes:
            golpe = self.golpes[self.estado]
            if "investida" in golpe and self.quadro < golpe["quadro_ativo"]:
                if self.olhando_direita:
                    self.x += golpe["investida"]
                else:
                    self.x -= golpe["investida"]

        self.prender_nas_paredes()

        # 3) animacao; quando um golpe ou o "apanhando" acaba, volta a ficar parado
        acabou = self.avancar_animacao()
        if acabou:
            if self.vida <= 0:
                self.mudar_estado("derrotado")
            elif self.altura > 0:
                self.mudar_estado("pulando")    # golpe no ar acabou: continua caindo
            else:
                self.mudar_estado("parado")

        # 4) no quadro em que o golpe esta esticado, confere se pegou o outro;
        #    cada golpe confere uma vez so, mesmo que o quadro dure varios ciclos.
        #    Aqui so DEVOLVE o dano: quem aplica e a atualizar_luta, depois que
        #    os dois lutadores ja se mexeram (ver la por que)
        if self.estado in self.golpes and not self.golpe_conferido:
            if self.quadro == self.golpes[self.estado]["quadro_ativo"]:
                self.golpe_conferido = True
                if self.caixa_golpe().colliderect(outro.caixa_corpo()):
                    return self.golpes[self.estado]["dano"]
        return 0

    def avancar_animacao(self):
        """Passa para o proximo quadro na hora certa.

        Devolve True quando uma animacao que nao repete chegou ao fim.
        """
        tempo = TEMPO_QUADRO.get(self.estado, TEMPO_QUADRO_GOLPE)
        # golpe com "tempo" proprio (como o soco forte) usa o dele
        if self.estado in self.golpes and "tempo" in self.golpes[self.estado]:
            tempo = self.golpes[self.estado]["tempo"]
        agora = pygame.time.get_ticks()
        if agora - self.ultima_troca < tempo:
            return False
        self.ultima_troca = agora
        self.quadro += 1
        total = len(self.animacoes[self.estado])
        if self.quadro >= total:
            if self.estado in ESTADOS_EM_LOOP:
                self.quadro = 0
            else:
                self.quadro = total - 1
                return True
        return False

    def levar_golpe(self, dano, x_atacante):
        """Perde vida, e jogado para tras e toca a animacao de apanhar."""
        if self.estado == "derrotado":
            return
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0
        if x_atacante < self.x:
            self.x += EMPURRAO
        else:
            self.x -= EMPURRAO
        self.prender_nas_paredes()
        # recomeca a animacao mesmo se ja estava apanhando
        self.estado = "apanhando"
        self.quadro = 0
        self.ultima_troca = pygame.time.get_ticks()

    def prender_nas_paredes(self):
        """Paredes invisiveis: puxa de volta se passou do limite."""
        if self.x < LIMITE_ESQ:
            self.x = LIMITE_ESQ
        if self.x > LIMITE_DIR:
            self.x = LIMITE_DIR

    def virar_para(self, outro):
        """Fica sempre de frente para o adversario (menos no meio de um golpe)."""
        if not self.ocupado():
            self.olhando_direita = outro.x > self.x

    # ------------------------------------------------------------ desenho
    def desenhar(self, tela):
        """Desenha sombra e quadro atual, com os pes em self.chao."""
        tela.blit(self.sombra, self.sombra.get_rect(center=(self.x, self.chao)))

        imagem = self.animacoes[self.estado][self.quadro]
        # so espelha quando o lado para onde ele deve olhar e diferente
        # do lado para onde o desenho original ja olha
        if self.olhando_direita != self.desenho_olha_direita:
            imagem = pygame.transform.flip(imagem, True, False)

        canto_x = self.x - QUADRO_L // 2
        canto_y = self.pes() - QUADRO_A     # a sombra fica no chao, o corpo sobe
        tela.blit(imagem, (canto_x, canto_y))

    def desenhar_caixas(self, tela):
        """Mostra as caixas de colisao (para testar e ajustar; tecla TAB)."""
        pygame.draw.rect(tela, (40, 220, 210), self.caixa_corpo(), 1)
        if self.estado in self.golpes:
            cor = (255, 60, 60)
            if self.quadro == self.golpes[self.estado]["quadro_ativo"]:
                cor = (255, 207, 92)
            pygame.draw.rect(tela, cor, self.caixa_golpe(), 1)


def atualizar_luta(j1, j2, teclas):
    """Atualiza os dois lutadores num quadro do jogo.

    Os acertos so sao aplicados depois que os DOIS se mexeram. Se o golpe do
    j1 fosse aplicado na hora, o j2 ja estaria apanhando quando chegasse a vez
    dele e o golpe dele sumiria: num empate, o jogador 1 sempre ganharia so por
    ser atualizado primeiro. Assim, se os dois acertam no mesmo quadro, os dois
    apanham.

    Devolve a lista dos sons dos golpes que acertaram neste quadro (ex.:
    ["medio"]), para o main tocar. Lista vazia: ninguem acertou.
    """
    dano1 = j1.atualizar(teclas, j2)
    dano2 = j2.atualizar(teclas, j1)
    # pega o som ANTES de aplicar o dano: depois o estado vira "apanhando"
    sons = []
    if dano1 > 0:
        sons.append(j1.golpes[j1.estado]["som"])
    if dano2 > 0:
        sons.append(j2.golpes[j2.estado]["som"])
    if dano1 > 0:
        j2.levar_golpe(dano1, j1.x)
    if dano2 > 0:
        j1.levar_golpe(dano2, j2.x)
    j1.virar_para(j2)
    j2.virar_para(j1)
    return sons


def criar_lutador(personagem, x, chao, teclas):
    """Cria o Lutador de um dos personagens da lista PERSONAGENS."""
    return Lutador(personagem["pasta"], x, chao, teclas, personagem["golpes"],
                   personagem["olha_direita"], personagem["escala"])


class NenhumaTecla:
    """Faz de conta que nenhuma tecla esta apertada (o main usa para travar os
    lutadores durante o "FIGHT!" e depois do K.O.). Funciona como o
    get_pressed(): NENHUMA_TECLA[pygame.K_a] da False."""
    def __getitem__(self, tecla):
        return False


NENHUMA_TECLA = NenhumaTecla()
