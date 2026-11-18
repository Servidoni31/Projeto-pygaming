import random
import pygame

# efeitos de golpe: cada tipo tem algumas variacoes e uma e sorteada a cada
# acerto, para nao soar sempre igual
EFEITOS = {
    "fraco": ["soco_fraco1.ogg", "soco_fraco2.ogg", "soco_fraco3.ogg"],
    "medio": ["golpe_medio1.ogg", "golpe_medio2.ogg", "golpe_medio3.ogg"],
    "forte": ["golpe_forte1.ogg", "golpe_forte2.ogg"],
}
# falas do locutor
VOZES = ["fight", "ready", "winner", "player_1", "player_2", "time", "empate"]

VOLUME_EFEITOS = 0.7
VOLUME_VOZ = 0.9

efeitos = {}    # "fraco" -> [Sound, Sound, ...]
vozes = {}      # "fight" -> Sound


def carregar_sons():
    """Carrega todos os sons. Chamar uma vez, depois do pygame.init()."""
    pygame.mixer.set_reserved(1)    # canal 0 so para a voz do locutor
    for tipo in EFEITOS:
        efeitos[tipo] = []
        for arquivo in EFEITOS[tipo]:
            som = pygame.mixer.Sound("assets/som/efeitos/" + arquivo)
            som.set_volume(VOLUME_EFEITOS)
            efeitos[tipo].append(som)
    for nome in VOZES:
        som = pygame.mixer.Sound("assets/som/voz/" + nome + ".ogg")
        som.set_volume(VOLUME_VOZ)
        vozes[nome] = som


def tocar_efeito(tipo):
    """Toca uma das variacoes do efeito ("fraco", "medio" ou "forte")."""
    random.choice(efeitos[tipo]).play()


fila_vozes = []  # falas esperando a vez, na ordem


def tocar_vozes(nomes):
    """Poe falas na fila para tocarem uma depois da outra.

    Ex.: tocar_vozes(["time", "player_1", "winner"]). Elas so tocam de
    verdade na atualizar_vozes, que o main chama a cada quadro.
    """
    for nome in nomes:
        fila_vozes.append(nome)


def atualizar_vozes():
    """Se o locutor esta calado e tem fala na fila, toca a proxima."""
    # o canal 0 fica reservado para a voz, assim os efeitos nunca a cortam
    canal = pygame.mixer.Channel(0)
    if len(fila_vozes) > 0 and not canal.get_busy():
        nome = fila_vozes.pop(0)
        canal.play(vozes[nome])


def tocar_musica(arquivo, volume):
    """Troca a musica de fundo (repete sem parar)."""
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
