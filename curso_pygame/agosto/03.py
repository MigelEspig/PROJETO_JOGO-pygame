import pygame
pygame.init()
tela = pygame.display.set_mode((700, 400))
cor_fundo = (25, 25, 35)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AZUL_ESCURO = (20, 35, 70)
ROXO = (64, 20, 125)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
ROSA = (255, 0, 255)

rodando = True

mostrar_circulo = False

while rodando:
    tela.fill(cor_fundo)

    for evento in pygame.event.get():
        print(evento)
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                rodando = False

            if evento.key == pygame.K_SPACE:
                cor_fundo = ROSA
            if evento.key == pygame.K_a:
                mostrar_circulo = True

    if mostrar_circulo:
        pygame.draw.circle(tela, VERDE, (350, 200), 20)


    pygame.display.flip()
pygame.quit()