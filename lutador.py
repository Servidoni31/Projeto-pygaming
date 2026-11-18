import pygame

ESCALA = 2
QUADRO_L = 96 * ESCALA      # largura de um quadro da folha, ja ampliado (192)
QUADRO_A = 63 * ESCALA      # altura de um quadro da folha, ja ampliado (126)

VELOCIDADE = 3              # pixels por quadro; a 60 quadros/s da 180 px/s
MEIO_CORPO = 24             # metade da largura do corpo (12 px x 2)
ALTURA_CORPO = 92           # altura do corpo (46 px x 2)
LIMITE_ESQ = MEIO_CORPO             # parede invisivel da esquerda
LIMITE_DIR = 688 - MEIO_CORPO       # parede invisivel da direita
EMPURRAO = 10               # quanto quem apanha e jogado para tras

# milissegundos que cada quadro fica na tela, por estado; golpe usa o padrao
TEMPO_QUADRO = {"parado": 110, "andando": 90, "apanhando": 110}
TEMPO_QUADRO_GOLPE = 70

# estados que repetem em loop; os outros tocam uma vez e acabam
ESTADOS_EM_LOOP = ["parado", "andando", "derrotado"]

# golpes de cada personagem. "alcance" e quanto o golpe chega a frente do
# centro do corpo (medido nos quadros da folha, x2); "quadro_ativo" e o
# quadro da animacao em que o braco ou a perna esta esticado e pode acertar
GOLPES_BRAWLER_GIRL = {
    # soco: o de maior alcance do jogo, mas fraco (uma "cutucada"); de perto,
    # empata em tempo com o soco do punk e os dois se acertam
    "soco":  {"arquivo": "punch.png", "dano": 5,  "alcance": 78, "quadro_ativo": 1,
              "tempo": 120},
    "chute": {"arquivo": "kick.png",  "dano": 12, "alcance": 66, "quadro_ativo": 3},
}
# o enemy-punk so tem a animacao de soco no pacote (nao existe chute nem no
# arquivo .ase original). Para ele ter dois golpes como a lutadora, o segundo
# e um "soco forte": a mesma animacao, mais lenta ("tempo" por quadro), com uma
# investida para a frente ate o quadro do acerto. Bate mais e chega mais longe,
# mas e lento: da tempo de o outro recuar.
GOLPES_ENEMY_PUNK = {
    "soco":       {"arquivo": "punch.png", "dano": 10, "alcance": 68, "quadro_ativo": 2,
                   "tempo": 55},
    "soco_forte": {"arquivo": "punch.png", "dano": 14, "alcance": 76, "quadro_ativo": 2,
                   "tempo": 130, "investida": 2},
}


def carregar_folha(caminho):
    """Carrega uma folha de sprites e devolve a lista dos quadros, ja ampliados.

    Toda folha do pacote tem quadros de 96x63 lado a lado, entao o numero de
    quadros e a largura da folha dividida por 96.
    """
    folha = pygame.image.load(caminho).convert_alpha()
    n_quadros = folha.get_width() // 96
    folha = pygame.transform.scale(
        folha, (folha.get_width() * ESCALA, folha.get_height() * ESCALA)
    )
    quadros = []
    for i in range(n_quadros):
        recorte = pygame.Rect(i * QUADRO_L, 0, QUADRO_L, QUADRO_A)
        quadros.append(folha.subsurface(recorte))
    return quadros


class Lutador:
    """Um lutador: posicao, vida, teclas, golpes, animacao e desenho."""

    def __init__(self, pasta, x, chao, teclas, golpes, desenho_olha_direita=True):
        # cada estado tem a sua lista de quadros
        apanhando = carregar_folha(pasta + "/hurt.png")
        self.animacoes = {
            "parado": carregar_folha(pasta + "/idle.png"),
            "andando": carregar_folha(pasta + "/walk.png"),
            "apanhando": apanhando,
            "derrotado": [apanhando[-1]],   # fica parado no ultimo quadro
        }
        for nome in golpes:
            self.animacoes[nome] = carregar_folha(pasta + "/" + golpes[nome]["arquivo"])
        self.golpes = golpes

        sombra = pygame.image.load("assets/sprites/shadow.png").convert_alpha()
        self.sombra = pygame.transform.scale(sombra, (20 * ESCALA, 8 * ESCALA))

        self.x = x                  # centro do corpo (nao o canto do quadro)
        self.chao = chao            # altura dos pes
        self.teclas = teclas        # {"esquerda": .., "direita": .., "soco": .., ...}
        self.vida = 100

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
    def caixa_corpo(self):
        """Retangulo onde o lutador pode ser atingido."""
        return pygame.Rect(self.x - MEIO_CORPO, self.chao - ALTURA_CORPO,
                           2 * MEIO_CORPO, ALTURA_CORPO)

    def caixa_golpe(self):
        """Retangulo que o golpe atual atinge, na frente do corpo."""
        alcance = self.golpes[self.estado]["alcance"]
        topo = self.chao - 90
        altura = 50
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
                tecla = self.teclas.get(nome)
                if tecla is None:
                    continue
                if teclas[tecla] and nome not in self.golpes_segurados:
                    self.mudar_estado(nome)
                    self.golpe_conferido = False
                    break

        self.golpes_segurados = []
        for nome in self.golpes:
            tecla = self.teclas.get(nome)
            if tecla is not None and teclas[tecla]:
                self.golpes_segurados.append(nome)

        # 2) andar, so se estiver livre
        if not self.ocupado():
            andou = False
            if teclas[self.teclas["esquerda"]]:
                self.x -= VELOCIDADE
                andou = True
            if teclas[self.teclas["direita"]]:
                self.x += VELOCIDADE
                andou = True
            if andou:
                self.mudar_estado("andando")
            else:
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
        canto_y = self.chao - QUADRO_A
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
    """
    dano1 = j1.atualizar(teclas, j2)
    dano2 = j2.atualizar(teclas, j1)
    if dano1 > 0:
        j2.levar_golpe(dano1, j1.x)
    if dano2 > 0:
        j1.levar_golpe(dano2, j2.x)
    j1.virar_para(j2)
    j2.virar_para(j1)
