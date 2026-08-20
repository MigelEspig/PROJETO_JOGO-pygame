import pygame
pygame.init()
LARGURA = 1000
ALTURA = 650
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AZUL_ESCURO = (20, 35, 70)
ROXO = (64, 20, 125)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Coordenadas e cores")
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    tela.fill(ROXO)
    pygame.draw.circle(tela, VERMELHO, (0, 0), 8)
    pygame.draw.circle(tela, VERMELHO, (LARGURA // 2, ALTURA // 2), 14)

    # LOSANGO DE PONTOS
    pygame.draw.circle(tela, AMARELO, (800, 150), 5)
    pygame.draw.circle(tela, AMARELO, (775, 175), 5)
    pygame.draw.circle(tela, AMARELO, (750, 200), 5)
    pygame.draw.circle(tela, AMARELO, (775, 225), 5)
    pygame.draw.circle(tela, AMARELO, (800, 250), 5)
    pygame.draw.circle(tela, AMARELO, (825, 175), 5)
    pygame.draw.circle(tela, AMARELO, (850, 200), 5)
    pygame.draw.circle(tela, AMARELO, (825, 225), 5)

    # QUADRADO DE PONTOS

    pygame.draw.circle(tela, AZUL, (200, 300), 5)
    pygame.draw.circle(tela, AZUL, (250, 300), 5)
    pygame.draw.circle(tela, AZUL, (300, 300), 5)
    pygame.draw.circle(tela, AZUL, (300, 350), 5)
    pygame.draw.circle(tela, AZUL, (200, 400), 5)
    pygame.draw.circle(tela, AZUL, (250, 400), 5)
    pygame.draw.circle(tela, AZUL, (300, 400), 5)
    pygame.draw.circle(tela, AZUL, (200, 350), 5)

    # CIRCULO DE PONTOS

    pygame.draw.circle(tela, VERDE, (500, 498), 5)

    pygame.draw.circle(tela, VERDE, (475, 490), 5)
    pygame.draw.circle(tela, VERDE, (525, 490), 5)

    pygame.draw.circle(tela, VERDE, (455, 470), 5)
    pygame.draw.circle(tela, VERDE, (545, 470), 5)

    pygame.draw.circle(tela, VERDE, (553, 445), 5)
    pygame.draw.circle(tela, VERDE, (447, 445), 5)

# [divisao inutil]

    pygame.draw.circle(tela, VERDE, (500, 392), 5)
    
    pygame.draw.circle(tela, VERDE, (475, 400), 5)
    pygame.draw.circle(tela, VERDE, (525, 400), 5)

    pygame.draw.circle(tela, VERDE, (455, 420), 5)
    pygame.draw.circle(tela, VERDE, (545, 420), 5)

    pygame.display.flip()



pygame.quit()