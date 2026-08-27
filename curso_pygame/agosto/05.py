import pygame
pygame.init()
tela = pygame.display.set_mode((800, 450))
x_cubo = 250
y_cubo = 225
x_circulo = 550
y_circulo = 225
vel_cubo = 1
vel_circulo = 1.5
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        x_cubo -= vel_cubo
    if teclas[pygame.K_d]:
        x_cubo += vel_cubo
    if teclas[pygame.K_w]:
        y_cubo -= vel_cubo
    if teclas[pygame.K_s]:
        y_cubo += vel_cubo

    if teclas[pygame.K_LEFT]:
        x_circulo -= vel_circulo
    if teclas[pygame.K_RIGHT]:
        x_circulo += vel_circulo
    if teclas[pygame.K_UP]:
        y_circulo -= vel_circulo
    if teclas[pygame.K_DOWN]:
        y_circulo += vel_circulo
    
    tela.fill((25, 25, 40))
    pygame.draw.rect(tela, (60, 150, 255), (x_cubo, y_cubo, 40, 40))
    pygame.draw.circle(tela, (255, 0, 0), (x_circulo, y_circulo), 25)
    pygame.display.flip()
pygame.quit()