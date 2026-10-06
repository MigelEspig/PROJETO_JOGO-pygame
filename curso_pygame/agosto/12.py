import pygame
import random

pygame.init()

tela = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Jogo do Alvo")

rodando = True
pontos = 0

alvo = pygame.Rect(300, 180, 60, 60)

cores = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0)
]
corAlvo = cores[random.randint(0,3)]


# -------------------------
# TEMPO
# -------------------------

ultimo_spawn = 0
intervalo = 1000


fonte = pygame.font.Font(None, 36)
fonte_titulo = pygame.font.Font(None, 64)
fonte_mensagem = pygame.font.Font(None, 42)

# -------------------------
# LOOP PRINCIPAL
# -------------------------

while rodando:

    # -------------------------
    # EVENTOS
    # -------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            # Só permite clicar enquanto não chegou a 30 pontos
            if pontos < 30:

                if alvo.collidepoint(evento.pos):
                    corAlvo = cores[random.randint(0,3)]

                    if corAlvo == (255, 0, 0):
                        pontos =- 2;
                    elif corAlvo == (0, 255, 0):
                        pontos =+ 2;
                    elif corAlvo == (0, 0, 255):
                        pontos =- 1;
                    else:
                        pontos =+ 1;

                    # Nova posição imediatamente após o clique
                    alvo.x = random.randint(
                        0,
                        800 - alvo.width
                    )

                    alvo.y = random.randint(
                        80,
                        450 - alvo.height
                    )
                    corAlvo = cores[random.randint(0,3)]


    # -------------------------
    # AUMENTO DA DIFICULDADE
    # -------------------------

    intervalo = max(
        300,
        1000 - (pontos // 5) * 100
    )

    # -------------------------
    # TEMPORIZADOR
    # -------------------------

    agora = pygame.time.get_ticks()

    # Só movimenta o alvo enquanto o jogo não terminou
    if pontos < 30:

        if agora - ultimo_spawn >= intervalo:

            alvo.x = random.randint(
                0,
                800 - alvo.width
            )

            alvo.y = random.randint(
                80,
                450 - alvo.height
            )

            corAlvo = cores[random.randint(0,3)]

            ultimo_spawn = agora

    # -------------------------
    # CENÁRIO
    # -------------------------

    tela.fill((30, 30, 30))

    # -------------------------
    # ALVO
    # -------------------------

    # Só mostra o alvo enquanto o jogo estiver acontecendo
    if pontos < 30:


        pygame.draw.rect(
            tela,
            corAlvo,
            alvo
        )


    # Placar
    texto_pontos = fonte.render(
        f"Pontos: {pontos}",
        True,
        (255, 255, 255)
    )

    tela.blit(
        texto_pontos,
        (15, 15)
    )

    # Título
    titulo = fonte_titulo.render(
        "CAÇA AO QUADRADO",
        True,
        (80, 170, 255)
    )

    rect_titulo = titulo.get_rect(
        center=(400, 55)
    )

    tela.blit(
        titulo,
        rect_titulo
    )

    # -------------------------
    # VELOCIDADE
    # -------------------------

    texto_intervalo = fonte.render(
        f"Velocidade: {intervalo} ms",
        True,
        (200, 200, 200)
    )

    tela.blit(
        texto_intervalo,
        (550, 15)
    )

    # -------------------------
    # INSTRUÇÃO
    # -------------------------

    if pontos < 30:

        instrucoes = fonte.render(
            "Clique no quadrado para ganhar pontos!",
            True,
            (200, 200, 200)
        )

        tela.blit(
            instrucoes,
            (15, 410)
        )

    # -------------------------
    # MENSAGEM DE 10 PONTOS
    # -------------------------

    if pontos >= 10 and pontos < 20:

        mensagem = fonte_mensagem.render(
            "PARABÉNS! VOCÊ ATINGIU 10 PONTOS!",
            True,
            (255, 220, 80)
        )

        rect_mensagem = mensagem.get_rect(
            center=(400, 120)
        )

        tela.blit(
            mensagem,
            rect_mensagem
        )

    # -------------------------
    # MENSAGEM DE 20 PONTOS
    # -------------------------

    elif pontos >= 20 and pontos < 30:

        mensagem = fonte_mensagem.render(
            "PARABÉNS! VOCÊ ATINGIU 20 PONTOS!",
            True,
            (255, 220, 80)
        )

        rect_mensagem = mensagem.get_rect(
            center=(400, 120)
        )

        tela.blit(
            mensagem,
            rect_mensagem
        )

    # -------------------------
    # MENSAGEM FINAL - 30 PONTOS
    # -------------------------

    elif pontos >= 30:

        mensagem = fonte_mensagem.render(
            "PARABÉNS! VOCÊ ATINGIU 30 PONTOS!",
            True,
            (255, 220, 80)
        )

        rect_mensagem = mensagem.get_rect(
            center=(400, 180)
        )

        tela.blit(
            mensagem,
            rect_mensagem
        )

        # Mensagem de encerramento
        final = fonte.render(
            "VOCÊ TERMINOU O JOGO!",
            True,
            (255, 255, 255)
        )

        rect_final = final.get_rect(
            center=(400, 230)
        )

        tela.blit(
            final,
            rect_final
        )

    pygame.display.flip()

pygame.quit()

# Atividade: Crie um sistema onde o quadrado muda de cor a cada vez que ele atualiza a posição.
# Caso ele seja clicado na cor vermelha, o jogador perde 2 pontos.
# Caso ele seja clicado na cor verde, o jogador ganha 2 pontos.
# Caso ele seja clicado na cor azul, o jogador ganha 1 ponto.
# Caso ele seja clicado na cor amarela, o jogador perde 1 ponto. 