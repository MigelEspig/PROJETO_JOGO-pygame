# SPACESHIPS - AULA 32
# Versao cumulativa: inclui tudo o que foi trabalhado ate esta aula.
# Execute: python aula_32.py
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
MARGEM, DESCIDA = 18, 29

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

# 5. MOVIMENTO LATERAL + DESCIDA NAS BORDAS

def mover_frota(inimigos, direcao, resto_x, velocidade, dt):
    if not inimigos:
        return direcao, resto_x
    resto_x += direcao * velocidade * dt
    dx = int(resto_x)
    resto_x -= dx
    if dx == 0:
        return direcao, resto_x
    esquerda = min(alien.left for alien in inimigos)
    direita = max(alien.right for alien in inimigos)
    virou = False
    if direcao > 0 and direita + dx >= LARGURA - MARGEM:
        dx = LARGURA - MARGEM - direita
        virou = True
    elif direcao < 0 and esquerda + dx <= MARGEM:
        dx = MARGEM - esquerda
        virou = True
    for alien in inimigos:
        alien.x += dx
        if virou:
            alien.y += DESCIDA
    if virou:
        direcao *= -1
        resto_x = 0.0
    return direcao, resto_x

# 6. DEVOLVER UMA PARTIDA LIMPA AO REINICIAR

def nova_partida():
    nave = pygame.Rect(380, 425, 40, 40)
    tiros = []
    inimigos = criar_frota()
    pontos, vidas, onda = 0, 3, 1
    direcao, resto_x = 1, 0.0
    return nave, tiros, inimigos, pontos, vidas, onda, direcao, resto_x

# 9. PREPARAR A JANELA E OBJETOS
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SPACESHIPS - aulas cumulativas")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)
fonte_grande = pygame.font.Font(None, 55)
nave, tiros, inimigos, pontos, vidas, onda, direcao, resto_x = nova_partida()
sprites = [gerar_sprite(DESENHO_1, ROXO), gerar_sprite(DESENHO_2, ROXO)]
estado = "menu"  # menu, jogando, pausado, registrar, fim
def escrever_centro(mensagem, y, cor=COR_TEXTO, destaque=False):
    f = fonte_grande if destaque else fonte
    imagem = f.render(mensagem, True, cor)
    tela.blit(imagem, imagem.get_rect(center=(LARGURA // 2, y)))
# 10. LOOP PRINCIPAL
rodando = True
while rodando:
    dt = min(relogio.tick(FPS) / 1000, 0.05)
    agora = pygame.time.get_ticks()
    # EVENTOS: so aqui lemos KEYDOWN
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
            elif estado == "menu" and evento.key == pygame.K_RETURN:
                estado = "jogando"
            elif estado == "fim" and evento.key == pygame.K_r:
                nave, tiros, inimigos, pontos, vidas, onda, direcao, resto_x = nova_partida()
                estado = "jogando"
            elif evento.key == pygame.K_p:
                if estado == "jogando":
                    estado = "pausado"
                elif estado == "pausado":
                    estado = "jogando"
            elif estado == "jogando" and evento.key == pygame.K_SPACE:
                tiro = pygame.Rect(nave.centerx - 3, nave.top, 6, 16)
                tiros.append(tiro)

    # ATUALIZAR O JOGO
    if estado == "jogando":
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
        velocidade = min(240, 100 + 20 * (onda - 1))
        direcao, resto_x = mover_frota(
            inimigos, direcao, resto_x, velocidade, dt
        )
        # Percorrer copias impede pular objetos removidos.
        for tiro in tiros[:]:
            for alien in inimigos[:]:
                if tiro.colliderect(alien):
                    inimigos.remove(alien)
                    tiros.remove(tiro)
                    pontos += 10
                    break
        # Cada onda vencida concede bonus e uma nova formacao.
        if not inimigos:
            onda += 1
            pontos += 50
            inimigos = criar_frota()
            tiros.clear()
            direcao, resto_x = 1, 0.0
        elif any(alien.bottom >= nave.top for alien in inimigos):
            vidas = max(0, vidas - 1)
            tiros.clear()
            inimigos = criar_frota()
            direcao, resto_x = 1, 0.0
            if vidas == 0:
                estado = "fim"

    # DESENHAR: limpar a tela antes de redesenhar os objetos
    tela.fill(COR_FUNDO)
    if estado == "menu":
        escrever_centro("SPACESHIPS", 85, COR_NAVE, destaque=True)
        escrever_centro("ENTER - iniciar partida", 165, COR_TIRO)
        escrever_centro("A/D ou setas: mover | ESPACO: tiro", 208)
        escrever_centro("P: pausa | R: reiniciar no fim", 242)
        escrever_centro("ESC: sair", 276)
    else:
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
        placar = f"Pontos: {pontos}   Vidas: {vidas}   Onda: {onda}"
        texto_placar = fonte.render(placar, True, COR_TEXTO)
        tela.blit(texto_placar, (17, 15))
        if estado == "pausado":
            escrever_centro("PAUSADO - P para voltar", 255, COR_TIRO)
        elif estado == "fim":
            escrever_centro("FIM DE JOGO", 240, COR_TIRO, destaque=True)
            escrever_centro("Pressione R para reiniciar", 290)
    pygame.display.flip()
pygame.quit()