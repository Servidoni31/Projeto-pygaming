# [TÍTULO DO JOGO]

Jogo de luta 1 contra 1, local, para dois jogadores no mesmo teclado.
Projeto final de Design de Software — Insper, 2026/2.

## Integrantes

- João Pedro Servidoni — [Servidoni31](https://github.com/Servidoni31)
- João Damiani — [usuário do GitHub]
- Guilherme Treves — [usuário do GitHub]

## Vídeo

[LINK DO VÍDEO AQUI — exigido pelo enunciado, precisa estar acessível ao professor]

## Como rodar

Requisitos: Python 3 e PyGame.

```
pip install pygame-ce
python main.py
```

Atenção ao `pygame-ce`: em Python 3.13 e 3.14 o pacote `pygame` comum não
tem versão pré-compilada e o `pip install pygame` falha tentando compilar
do zero. O `pygame-ce` é a versão mantida pela comunidade, é instalada
normalmente nessas versões e se usa igual — o `import pygame` continua o
mesmo. Em Python 3.12 ou anterior, `pip install pygame` também funciona.

Testado em Python 3.14.6 com pygame-ce 2.5.8.

## Controles

| Ação | Jogador 1 | Jogador 2 |
|---|---|---|
| Andar | A / D | ← / → |
| Pular | W | ↑ |
| Soco | [tecla] | [tecla] |
| Chute | [tecla] | [tecla] |
| Defender | [tecla] | [tecla] |

## Objetivo

Zerar a vida do adversário antes do tempo acabar. Se o tempo terminar, vence
quem tiver mais vida.

## Créditos dos assets

Todos os assets usados estão em domínio público (CC0), sem obrigação de
atribuição. O crédito abaixo é por transparência.

- **Cenário 1 e trilha sonora** — "Cyberpunk Street Environment", por
  Luis Zuno (ansimuz) — CC0
  https://opengameart.org/content/cyberpunk-street-environment

- **Personagens e cenário 2** — "Streets of Fight", por Luis Zuno
  (ansimuz) — CC0
  https://opengameart.org/content/streets-of-fight

- **Cenário 3 e trilhas adicionais** — "Cyberpunk City 2", por Luis Zuno
  (ansimuz). Uso pessoal e comercial, modificação e redistribuição
  permitidas; crédito não obrigatório.
  https://ansimuz.itch.io/

O cenário 2 foi montado a partir da imagem de divulgação do pacote, que
vinha com dois lutadores desenhados nela; a região foi coberta com uma
faixa limpa da própria calçada.

Também foram avaliados durante a escolha, mas não utilizados:

- "Brawler Asset Character 'Vigilante' SMS", por Chasersgaming — CC0
  https://opengameart.org/content/brawler-asset-character-vigilante-sms
- "Agent Character", por Chasersgaming — CC0
  https://opengameart.org/content/agent-character
- "Platformer or Fighter Sprites", por Fracture — CC-BY-SA 3.0 / GPL 3.0
  https://opengameart.org/content/platformer-or-fighter-sprites
  Descartado por exigir share-alike e por não combinar em escala e paleta
  com o cenário escolhido.

## Uso de inteligência artificial

[Preencher antes da entrega. O enunciado exige:]

- proporção de código gerado por IA, com a fonte (link do histórico exportado)
- um parágrafo explicando como a IA foi usada no projeto
- as interações no Anexo
- comentário `# feito com CoPilot` em funções e classes sugeridas por IA

Todo o código entregue é compreendido pelos integrantes do grupo.
