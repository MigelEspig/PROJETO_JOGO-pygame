import pygame
import random
import math
import sys

# --- INICIALIZAÇÃO ---
pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MORFLEX: EM BUSCA DO MUNDO INTELÍGIVEL 💊🕶️")
clock = pygame.time.Clock()

# --- CORES ZUADAS ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 70)
RED = (255, 30, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
SKIN = (255, 205, 148)

# --- FONTE ---
font_small = pygame.font.SysFont("Comic Sans MS", 18, bold=True)
font_medium = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
font_large = pygame.font.SysFont("Comic Sans MS", 50, bold=True)

# --- SISTEMA DE TREMEDEIRA (SCREEN SHAKE) ---
shake_intensity = 0

def add_shake(amount):
    global shake_intensity
    shake_intensity = max(shake_intensity, amount)

# --- CLASSE: EFEITO CHUVA MATRIX (ZUADA) ---
MATRIX_WORDS = ["MORFLEX", "CLT", "BOLETO", "CAVERNA", "SOCRATES", "IDEIAS", "NEO", "CAFE", "XEREC", "REALI", "0101", "VERMELHA", "6X1"]
class MatrixRain:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.randint(4, 12)
        self.text = random.choice(MATRIX_WORDS)
        self.color = (0, random.randint(150, 255), 70)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, 0)
            self.x = random.randint(0, WIDTH)
            self.text = random.choice(MATRIX_WORDS)

    def draw(self, surface):
        txt = font_small.render(self.text, True, self.color)
        surface.blit(txt, (self.x, self.y))

# --- CLASSE: TEXTO FLUTUANTE (POP-UP MEME) ---
class FloatingText:
    def __init__(self, text, x, y, color=YELLOW):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life = 40  # frames
        self.vy = -2

    def update(self):
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            txt = font_medium.render(self.text, True, self.color)
            surface.blit(txt, (self.x, self.y))

