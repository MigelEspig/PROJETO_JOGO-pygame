import pygame
pygame.init()
tela = pygame.display.set_mode((700, 400))
cor_fundo = (25, 25, 35)
rodando = True
mostrar_sol = True
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
                cor_fundo = (60, 30, 90)
            if evento.key == pygame.K_s:
                mostrar_sol = not mostrar_sol
    if mostrar_sol:
        pygame.draw.circle(tela, (255, 255, 0), (600, 100), 40)
    
    # Dentro do loop, depois de tela.fill(...)
    pygame.draw.rect(tela, (60, 180, 90), (0, 330, 800, 120))
    pygame.draw.rect(tela, (70, 130, 255), (360, 260, 80, 80))
    pygame.draw.circle(tela, (255, 230, 200), (400, 245), 28)
    pygame.draw.line(tela, (20, 20, 20), (375, 245), (390, 245), 4)
    pygame.draw.line(tela, (20, 20, 20), (410, 245), (425, 245), 4)
    pygame.display.flip()
pygame.quit()