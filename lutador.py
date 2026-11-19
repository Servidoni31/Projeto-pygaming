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

DANO_NA_DEFESA = 40         # quem defende leva so 40% do dano do golpe
DURACAO_FAISCA = 150        # ms que a faisca do bloqueio fica na tela

# dash: toque duplo para um lado. Serve para fugir de combo: funciona ate
# apanhando, e durante o dash nenhum golpe pega
TOQUE_DUPLO = 250           # ms maximo entre os dois toques
QUADROS_DASH = 10           # quanto dura o dash (quadros)
VELOCIDADE_DASH = 7         # px por quadro: 10 x 7 = 70 px
RECARGA_DASH = 1200         # ms ate poder dar outro dash

# milissegundos que cada quadro fica na tela, por estado; golpe usa o padrao
TEMPO_QUADRO = {"parado": 110, "andando": 90, "apanhando": 110, "pulando": 120}
TEMPO_QUADRO_GOLPE = 70

# estados que repetem em loop; os outros tocam uma vez e acabam
ESTADOS_EM_LOOP = ["parado", "andando", "derrotado", "defendendo", "dash"]


# feito com Claude (IA)
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


# feito com Claude (IA)
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


# feito com Claude (IA)
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
        # defesa: nenhum pacote tem desenho de guarda; fica no 1o quadro do
        # parado e o escudo neon e desenhado por cima (ver desenhar)
        self.animacoes["defendendo"] = [self.animacoes["parado"][0]]
        self.ultimo_bloqueio = -10000   # quando bloqueou um golpe (para a faisca)
        # dash: usa os quadros do andar (com um rastro desenhado atras)
        self.animacoes["dash"] = self.animacoes["andando"]
        self.quadros_dash = 0           # quantos quadros de dash ainda faltam
        self.direcao_dash = 1           # 1 = para a direita, -1 = para a esquerda
        self.ultimo_dash = -10000       # quando deu o ultimo dash (para a recarga)
        self.ultimo_toque = {"esquerda": -10000, "direita": -10000}
        self.lados_segurados = []       # setas seguradas no quadro anterior
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
        """Enquanto golpeia, apanha, defende ou esta caido, nao anda nem golpeia."""
        return (self.estado in self.golpes
                or self.estado == "apanhando"
                or self.estado == "derrotado"
                or self.estado == "defendendo"
                or self.estado == "dash")

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
        # 0a) dash: toque duplo para um lado (apertou, soltou, apertou de novo
        #     em menos de TOQUE_DUPLO ms). Vale parado, andando, defendendo e
        #     ate apanhando (e o jeito de fugir de combo); no ar e caido, nao
        agora = pygame.time.get_ticks()
        for lado in ["esquerda", "direita"]:
            apertada = teclas[self.teclas[lado]]
            if apertada and lado not in self.lados_segurados:      # toque novo
                pode = (self.altura == 0
                        and self.estado in ["parado", "andando", "defendendo", "apanhando"]
                        and agora - self.ultimo_dash > RECARGA_DASH)
                if pode and agora - self.ultimo_toque[lado] < TOQUE_DUPLO:
                    self.direcao_dash = 1
                    if lado == "esquerda":
                        self.direcao_dash = -1
                    self.quadros_dash = QUADROS_DASH
                    self.ultimo_dash = agora
                    self.mudar_estado("dash")
                self.ultimo_toque[lado] = agora
        self.lados_segurados = []
        for lado in ["esquerda", "direita"]:
            if teclas[self.teclas[lado]]:
                self.lados_segurados.append(lado)

        if self.estado == "dash":
            self.x += VELOCIDADE_DASH * self.direcao_dash
            self.quadros_dash -= 1
            if self.quadros_dash <= 0:
                self.mudar_estado("parado")

        # 0b) defesa: enquanto segura "baixo" no chao, fica na guarda (nao anda
        #    nem golpeia); soltou, volta a ficar parado
        tecla_baixo = self.teclas.get("baixo")
        quer_defender = (tecla_baixo is not None and teclas[tecla_baixo]
                         and self.altura == 0)
        if self.estado == "defendendo" and not quer_defender:
            self.mudar_estado("parado")
        elif quer_defender and not self.ocupado():
            self.mudar_estado("defendendo")

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
        """Perde vida, e jogado para tras e toca a animacao de apanhar.

        Se estiver defendendo, leva so DANO_NA_DEFESA % do dano, e empurrado
        a metade e continua na guarda (nao cambaleia). No meio de um dash,
        o golpe nao pega. Devolve "acertou", "bloqueou" ou "desviou".
        """
        if self.estado == "derrotado" or self.estado == "dash":
            return "desviou"
        bloqueou = self.estado == "defendendo"
        empurrao = EMPURRAO
        if bloqueou:
            dano = dano * DANO_NA_DEFESA // 100
            empurrao = EMPURRAO // 2
            self.ultimo_bloqueio = pygame.time.get_ticks()
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0
        if x_atacante < self.x:
            self.x += empurrao
        else:
            self.x -= empurrao
        self.prender_nas_paredes()
        if bloqueou:
            return "bloqueou"
        # recomeca a animacao mesmo se ja estava apanhando
        self.estado = "apanhando"
        self.quadro = 0
        self.ultima_troca = pygame.time.get_ticks()
        return "acertou"

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

        # dash: duas copias meio transparentes atras, como um rastro
        if self.estado == "dash":
            for passo, transparencia in [(2, 60), (1, 120)]:
                rastro = imagem.copy()
                rastro.set_alpha(transparencia)
                atras = canto_x - self.direcao_dash * VELOCIDADE_DASH * 2 * passo
                tela.blit(rastro, (atras, canto_y))

        tela.blit(imagem, (canto_x, canto_y))

        # defendendo: um escudo neon na frente do corpo; quando acabou de
        # bloquear um golpe, ele pisca mais forte e mais largo (a "faisca")
        if self.estado == "defendendo":
            frente = 30
            if not self.olhando_direita:
                frente = -30
            x = self.x + frente
            topo = self.pes() - 84
            cor = (40, 226, 214)
            largura = 2
            if pygame.time.get_ticks() - self.ultimo_bloqueio < DURACAO_FAISCA:
                cor = (255, 255, 255)
                largura = 4
            pygame.draw.line(tela, cor, (x, topo), (x, topo + 64), largura)
            # pontas do escudo, viradas para o lado do corpo
            volta = -6
            if not self.olhando_direita:
                volta = 6
            pygame.draw.line(tela, cor, (x, topo), (x + volta, topo - 6), largura)
            pygame.draw.line(tela, cor, (x, topo + 64), (x + volta, topo + 70), largura)

    def desenhar_caixas(self, tela):
        """Mostra as caixas de colisao (para testar e ajustar; tecla TAB)."""
        pygame.draw.rect(tela, (40, 220, 210), self.caixa_corpo(), 1)
        if self.estado in self.golpes:
            cor = (255, 60, 60)
            if self.quadro == self.golpes[self.estado]["quadro_ativo"]:
                cor = (255, 207, 92)
            pygame.draw.rect(tela, cor, self.caixa_golpe(), 1)


