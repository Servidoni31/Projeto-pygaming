# Insper Fighter

Jogo de luta 1 contra 1, local, para dois jogadores no mesmo teclado.
Projeto final de Design de Software — Insper, 2026/2.

## Integrantes

- João Pedro Servidoni — [Servidoni31](https://github.com/Servidoni31)
- João Damiani — [joaofldamiani](https://github.com/joaofldamiani)
- Guilherme Treves — [Treves05](https://github.com/Treves05)

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

## Como jogar

Na tela inicial, **Enter** começa. O jogador 1 escolhe o lutador, depois o
jogador 2, e depois a arena (setas para escolher, **Enter** para confirmar,
**Esc** para voltar). A luta começa com o "FIGHT!"; quando alguém é
nocauteado ou o tempo acaba, aparece a tela de vitória: **Enter** para
revanche, **C** para escolher de novo, **Esc** para voltar ao início. **Esc**
no meio da luta também volta ao início.

## Controles

| Ação | Jogador 1 | Jogador 2 |
|---|---|---|
| Andar | A / D | ← / → |
| Pular | W | ↑ |
| Defender (segurar) | S | ↓ |
| Dash (toque duplo) | A A / D D | ← ← / → → |
| Golpe 1 | E | Shift direito |
| Golpe 2 | Q | ; / : (a tecla ao lado do ponto) |

Defendendo, o lutador fica parado com um escudo neon na frente e leva só 40%
do dano dos golpes, sem cambalear. Não dá para andar nem golpear na guarda,
e no ar não dá para defender.

O dash (apertar duas vezes rápido para um lado) joga o lutador uns 70 px
para aquele lado, e durante ele nenhum golpe pega. Funciona até apanhando:
é o jeito de sair de um combo. Depois de um dash, só dá para dar outro
1,2 s depois.

## Personagens

Cada personagem tem dois golpes; o golpe 1 é sempre o mais rápido.

| Personagem | Golpe 1 | Golpe 2 | Estilo |
|---|---|---|---|
| Lutadora | soco (5) | chute (12) | maior alcance do jogo, mantém distância |
| Punk | soco (10) | soco forte (14) | forte de perto; o soco forte avança |
| Ninja | soco (6) | voadora (11) | a voadora cruza meia tela |
| Ilusionista | soco (7) | investida (11) | avança com o ombro |
| Agente Smith | soco (7) | chute (10) | veio de outro jogo — e dá para ver |
| Renegade | soco (8) | chute (13) | lento e pesado, alcance curto |

O punk não tem animação de chute no pacote de sprites; o segundo golpe dele
é a mesma animação do soco, mais lenta e com investida. O Agente Smith e o
Renegade são de pacotes de 8 bits e foram mantidos com o visual original, de
propósito.

**F1** mostra as caixas de colisão (corpo em azul, golpe em vermelho, e em
dourado no quadro em que o golpe acerta).

## Objetivo

Zerar a vida do adversário antes do tempo acabar. Se o tempo terminar, vence
quem tiver mais vida.

## Créditos dos assets

A arte, as trilhas e quase todos os sons são de uso livre e não exigem
atribuição; o crédito abaixo é por transparência. As exceções são a fonte
do cronômetro (a licença OFL pede que o crédito e o texto da licença
acompanhem o projeto), o som do soco forte (OGA-BY 3.0) e os sprites do
ninja e da Ilusionista (CC-BY-SA 3.0), que exigem atribuição.

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

- **Cenário 4 (Passarela)** — fundo do "Warped City", por Luis Zuno
  (ansimuz) — CC0. As três camadas do fundo foram juntadas numa imagem e a
  passarela neon de baixo foi desenhada por nós.
  https://opengameart.org/content/warped-city

- **Fonte do cronômetro** — "Press Start 2P", por CodeMan38 (The Press
  Start 2P Project Authors). Licença SIL Open Font License 1.1; o texto da
  licença está em `assets/fontes/OFL.txt`.
  https://fonts.google.com/specimen/Press+Start+2P

- **Sons de golpe** (`assets/som/efeitos/`, menos `golpe_forte2.ogg`) —
  "37 hits/punches", por Independent.nu — CC0
  https://opengameart.org/content/37-hitspunches

- **Som do soco forte** (`assets/som/efeitos/golpe_forte2.ogg`) — "Fleshy
  Fight Sounds", por will_leamon — OGA-BY 3.0.
  Additional Sound FX by Will Leamon.
  https://opengameart.org/content/fleshy-fight-sounds

- **Voz do locutor** (`assets/som/voz/`) — "Voiceover Pack: Fighter", por
  Kenney (www.kenney.nl) — CC0
  https://opengameart.org/content/voiceover-pack-fighter-40-taunts

Os sons de golpe foram cortados (silêncio do começo e do fim), passados
para mono e normalizados no mesmo volume.

O cenário 2 foi montado a partir da imagem de divulgação do pacote, que
vinha com dois lutadores desenhados nela; a região foi coberta com uma
faixa limpa da própria calçada.

- **Ninja e Ilusionista** — "Platformer or Fighter Sprites", enviado por
  Fracture; sprites originais de KZR e Jason Buividas (Team SD, para
  Shinobi Densetsu), sobre bases de Miguel Duarte e Clint Bellanger —
  CC-BY-SA 3.0 / GPL 3.0.
  https://opengameart.org/content/platformer-or-fighter-sprites
  Modificações: o ninja é o "Blue Ninja" do pacote; os dois foram
  recoloridos com a paleta do Streets of Fight e os quadros foram
  remontados no formato usado pelo jogo. Por causa da licença CC-BY-SA, as
  versões modificadas (`assets/sprites/ninja/` e
  `assets/sprites/ilusionista/`) são distribuídas sob a mesma licença.

- **Agente Smith** — "Agent Character", por Chasersgaming — CC0
  https://opengameart.org/content/agent-character

- **Renegade** — "Brawler Asset Character 'Renegade' SMS", por
  Chasersgaming — CC0
  https://opengameart.org/content/brawler-asset-character-renegade-sms

  Os dois foram mantidos com as cores originais; só os quadros foram
  remontados no formato usado pelo jogo.

Também foi avaliado durante a escolha, mas não utilizado:

- "Brawler Asset Character 'Vigilante' SMS", por Chasersgaming — CC0
  https://opengameart.org/content/brawler-asset-character-vigilante-sms

## Uso de inteligência artificial

### Proporção

A conta foi feita com `git blame` em todos os arquivos `.py`, contando as
linhas de código (sem linhas em branco e sem comentários). Uma linha conta como
"Claude" quando entrou num commit feito com o Claude, ou seja, um commit com a
linha `Co-Authored-By: Claude` na mensagem.

| Origem | Linhas | % |
|---|---|---|
| Claude (Anthropic) | 723 | 85% |
| Guilherme Treves | 70 | 8% |
| João Damiani (parte com sugestões do GitHub Copilot) | 43 | 5% |
| João Servidoni, sem IA | 56 | 8% |

Por arquivo:
- **Feitos com o Claude:** `lutador.py`, `personagens.py`, `sons.py`,
  `cenarios.py` e quase todo o `main.py`.
- **`inicio.py`:** as telas são do Treves. O Claude adaptou a seleção de
  personagem e de cenário e acrescentou as funções de miniatura e de imagem de
  vitória.
- **`interface.py`:** é do Damiani, com funções sugeridas pelo Copilot e
  pequenos ajustes do Claude.

Fonte: histórico da conversa com o Claude — https://claude.ai/share/62c00f9e-9348-432d-ac7f-0a57f1bb2778 .

### Como a IA foi usada

O grupo decidiu o jogo, as regras e o escopo, e dividiu as tarefas. O Treves
fez as telas e o Damiani fez a barra de vida, o cronômetro e a música. Usamos o
Claude (Anthropic) como programador, em conversa, pedindo uma coisa de cada vez:
a classe `Lutador` com os estados de animação, as caixas de acerto, o pulo, a
defesa, o dash, o laço principal com a troca de telas, o sistema de som e a
lista de personagens. O Claude também escreveu scripts fora do jogo para
recolorir os sprites no estilo cyberpunk e para tratar os áudios do locutor.
Nossa parte em cada pedido foi:
- testar cada versão jogando;
- apontar o que estava errado (golpes que não davam dano, alcance
  desequilibrado, teclas ruins, sprites feios);
- escolher personagens, arenas e sons;
- aprovar cada mudança antes de ir para o GitHub.

O Damiani usou o GitHub Copilot nas funções do `interface.py`.

Toda função ou classe feita ou alterada com IA tem um comentário logo acima:
`# feito com Claude (IA)`, `# feito pelo Treves, adaptado com Claude (IA)` ou
`# feito com CoPilot`.

### Anexo — principais pedidos feitos ao Claude

1. Ajudar Montar a estrutura do jogo: lutador com animações, golpes, dano e K.O.
2. Ajudar Equilibrar dano, alcance e velocidade dos golpes entre os lutadores.
3. Ajudar a Adicionar efeitos sonoros e as falas do locutor ("FIGHT", "K.O.", vencedor), deixando a voz mais intensa.
4. Ajudar Passar de 2 para 6 personagens, recolorindo os sprites no estilo cyberpunk.
5. Ajudar Criar o menu, a seleção de personagem e de arena, a tela de vitória e uma 4ª arena.
6. Ajudar Adicionar descrição curta para cada personagem.
7. Adicionar pulo, defesa (segurar para baixo) e dash (toque duplo) para escapar de combos.
8. Tirar as funções do `main.py` (pedido do Damiani) e remapear as teclas de golpe.
9. Corrigir as caixas de colisão que apareciam ao apertar TAB sem querer (atalho passou para F1).

O histórico completo está no link acima.

Todo o código entregue é compreendido pelos integrantes do grupo.
