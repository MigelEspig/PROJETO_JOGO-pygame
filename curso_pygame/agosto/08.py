import pygame
pygame.init()
tela = pygame.display.set_mode((800, 450))
relogio = pygame.time.Clock()
FPS = 60
x = 100.0
velocidade = 240  # pixels por segundo
rodando = True

while rodando:

    dt = relogio.tick(FPS) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_d]:
        x += velocidade * dt

    if teclas[pygame.K_a]:
        x -= velocidade * dt

    tela.fill((30, 30, 30))

    pygame.draw.rect(tela, (80, 160, 255), (round(x), 200, 40, 40))

    pygame.display.flip()

pygame.quit()