# feito com Claude (IA)
def atualizar_luta(j1, j2, teclas):
    """Atualiza os dois lutadores num quadro do jogo.

    Os acertos so sao aplicados depois que os DOIS se mexeram. Se o golpe do
    j1 fosse aplicado na hora, o j2 ja estaria apanhando quando chegasse a vez
    dele e o golpe dele sumiria: num empate, o jogador 1 sempre ganharia so por
    ser atualizado primeiro. Assim, se os dois acertam no mesmo quadro, os dois
    apanham.

    Devolve a lista dos sons dos golpes que acertaram neste quadro (ex.:
    ["medio"]), para o main tocar. Lista vazia: ninguem acertou. Golpe
    bloqueado toca o som "fraco".
    """
    dano1 = j1.atualizar(teclas, j2)
    dano2 = j2.atualizar(teclas, j1)
    # pega o som ANTES de aplicar o dano: depois o estado vira "apanhando"
    som1 = None
    som2 = None
    if dano1 > 0:
        som1 = j1.golpes[j1.estado]["som"]
    if dano2 > 0:
        som2 = j2.golpes[j2.estado]["som"]
    sons = []
    if dano1 > 0:
        resultado = j2.levar_golpe(dano1, j1.x)
        if resultado == "bloqueou":
            sons.append("fraco")
        elif resultado == "acertou":
            sons.append(som1)
    if dano2 > 0:
        resultado = j1.levar_golpe(dano2, j2.x)
        if resultado == "bloqueou":
            sons.append("fraco")
        elif resultado == "acertou":
            sons.append(som2)
    j1.virar_para(j2)
    j2.virar_para(j1)
    return sons


# feito com Claude (IA)
def criar_lutador(personagem, x, chao, teclas):
    """Cria o Lutador de um dos personagens da lista PERSONAGENS."""
    return Lutador(personagem["pasta"], x, chao, teclas, personagem["golpes"],
                   personagem["olha_direita"], personagem["escala"])


# feito com Claude (IA)
class NenhumaTecla:
    """Faz de conta que nenhuma tecla esta apertada (o main usa para travar os
    lutadores durante o "FIGHT!" e depois do K.O.). Funciona como o
    get_pressed(): NENHUMA_TECLA[pygame.K_a] da False."""
    def __getitem__(self, tecla):
        return False


NENHUMA_TECLA = NenhumaTecla()
