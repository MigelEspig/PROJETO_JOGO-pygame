# SPACESHIPS - AULA 20
# Versao cumulativa: inclui tudo o que foi trabalhado ate esta aula.
# Execute: python aula_20.py
import pygame

pygame.init()
# 1. CONFIGURACOES
LARGURA, ALTURA = 800, 500
FPS = 60
COR_FUNDO = (10, 15, 35)
COR_NAVE = (80, 220, 255)
COR_TEXTO = (255, 255, 255)
COR_TIRO = (255, 230, 100)
VERMELHO = (255, 0, 0)
VELOCIDADE_NAVE = 6

# 9. PREPARAR A JANELA E OBJETOS
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SPACESHIPS - aulas cumulativas")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)
fonte_grande = pygame.font.Font(None, 55)
nave = pygame.Rect(380, 425, 40, 40)
inimigo = pygame.Rect(375, 50, 50, 50)
tiros = []
# 10. LOOP PRINCIPAL
rodando = True
while rodando:
    relogio.tick(FPS)
    # EVENTOS: so aqui lemos KEYDOWN
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                tiro = pygame.Rect(nave.centerx - 3, nave.top, 6, 16)
                tiros.append(tiro)

    # ATUALIZAR O JOGO
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        nave.x -= VELOCIDADE_NAVE
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        nave.x += VELOCIDADE_NAVE
    nave.x = max(0, min(nave.x, LARGURA - nave.width))
    for tiro in tiros:
        tiro.y -= 9

    # DESENHAR: limpar a tela antes de redesenhar os objetos
    tela.fill(COR_FUNDO)
    pygame.draw.polygon(tela, COR_NAVE, [
        (nave.centerx, nave.top),
        (nave.left, nave.bottom),
        (nave.right, nave.bottom)
    ])
    pygame.draw.rect(tela, VERMELHO, inimigo)

    for tiro in tiros:
        pygame.draw.rect(tela, COR_TIRO, tiro)
    mensagem = ""
    if nave.left == 0:
        mensagem = "Limite esquerdo!"
    elif nave.right == LARGURA:
        mensagem = "Limite direito!"
    if mensagem:
        texto = fonte.render(mensagem, True, COR_TEXTO)
        tela.blit(texto, (20, 465))
    pygame.display.flip()
    if tiros:
        for tiro in tiros:
            if tiro.colliderect(inimigo):
                tiros.remove(tiro)
                rodando = False

pygame.quit()