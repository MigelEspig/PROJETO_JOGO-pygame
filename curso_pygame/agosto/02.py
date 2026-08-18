import pygame
pygame.init()
LARGURA = 800
ALTURA = 450
AZUL_ESCURO = (20, 35, 70)
BRANCO = (255, 255, 255)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Coordenadas e cores")
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    tela.fill(AZUL_ESCURO)
    pygame.draw.circle(tela, BRANCO, (0, 0), 8)
    pygame.draw.circle(tela, BRANCO, (LARGURA // 2, ALTURA // 2), 8)
    pygame.display.flip()
pygame.quit()