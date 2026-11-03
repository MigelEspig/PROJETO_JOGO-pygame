import pygame
import random

# Iniciar o Pygame
pygame.init()

# Configuracoes
LARGURA = 800
ALTURA = 500
FPS = 60

# Criar a janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Aula 12 - Revisao")

# Criar o relogio
relogio = pygame.time.Clock()

# Criar o alvo
TAMANHO = 40
alvo = pygame.Rect(100, 200, TAMANHO, TAMANHO)

# Configurar o temporizador
INTERVALO = 1000
ultimo_sorteio = pygame.time.get_ticks()

# Controle do jogo
rodando = True

while rodando:

    relogio.tick(FPS)

    # Verificar eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # Mudar a posicao ao apertar ESPACO
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_SPACE:

                alvo.x = random.randint(
                    0, LARGURA - TAMANHO
                )

                ultimo_sorteio = pygame.time.get_ticks()

    # Verificar quanto tempo passou
    agora = pygame.time.get_ticks()

    if agora - ultimo_sorteio >= INTERVALO:

        # Sortear uma nova posicao
        alvo.x = random.randint(
            0, LARGURA - TAMANHO
        )

        ultimo_sorteio = agora

    # Pintar a janela
    tela.fill((10, 15, 35))

    # Desenhar o quadrado
    pygame.draw.rect(
        tela,
        (255, 100, 100),
        alvo
    )

    # Atualizar a imagem
    pygame.display.flip()

# Encerrar o programa
pygame.quit()