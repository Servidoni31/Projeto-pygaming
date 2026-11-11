# Referência dos assets

Medidas conferidas arquivo por arquivo. Use estes números no código em vez
de adivinhar.

## Sprites dos personagens

Todos os quadros, dos dois personagens, em todas as animações, têm
**96 × 63 pixels**. Sempre. Por isso o recorte é sempre:

```python
quadro = pygame.Rect(indice * 96, 0, 96, 63)
```

Como o tamanho é fixo, o personagem não escorrega de lado ao atacar — o
boneco fica centralizado na moldura e os membros esticados cabem na folga.

As folhas têm alpha de verdade, então é `convert_alpha()`, sem colorkey.

### brawler-girl

| Arquivo | Quadros |
|---|---|
| `idle.png` | 4 |
| `walk.png` | 10 |
| `punch.png` | 3 |
| `jab.png` | 3 |
| `kick.png` | 5 |
| `jump.png` | 4 |
| `jump_kick.png` | 3 |
| `dive_kick.png` | 5 |
| `hurt.png` | 2 |

### enemy-punk

| Arquivo | Quadros |
|---|---|
| `idle.png` | 4 |
| `walk.png` | 4 |
| `punch.png` | 3 |
| `hurt.png` | 4 |

O enemy-punk não tem chute nem pulo. Se os dois jogadores precisarem do
mesmo repertório, use a brawler-girl para os dois e repinte um deles.

### shadow.png

20 × 8. A sombra que vai sob os pés. Desenhe antes do personagem, centrada
na posição do chão.

## Cenários

Desenhe a cena numa superfície de **688 × 272** e escale ela por 2 no fim
de cada quadro. Os personagens são desenhados em **2×**.

### Cenário 1 — rua cyberpunk (em camadas, permite parallax)

| Arquivo | Tamanho | Papel |
|---|---|---|
| `cenario/back.png` | 112 × 272 | céu e fundo distante — repete na horizontal |
| `cenario/middle.png` | 256 × 272 | prédios do meio — repete na horizontal |
| `cenario/foreground.png` | 688 × 272 | a rua onde os lutadores pisam |

Chão (altura dos pés): **y = 256**

### Cenário 2 — calçada

| Arquivo | Tamanho |
|---|---|
| `cenario/cenario2.png` | 688 × 272 |

Imagem única, sem camadas. Chão: **y = 230**

Observação: este cenário foi montado a partir da imagem de divulgação do
pacote Streets of Fight, que vinha com dois lutadores desenhados nela. A
região foi coberta com uma faixa limpa da própria calçada. A versão sem o
remendo está em `material-original/streets-of-fight/`.

## Som

`som/trilha.ogg` — PyGame toca `.ogg` nativamente, sem biblioteca extra.
