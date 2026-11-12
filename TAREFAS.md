# Divisão de tarefas

Entrega: **23/11, 12h00**. Feira de Jogos logo depois, e prova individual
do projeto no dia 25.

## Regras que valem pra todo mundo

**Cada um commita da própria conta.** A rubrica dá conceito D para o grupo
inteiro se os commits forem de um usuário só, por melhor que o jogo fique.
Não vale um subir o código dos outros.

Antes de começar a mexer: `git pull`
Ao terminar um pedaço: `git add .` → `git commit -m "..."` → `git push`

**Cada um no seu arquivo.** Se os três editarem `main.py`, vai dar conflito
toda hora. Cada tarefa tem o seu próprio `.py`, e o `main.py` só chama.
Isso também vale ponto: a rubrica pede responsabilidades separadas em
arquivos diferentes.

**Rascunhos vão para `design/`.** Foto de papel serve. É evidência de
trabalho em equipe e vale 25% da nota.

## Como rodar

```
pip install pygame-ce
python main.py
```

`pygame-ce` e não `pygame`: em Python 3.13 e 3.14 o pygame comum não
instala. O `import pygame` no código continua igual.

## Medidas que vocês vão precisar

Está tudo em `assets/LEIA-ME.md`. O essencial:

- a tela do jogo é **688 × 272**, ampliada 2× na janela (1376 × 544)
- todo quadro de personagem tem **96 × 63** pixels
- chão do cenário 1: **y = 256** · chão do cenário 2: **y = 230**

---

## Treves — telas e menu

Arquivo: `telas.py`

1. **Tela de início** — título do jogo, "aperte ENTER para começar"
2. **Tela de seleção** — escolher o personagem (2 opções) e o cenário
   (2 opções), com as setas e ENTER
3. **Tela de vitória** — quem venceu, e opção de revanche

Não precisa saber nada da lógica de luta. Cada tela é: desenhar imagens e
texto na superfície `tela`, e devolver o que o jogador escolheu.

Para texto: `pygame.font.Font(None, tamanho)` e depois `.render(...)`.

Comece pela tela de início, que é a mais simples. As três telas juntas
já atendem o "múltiplas telas" que a rubrica pede.

## Damiani — som, interface e acabamento

Arquivo: `interface.py`

1. **Trilha de fundo em loop** — o arquivo é `assets/som/trilha.ogg`.
   `pygame.mixer.music.load(...)` e `play(-1)` para repetir sem parar
2. **Efeitos sonoros** — impacto do soco, pulo. Procurar em
   opengameart.org filtrando por licença CC0, e anotar a fonte no README
3. **Barra de vida** dos dois jogadores, no topo da tela
4. **Cronômetro** de 60 segundos do round

A barra de vida é um retângulo desenhado com `pygame.draw.rect`, cuja
largura encolhe conforme a vida cai. Comece por ela: é a mais visível e
não depende de mais nada.

## João — lutador e combate

Arquivo: `lutador.py`

1. Recortar um quadro da folha de sprite e desenhar na tela
2. Trocar de quadro ao longo do tempo (animação)
3. Mover com o teclado
4. Máquina de estados: parado, andando, socando, chutando, tomando dano
5. Colisão entre o ataque de um e o corpo do outro
6. Dano e fim de round

É a parte mais pesada e a que o resto depende, por isso vem primeiro.

---

## Sugestão de marcos

| Até | O que já deveria rodar |
|---|---|
| 15/11 | lutador aparece e anda · tela de início pronta · trilha tocando |
| 18/11 | dois lutadores · soco acerta e tira vida · barra de vida |
| 20/11 | seleção de personagem e cenário · tela de vitória · efeitos sonoros |
| 22/11 | gravar o vídeo · fechar o README · testar numa máquina limpa |

Deixar pra testar no dia 23 de manhã é como se perde a entrega.
