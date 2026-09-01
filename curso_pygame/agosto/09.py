import pygame
pygame.init()
tela = pygame.display.set_mode((800, 450))
relogio = pygame.time.Clock()
FPS = 60
velocidade = 240
jogador = pygame.Rect(100, 180, 45, 45)
obstaculo = pygame.Rect(420, 130, 100, 170)
area_tela = tela.get_rect()
rodando = True

while rodando:

    dt = relogio.tick(FPS) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_d]:
        jogador.x += velocidade * dt

    if teclas[pygame.K_a]:
        jogador.x -= velocidade * dt

    if teclas[pygame.K_w]:
        jogador.y -= velocidade * dt

    if teclas[pygame.K_s]:
        jogador.y += velocidade * dt

    # Impede o jogador de sair da tela
    jogador.clamp_ip(area_tela)

    # Verifica se o jogador está encostando no obstáculo
    if jogador.colliderect(obstaculo):
        cor_jogador = (255, 90, 90)
    else:
        cor_jogador = (70, 150, 255)

    # Desenha a tela
    tela.fill((30, 30, 30))

    pygame.draw.rect(tela, cor_jogador, jogador)

    pygame.draw.rect(tela, (110, 110, 125), obstaculo)

    pygame.display.flip()

pygame.quit()