# --- CLASSE: PLAYER (MORFLEX) ---
class Morflex:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 28
        self.speed = 7
        self.angle = 0
        self.despertar = 0  # Progresso até vencer
        self.alienacao = 0  # Dano acumulado (game over)

    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # Normalizar movimento diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx * self.speed
        self.y += dy * self.speed

        # Rebatimento nas bordas
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

        # Efeito de balanço (wobble)
        self.angle = math.sin(pygame.time.get_ticks() * 0.01) * 15

    def draw(self, surface):
        # Desenha Sobretudo (Corpo)
        pygame.draw.rect(surface, (20, 20, 20), (self.x - 22, self.y + 10, 44, 35), border_radius=8)
        
        # Desenha Cabeça
        pygame.draw.circle(surface, SKIN, (int(self.x), int(self.y)), self.radius)
        
        # Óculos escuros do Morflex (Marca Registrada 😎)
        pygame.draw.rect(surface, BLACK, (self.x - 22, self.y - 10, 18, 12), border_radius=3)
        pygame.draw.rect(surface, BLACK, (self.x + 4, self.y - 10, 18, 12), border_radius=3)
        pygame.draw.line(surface, BLACK, (self.x - 5, self.y - 4), (self.x + 5, self.y - 4), 3)
        # Brilho dos Óculos
        pygame.draw.line(surface, WHITE, (self.x - 20, self.y - 8), (self.x - 14, self.y - 3), 2)
        pygame.draw.line(surface, WHITE, (self.x + 6, self.y - 8), (self.x + 12, self.y - 3), 2)

        # Boca séria / desconfiada
        pygame.draw.line(surface, BLACK, (self.x - 8, self.y + 14), (self.x + 8, self.y + 14), 3)

        # Nome em cima
        txt = font_small.render("MORFLEX", True, GREEN)
        surface.blit(txt, (self.x - txt.get_width()//2, self.y - 48))

# --- CLASSE: PÍLULA VERMELHA (OBJETIVO) ---
class RedPill:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.pulse = 0

    def draw(self, surface):
        self.pulse += 0.1
        scale = math.sin(self.pulse) * 4
        # Desenha cápsula vermelha brilhante
        r = int(14 + scale)
        pygame.draw.ellipse(surface, RED, (self.x - r, self.y - 10, r*2, 20))
        pygame.draw.ellipse(surface, WHITE, (self.x - r//2, self.y - 6, r, 6))
        
        txt = font_small.render("VERDADE", True, RED)
        surface.blit(txt, (self.x - txt.get_width()//2, self.y - 30))

# --- CLASSE: PÍLULA AZUL (INIMIGO DA MATRIX) ---
BLUE_QUOTES = ["FICA NA MATRIX!", "DORME MAIS 5 MIN", "TRABALHE 6X1", "PAGUE O BOLETO", "SÓ MAIS UM REELS", "ILUSÃO É BOM"]

class BluePill:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.vx = random.choice([-4, -3, 3, 4])
        self.vy = random.choice([-4, -3, 3, 4])
        self.quote = random.choice(BLUE_QUOTES)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Quicar nas paredes
        if self.x < 20 or self.x > WIDTH - 20:
            self.vx *= -1
            self.quote = random.choice(BLUE_QUOTES)
        if self.y < 20 or self.y > HEIGHT - 20:
            self.vy *= -1
            self.quote = random.choice(BLUE_QUOTES)

    def draw(self, surface):
        # Cápsula Azul Maligna
        pygame.draw.ellipse(surface, BLUE, (self.x - 16, self.y - 10, 32, 20))
        # Olhos malignos da pílula azul
        pygame.draw.circle(surface, RED, (int(self.x - 5), int(self.y - 2)), 3)
        pygame.draw.circle(surface, RED, (int(self.x + 5), int(self.y - 2)), 3)

        txt = font_small.render(self.quote, True, BLUE)
        surface.blit(txt, (self.x - txt.get_width()//2, self.y + 12))

# --- SETUP DO JOGO ---
rains = [MatrixRain() for _ in range(40)]
player = Morflex()
red_pill = RedPill()
blue_pills = [BluePill() for _ in range(4)]
floating_texts = []

score = 0
game_state = "PLAYING" # "PLAYING", "GAMEOVER", "WIN"

# --- LOOP PRINCIPAL ---
running = True
while running:
    clock.tick(60)

    # --- PROCESSAR EVENTOS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state != "PLAYING":
                # Resetar Jogo
                player = Morflex()
                red_pill = RedPill()
                blue_pills = [BluePill() for _ in range(4)]
                floating_texts.clear()
                score = 0
                game_state = "PLAYING"

    if game_state == "PLAYING":
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Atualizar Pílulas Azuis
        for bp in blue_pills:
            bp.update()

        # Atualizar Chuva Matrix
        for r in rains:
            r.update()

        # Atualizar Textos Flutuantes
        for ft in floating_texts[:]:
            ft.update()
            if ft.life <= 0:
                floating_texts.remove(ft)

        # --- COLISÃO: MORFLEX vs PÍLULA VERMELHA ---
        dist_red = math.hypot(player.x - red_pill.x, player.y - red_pill.y)
        if dist_red < player.radius + 15:
            score += 1
            player.despertar += 12
            add_shake(12)
            red_pill.respawn()

            # Mensagens zoadas ao pegar a pílula
            msgs = ["MUNDO INTELIGÍVEL!", "SAIU DA CAVERNA!", "SÓCRATES APROVA!", "MATRIX QUEBRADA!", "NEO QUEM?"]
            floating_texts.append(FloatingText(random.choice(msgs), player.x - 50, player.y - 30, GREEN))

            # Adicionar mais pílulas azuis para dificultar a zueira
            if score % 3 == 0:
                blue_pills.append(BluePill())
                floating_texts.append(FloatingText("MAIS ALIENADORES APARECERAM!", WIDTH//2 - 150, 100, RED))

        # --- COLISÃO: MORFLEX vs PÍLULA AZUL ---
        for bp in blue_pills:
            dist_blue = math.hypot(player.x - bp.x, player.y - bp.y)
            if dist_blue < player.radius + 15:
                player.alienacao += 1.5
                add_shake(5)
                if random.random() < 0.1:
                    msgs_bad = ["DORMA!", "CLT 6X1!", "CLIQUE NO AD!", "ASSISTA BBB!"]
                    floating_texts.append(FloatingText(random.choice(msgs_bad), player.x - 30, player.y - 30, RED))

        # Checar Condições de Fim de Jogo
        if player.alienacao >= 100:
            game_state = "GAMEOVER"
        elif player.despertar >= 100:
            game_state = "WIN"

    # --- DESENHAR TELA ---
    # Aplica o Efeito de Screen Shake offset
    render_surf = pygame.Surface((WIDTH, HEIGHT))
    render_surf.fill(BLACK)

    # Desenhar chuva de fundo
    for r in rains:
        r.draw(render_surf)

    if game_state == "PLAYING":
        red_pill.draw(render_surf)
        for bp in blue_pills:
            bp.draw(render_surf)
        player.draw(render_surf)

        for ft in floating_texts:
            ft.draw(render_surf)

        # --- INTERFACE ZUADA (HUD) ---
        # Barra de Despertar (Vermelha/Verde)
        pygame.draw.rect(render_surf, (50, 50, 50), (20, 20, 250, 25), border_radius=5)
        pygame.draw.rect(render_surf, GREEN, (20, 20, int(2.5 * player.despertar), 25), border_radius=5)
        txt_desp = font_small.render(f"DESPERTAR (Mundo Real): {int(player.despertar)}%", True, WHITE)
        render_surf.blit(txt_desp, (25, 22))

        # Barra de Alienação (Azul)
        pygame.draw.rect(render_surf, (50, 50, 50), (20, 55, 250, 25), border_radius=5)
        pygame.draw.rect(render_surf, BLUE, (20, 55, int(2.5 * player.alienacao), 25), border_radius=5)
        txt_ali = font_small.render(f"ALIENAÇÃO (Matrix): {int(player.alienacao)}%", True, WHITE)
        render_surf.blit(txt_ali, (25, 57))

        # Contador de Pílulas
        txt_score = font_medium.render(f"Pílulas Vermelhas: {score}", True, YELLOW)
        render_surf.blit(txt_score, (WIDTH - 320, 20))

    elif game_state == "GAMEOVER":
        render_surf.fill((40, 0, 0))
        t1 = font_large.render("VOCÊ FOI ALIENADO! 😭", True, RED)
        t2 = font_medium.render("Morflex tomou pílulas azuis demais.", True, WHITE)
        t3 = font_medium.render("Agora você trabalha 6x1 em escala presencial.", True, YELLOW)
        t4 = font_medium.render("Pressione 'R' para tentar despertar de novo!", True, GREEN)
        
        render_surf.blit(t1, (WIDTH//2 - t1.get_width()//2, 180))
        render_surf.blit(t2, (WIDTH//2 - t2.get_width()//2, 270))
        render_surf.blit(t3, (WIDTH//2 - t3.get_width()//2, 320))
        render_surf.blit(t4, (WIDTH//2 - t4.get_width()//2, 420))

    elif game_state == "WIN":
        render_surf.fill((0, 50, 20))
        t1 = font_large.render("MUNDO INTELIGÍVEL ALCANÇADO! 😎🕶️", True, GREEN)
        t2 = font_medium.render(f"Morflex coletou {score} pílulas e destruiu a iludente Matrix!", True, WHITE)
        t3 = font_medium.render("Platão e Sócrates estão orgulhosos de você.", True, YELLOW)
        t4 = font_medium.render("Pressione 'R' para transcender novamente!", True, WHITE)
        
        render_surf.blit(t1, (WIDTH//2 - t1.get_width()//2, 180))
        render_surf.blit(t2, (WIDTH//2 - t2.get_width()//2, 270))
        render_surf.blit(t3, (WIDTH//2 - t3.get_width()//2, 320))
        render_surf.blit(t4, (WIDTH//2 - t4.get_width()//2, 420))

    # --- CALCULAR TREMEDEIRA NA TELA ---
    offset_x = 0
    offset_y = 0
    if shake_intensity > 0:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        shake_intensity -= 1

    # Renderizar surface final com o tremor
    screen.fill(BLACK)
    screen.blit(render_surf, (offset_x, offset_y))

    pygame.display.flip()

pygame.quit()
sys.exit()