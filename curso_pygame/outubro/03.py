import pygame

# Iniciar o Pygame
pygame.init()

# Criar a janela
tela = pygame.display.set_mode((800, 500))

pygame.display.set_caption("Spaceships - Nave")

# Criar o relogio
relogio = pygame.time.Clock()

# Definir a cor da nave
AZUL = (80, 220, 255)

# Controle do jogo
rodando = True

while rodando:

    relogio.tick(60)

    # Verificar eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # Pintar o fundo
    tela.fill((10, 15, 35))

    # Desenhar a nave
    pygame.draw.polygon(
        tela,
        AZUL,
        [
            (400, 400),
            (380, 445),
            (420, 445)
        ]
    )

    # Atualizar a tela
    pygame.display.flip()

pygame.quit()