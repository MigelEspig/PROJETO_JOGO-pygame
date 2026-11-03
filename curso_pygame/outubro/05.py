import pygame

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

VELOCIDADE_NAVE = 6

# -----------------------------
# CRIAR A JANELA
# -----------------------------

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption("Spaceships")

relogio = pygame.time.Clock()

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
    # MOVIMENTO DA NAVE
    # -------------------------

    teclas = pygame.key.get_pressed()

    # Movimento para a esquerda
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:

        nave.x -= VELOCIDADE_NAVE

    # Movimento para a direita
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:

        nave.x += VELOCIDADE_NAVE

    # -------------------------
    # DESENHAR
    # -------------------------

    tela.fill(COR_FUNDO)

    # Desenhar a nave triangular
    pygame.draw.polygon(
        tela,
        COR_NAVE,
        [
            (nave.centerx, nave.top),
            (nave.left, nave.bottom),
            (nave.right, nave.bottom)
        ]
    )

    pygame.display.flip()

pygame.quit()