import pygame
#nota
# Iniciar o Pygame
pygame.init()

# -----------------------------
# CONSTANTES
# -----------------------------

LARGURA = 800
ALTURA = 500

FPS = 60

COR_FUNDO = (10, 15, 35)
COR_NAVE = (80, 220, 255)
COR_TEXTO = (255, 255, 255)

VELOCIDADE_NAVE = 6

# -----------------------------
# CRIAR A JANELA
# -----------------------------

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption("Spaceships")

relogio = pygame.time.Clock()

# Fonte das mensagens
fonte = pygame.font.Font(None, 30)

# -----------------------------
# CRIAR A NAVE
# -----------------------------

nave = pygame.Rect(
    380,
    425,
    40,
    40
)

# -----------------------------
# LOOP PRINCIPAL
# -----------------------------

rodando = True

while rodando:

    relogio.tick(FPS)

    # Verificar eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # -------------------------
    # MOVIMENTO
    # -------------------------

    teclas = pygame.key.get_pressed()

    # Esquerda
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:

        nave.x -= VELOCIDADE_NAVE

    # Direita
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:

        nave.x += VELOCIDADE_NAVE

    # -------------------------
    # LIMITES DA TELA
    # -------------------------

    nave.x = max(
        0,
        min(nave.x, LARGURA - nave.width)
    )

    # -------------------------
    # VERIFICAR AS BORDAS
    # -------------------------

    mensagem = ""

    if nave.left == 0:

        mensagem = "Limite esquerdo!"

    elif nave.right == LARGURA:

        mensagem = "Limite direito!"

    # -------------------------
    # DESENHAR
    # -------------------------

    tela.fill(COR_FUNDO)

    # Desenhar a nave
    pygame.draw.polygon(
        tela,
        COR_NAVE,
        [
            (nave.centerx, nave.top),
            (nave.left, nave.bottom),
            (nave.right, nave.bottom)
        ]
    )

    # Mostrar mensagem na tela
    if mensagem != "":

        texto = fonte.render(
            mensagem,
            True,
            COR_TEXTO
        )

        tela.blit(texto, (20, 20))

    # Atualizar a janela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
