# So dados: os golpes e a lista de personagens. Este arquivo nao importa nada,
# para o lutador.py poder importar daqui sem import circular.

# Golpes de cada personagem, na ordem das teclas: o 1o golpe sai na tecla
# "golpe1" e o 2o na "golpe2".
#   arquivo      - folha da animacao do golpe
#   dano         - quanto de vida tira
#   alcance      - ate onde o golpe chega, a frente do centro do corpo (px na tela)
#   quadro_ativo - quadro da animacao em que o golpe pode acertar
#   tempo        - ms por quadro (opcional; sem ele, 70): maior = golpe mais lento
#   investida    - px por quadro que o lutador avanca ate o acerto (opcional)
#   som          - efeito que toca no acerto ("fraco", "medio" ou "forte")

GOLPES_BRAWLER_GIRL = {
    # soco: o de maior alcance do jogo, mas fraco (uma "cutucada"); de perto,
    # empata em tempo com o soco do punk e os dois se acertam
    "soco":  {"arquivo": "punch.png", "dano": 5,  "alcance": 78, "quadro_ativo": 1,
              "tempo": 120, "som": "fraco"},
    "chute": {"arquivo": "kick.png",  "dano": 12, "alcance": 66, "quadro_ativo": 3,
              "som": "medio"},
}
# o enemy-punk so tem a animacao de soco no pacote (nao existe chute nem no
# arquivo .ase original). Para ele ter dois golpes como a lutadora, o segundo
# e um "soco forte": a mesma animacao, mais lenta, com uma investida para a
# frente ate o quadro do acerto. Bate mais e chega mais longe, mas e lento.
GOLPES_ENEMY_PUNK = {
    "soco":       {"arquivo": "punch.png", "dano": 10, "alcance": 68, "quadro_ativo": 2,
                   "tempo": 55, "som": "medio"},
    "soco_forte": {"arquivo": "punch.png", "dano": 14, "alcance": 76, "quadro_ativo": 2,
                   "tempo": 130, "investida": 2, "som": "forte"},
}
# ninja: soco rapido e fraco; a voadora atravessa a tela
# (ninja, ilusionista, agente e renegade sao desenhados menores que a lutadora
# e o punk; o alcance deles e um pouco maior que o braco no desenho, para os
# golpes chegarem na mesma distancia dos personagens principais)
GOLPES_NINJA = {
    "soco":     {"arquivo": "punch.png", "dano": 6, "alcance": 66, "quadro_ativo": 1,
                 "tempo": 90, "som": "fraco"},
    "voadora":  {"arquivo": "flying_kick.png", "dano": 11, "alcance": 62, "quadro_ativo": 2,
                 "tempo": 110, "investida": 4, "som": "forte"},
}
# ilusionista: soco normal e uma investida com o ombro
GOLPES_ILUSIONISTA = {
    "soco":      {"arquivo": "punch.png", "dano": 7,  "alcance": 68, "quadro_ativo": 2,
                  "tempo": 60, "som": "fraco"},
    "investida": {"arquivo": "lunge.png", "dano": 11, "alcance": 66, "quadro_ativo": 2,
                  "tempo": 80, "investida": 3, "som": "medio"},
}
# agente: o de terno, de outro "jogo"
GOLPES_AGENTE = {
    "soco":  {"arquivo": "punch.png", "dano": 7,  "alcance": 66, "quadro_ativo": 1,
              "tempo": 100, "som": "medio"},
    "chute": {"arquivo": "kick.png",  "dano": 10, "alcance": 80, "quadro_ativo": 1,
              "tempo": 150, "som": "medio"},
}
# renegade: lento e pesado, o chute e o golpe mais forte do jogo
GOLPES_RENEGADE = {
    "soco":  {"arquivo": "punch.png", "dano": 8,  "alcance": 64, "quadro_ativo": 1,
              "tempo": 110, "som": "medio"},
    "chute": {"arquivo": "kick.png",  "dano": 13, "alcance": 78, "quadro_ativo": 1,
              "tempo": 170, "som": "forte"},
}

# Todos os personagens do jogo. "olha_direita": para que lado o desenho
# original olha; "escala": quanto a folha e ampliada na tela.
PERSONAGENS = [
    {"nome": "Lutadora",    "pasta": "assets/sprites/brawler-girl",
     "golpes": GOLPES_BRAWLER_GIRL, "olha_direita": True,  "escala": 2},
    {"nome": "Punk",        "pasta": "assets/sprites/enemy-punk",
     "golpes": GOLPES_ENEMY_PUNK,   "olha_direita": False, "escala": 2},
    {"nome": "Ninja",       "pasta": "assets/sprites/ninja",
     "golpes": GOLPES_NINJA,        "olha_direita": True,  "escala": 2},
    {"nome": "Ilusionista", "pasta": "assets/sprites/ilusionista",
     "golpes": GOLPES_ILUSIONISTA,  "olha_direita": True,  "escala": 2},
    {"nome": "Agente Smith", "pasta": "assets/sprites/agente",
     "golpes": GOLPES_AGENTE,       "olha_direita": True,  "escala": 3},
    {"nome": "Renegade",    "pasta": "assets/sprites/renegade",
     "golpes": GOLPES_RENEGADE,     "olha_direita": True,  "escala": 3},
]
