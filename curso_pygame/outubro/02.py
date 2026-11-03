import pygame

# Iniciar o Pygame
pygame.init()

# Criar a janela
tela = pygame.display.set_mode((800, 500))

# Titulo da janela
pygame.display.set_caption("Spaceships")

# Criar o relogio
relogio = pygame.time.Clock()

# Controle do jogo
rodando = True

# Loop principal
while rodando:

    # Limitar a 60 quadros por segundo
    relogio.tick(60)

    # Verificar eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # Pintar o fundo
    tela.fill((10, 15, 35))

    # Atualizar a janela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()