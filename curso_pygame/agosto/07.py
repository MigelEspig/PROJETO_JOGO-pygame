import pygame
pygame.init()
tela = pygame.display.set_mode((800, 450))
x = 380
y = 205
velocidade = 2
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        x += velocidade
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        y += velocidade
    tela.fill((25, 25, 40))
    pygame.draw.rect(tela, (60, 150, 255), (x, y, 40, 40))
    pygame.display.flip()
pygame.quit()