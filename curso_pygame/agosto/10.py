import pygame
import random

pygame.init()

tela = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Jogo do Alvo")

rodando = True
boneco_x = 60
boneco_y = 60

pontos = 0

alvo = pygame.Rect(300, 180, 60, 60)

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if alvo.collidepoint(evento.pos):
                pontos += 1
                alvo.width = alvo.width - 10
                alvo.height = alvo.height - 10


                alvo.x = random.randint(0, 740)
                alvo.y = random.randint(0, 390)
            else:
                alvo.width = alvo.width + 10
                alvo.height = alvo.height + 10
                
                alvo.x = random.randint(0, 740)
                alvo.y = random.randint(0, 390)

    tela.fill((30, 30, 30))

    pygame.draw.rect(tela, (255, 110, 90), alvo)

    pygame.display.flip()

pygame.quit()