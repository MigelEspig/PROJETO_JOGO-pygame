import pygame

# Iniciar o Pygame
pygame.init()

# -----------------------------
# CONSTANTES DO JOGO
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
# POSICAO DA NAVE
# -----------------------------

centro_x = LARGURA // 2

ponta_y = ALTURA - 100

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

    # Pintar o fundo
    tela.fill(COR_FUNDO)

    # Desenhar a nave
    pygame.draw.polygon(
        tela,
        COR_NAVE,
        [
            (centro_x, ponta_y),
            (centro_x - 20, ponta_y + 45),
            (centro_x + 20, ponta_y + 45)
        ]
    )

    pygame.display.flip()

pygame.quit()