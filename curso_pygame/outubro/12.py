# SPACESHIPS - AULA 24
# Versao cumulativa: inclui tudo o que foi trabalhado ate esta aula.
# Execute: python aula_24.py
import pygame

pygame.init()
# 1. CONFIGURACOES
LARGURA, ALTURA = 800, 500
FPS = 60
COR_FUNDO = (10, 15, 35)
COR_NAVE = (80, 220, 255)
COR_TEXTO = (255, 255, 255)
COR_TIRO = (255, 230, 100)
VELOCIDADE_NAVE = 6
ROXO = (188, 100, 247)
VERDE = (105, 250, 206)
TAMANHO_PIXEL = 3
LARGURA_ALIEN, ALTURA_ALIEN = 39, 33
COLUNAS, LINHAS = 8, 3
ESPACO_X, ESPACO_Y = 23, 17

# 2. MATRIZ DE PIXEL ART (0=vazio, 1=corpo, 2=olhos)

DESENHO_1 = [
    "0001100011000",
    "0011111111100",
    "0111111111110",
    "1122111112211",
    "1111111111111",
    "1111111111111",
    "0011111111100",
    "0011011101100",
    "0110000000110",
    "1100000000011",
    "1000000000001",
]
DESENHO_2 = [
    "0001100011000",
    "0011111111100",
    "0111111111110",
    "1122111112211",
    "1111111111111",
    "1111111111111",
    "0011111111100",
    "0011011101100",
    "0001100011000",
    "0011000001100",
    "0110000000110",
]

DESENHO_3 = [
    "0000001111100000",
    "0000011111110000",
    "0000112111211000",
    "0001111111111100",
    "0001211111121100",
    "0011111111111110",
    "0111111111111110",
    "1111111111111111",
    "1111111111111111",
    "0111111111111110",
    "0011000000011000",
    "0022000000022000"
]
DESENHO_4 = [
    "0000001111100000",
    "0000011111110000",
    "0000112111211000",
    "0001111111111100",
    "0001211111121100",
    "0011111111111110",
    "0111111111111110",
    "1111111111111111",
    "1111111111111111",
    "0111111111111110",
    "0110000000001100",
    "2200000000000220"
]

# 3. CONVERTER A MATRIZ EM UMA IMAGEM TRANSPARENTE

def gerar_sprite(desenho, cor):
    imagem = pygame.Surface((LARGURA_ALIEN, ALTURA_ALIEN), pygame.SRCALPHA)
    for linha, texto in enumerate(desenho):
        for coluna, simbolo in enumerate(texto):
            if simbolo != "0":
                cor_pixel = VERDE if simbolo == "2" else cor
                pygame.draw.rect(imagem, cor_pixel, (
                    coluna * TAMANHO_PIXEL, linha * TAMANHO_PIXEL,
                    TAMANHO_PIXEL, TAMANHO_PIXEL
                ))
    return imagem

def Gerar_maicon(desenho, cor):
    imagem_maicon = pygame.Surface((LARGURA_ALIEN, ALTURA_ALIEN), pygame.SRCALPHA)
    for linha, texto in enumerate(desenho):
        for coluna, simbolo in enumerate(texto):
            if simbolo != "0":
                cor_pixel = VERDE if simbolo == "2" else cor
                pygame.draw.rect(imagem_maicon, cor_pixel, (
                    coluna * TAMANHO_PIXEL, linha * TAMANHO_PIXEL,
                    TAMANHO_PIXEL, TAMANHO_PIXEL
                ))
    return imagem_maicon


# 4. MONTAR A FORMACAO

def criar_frota():
    largura_frota = COLUNAS * LARGURA_ALIEN + (COLUNAS - 1) * ESPACO_X
    x_inicial = (LARGURA - largura_frota) // 2
    inimigos = []
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = x_inicial + coluna * (LARGURA_ALIEN + ESPACO_X)
            y = 73 + linha * (ALTURA_ALIEN + ESPACO_Y)
            inimigos.append(pygame.Rect(x, y, LARGURA_ALIEN, ALTURA_ALIEN))
    return inimigos

# 9. PREPARAR A JANELA E OBJETOS
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SPACESHIPS - aulas cumulativas")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)
fonte_grande = pygame.font.Font(None, 55)
nave = pygame.Rect(380, 425, 40, 40)
tiros = []
inimigos = criar_frota()
sprites = [gerar_sprite(DESENHO_1, ROXO), gerar_sprite(DESENHO_2, ROXO)]
# 10. LOOP PRINCIPAL
rodando = True
while rodando:
    relogio.tick(FPS)
    agora = pygame.time.get_ticks()
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
    for tiro in tiros[:]:
        tiro.y -= 9
        if tiro.bottom < 0:
            tiros.remove(tiro)

    # DESENHAR: limpar a tela antes de redesenhar os objetos
    tela.fill(COR_FUNDO)
    pygame.draw.polygon(tela, COR_NAVE, [
        (nave.centerx, nave.top),
        (nave.left, nave.bottom),
        (nave.right, nave.bottom)
    ])
    animacao = (agora // 300) % 2
    for alien in inimigos:
        tela.blit(sprites[animacao], alien.topleft)
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
pygame.quit()