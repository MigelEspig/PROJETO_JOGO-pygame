import pygame, random, math, sys

pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MORFLEX V3: A ASCESE vs TIK TOK ☀️📱")
clock = pygame.time.Clock()

# Cores
BLACK, WHITE, GREEN, RED, BLUE = (0,0,0), (255,255,255), (0,255,70), (255,30,60), (30,144,255)
YELLOW, SKIN = (255,255,0), (255,205,148)
CYAN, PINK = (0, 255, 255), (255, 0, 80) # Cores do Boss

font_small = pygame.font.SysFont("Comic Sans MS", 18, bold=True)
font_med = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
font_large = pygame.font.SysFont("Comic Sans MS", 50, bold=True)

shake = 0
def add_shake(a): global shake; shake = max(shake, a)

# --- CHUVA MATRIX ESTÁ DE VOLTA ---
MATRIX_WORDS = ["MORFLEX", "CLT", "BOLETO", "CAVERNA", "LÓGICA", "CRINGE", "VIRAL", "TREND", "PLATÃO"]
class MatrixRain:
    def __init__(self):
        self.x, self.y = random.randint(0, WIDTH), random.randint(-HEIGHT, 0)
        self.speed, self.text = random.randint(4, 12), random.choice(MATRIX_WORDS)
        self.color = (0, random.randint(150, 255), 70)
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y, self.x = random.randint(-100, 0), random.randint(0, WIDTH)
            self.text = random.choice(MATRIX_WORDS)
    def draw(self, s):
        s.blit(font_small.render(self.text, True, self.color), (self.x, self.y))

class FloatingText:
    def __init__(self, t, x, y, c=YELLOW):
        self.t, self.x, self.y, self.c, self.life = t, x, y, c, 40
    def update(self): self.y -= 2; self.life -= 1
    def draw(self, s):
        if self.life > 0: s.blit(font_med.render(self.t, True, self.c), (self.x, self.y))

# --- TIROS MELHORADOS ---
class LaserSocratico:
    def __init__(self, x, y):
        self.x, self.y, self.speed = x, y, -12
    def update(self): self.y += self.speed
    def draw(self, s):
        pygame.draw.rect(s, YELLOW, (self.x-4, self.y, 8, 25), border_radius=4)
        s.blit(font_small.render("LÓGICA!", True, YELLOW), (self.x+10, self.y))

class Morflex:
    def __init__(self):
        self.x, self.y, self.r, self.s = WIDTH//2, HEIGHT//2, 28, 8
        self.desp, self.alien = 0, 0
        self.lasers, self.last_shot = [], 0
    def move(self, keys):
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        if dx and dy: dx *= 0.707; dy *= 0.707
        self.x = max(self.r, min(WIDTH-self.r, self.x + dx * self.s))
        self.y = max(self.r, min(HEIGHT-self.r, self.y + dy * self.s))
        for l in self.lasers[:]:
            l.update()
            if l.y < 0: self.lasers.remove(l)
    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_shot > 250: # Cooldown de 250ms
            self.lasers.append(LaserSocratico(self.x, self.y - 20))
            self.last_shot = agora
            add_shake(3)
    def draw(self, s):
        for l in self.lasers: l.draw(s)
        pygame.draw.rect(s, (20,20,20), (self.x-22, self.y+10, 44, 35), border_radius=8)
        pygame.draw.circle(s, SKIN, (int(self.x), int(self.y)), self.r)
        pygame.draw.rect(s, BLACK, (self.x-22, self.y-10, 18, 12), border_radius=3)
        pygame.draw.rect(s, BLACK, (self.x+4, self.y-10, 18, 12), border_radius=3)
        s.blit(font_small.render("MORFLEX", True, GREEN), (self.x-40, self.y-48))

class RedPill:
    def __init__(self): self.respawn()
    def respawn(self): self.x, self.y, self.pulse = random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50), 0
    def draw(self, s):
        self.pulse += 0.2; r = int(14 + math.sin(self.pulse)*4)
        pygame.draw.ellipse(s, RED, (self.x-r, self.y-10, r*2, 20))
        s.blit(font_small.render("VERDADE", True, RED), (self.x-35, self.y-30))

class BluePill:
    def __init__(self): self.respawn()
    def respawn(self):
        self.x, self.y = random.randint(50, WIDTH-50), random.choice([-50, HEIGHT+50])
        self.vx, self.vy = random.choice([-6,6]), random.choice([-6,6])
        self.q = random.choice(["FICA NA MATRIX!", "DORME MAIS!", "6X1 É VIDA!"])
    def update(self):
        self.x += self.vx; self.y += self.vy
        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < -100 or self.y > HEIGHT+100: self.vy *= -1
    def draw(self, s):
        pygame.draw.ellipse(s, BLUE, (self.x-16, self.y-10, 32, 20))
        s.blit(font_small.render(self.q, True, BLUE), (self.x-40, self.y+12))

# --- O CHEFÃO TIK TOK ---
class Brainrot:
    def __init__(self, x, y):
        self.x, self.y, self.vy = x, y, random.randint(6, 10)
        self.q = random.choice(["FAZ A DC!", "POV", "TRENDING", "CRINGE"])
    def update(self): self.y += self.vy
    def draw(self, s):
        pygame.draw.rect(s, CYAN, (self.x-2, self.y-2, 30, 30))
        pygame.draw.rect(s, PINK, (self.x+2, self.y+2, 30, 30))
        pygame.draw.rect(s, WHITE, (self.x, self.y, 30, 30))
        s.blit(font_small.render(self.q, True, PINK), (self.x-10, self.y-20))

class TikTokBoss:
    def __init__(self):
        self.x, self.y, self.w, self.h = WIDTH//2, 100, 120, 120
        self.hp, self.max_hp = 100, 100
        self.vx = 8
        self.ataques = []
        self.timer_ataque = 0
    def update(self):
        self.x += self.vx
        if self.x < 50 or self.x > WIDTH - 150: self.vx *= -1
        
        self.timer_ataque += 1
        if self.timer_ataque > 30: # Atira brainrot loucamente
            self.ataques.append(Brainrot(self.x + self.w//2, self.y + self.h))
            self.timer_ataque = 0
            
        for a in self.ataques[:]:
            a.update()
            if a.y > HEIGHT: self.ataques.remove(a)
    def draw(self, s):
        # Efeito Glitch do logo
        pygame.draw.rect(s, CYAN, (self.x-5, self.y-5, self.w, self.h), border_radius=20)
        pygame.draw.rect(s, PINK, (self.x+5, self.y+5, self.w, self.h), border_radius=20)
        pygame.draw.rect(s, BLACK, (self.x, self.y, self.w, self.h), border_radius=20)
        s.blit(font_large.render("TIK TOK", True, WHITE), (self.x - 40, self.y - 60))
        
        # Barra de Vida do Boss
        pygame.draw.rect(s, RED, (self.x-20, self.y+130, 160, 15))
        pygame.draw.rect(s, GREEN, (self.x-20, self.y+130, int(160 * (self.hp/self.max_hp)), 15))
        
        for a in self.ataques: a.draw(s)

# Setup
rains = [MatrixRain() for _ in range(30)]
p, rp, bpills = Morflex(), RedPill(), [BluePill() for _ in range(5)]
texts, state, score, boss = [], "PLAYING", 0, None

while True:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and state not in ["PLAYING", "BOSS"]:
                p, rp, bpills = Morflex(), RedPill(), [BluePill() for _ in range(5)]
                texts, state, score, boss = [], "PLAYING", 0, None

    keys = pygame.key.get_pressed()
    if state in ["PLAYING", "BOSS"]:
        p.move(keys)
        if keys[pygame.K_SPACE]: p.atirar()

        for t in texts[:]: t.update(); texts.remove(t) if t.life <= 0 else None

    if state == "PLAYING":
        for b in bpills: b.update()

        # Pegar Pílula Vermelha
        if math.hypot(p.x - rp.x, p.y - rp.y) < p.r + 15:
            score += 1; p.desp += 15; add_shake(10); rp.respawn()
            texts.append(FloatingText("EXPANDINDO A MENTE!", p.x-80, p.y-30, GREEN))
            if score % 2 == 0: bpills.append(BluePill())
            
            # TRIGGER DO BOSS FINAL!
            if p.desp >= 100:
                state = "BOSS"
                boss = TikTokBoss()
                bpills.clear() # Limpa as pílulas menores
                texts.append(FloatingText("O ALGORITMO DESPERTOU!!!", WIDTH//2 - 200, HEIGHT//2, RED))
                add_shake(30)

        # Colisão Laser vs Pílula Azul
        for l in p.lasers[:]:
            for b in bpills[:]:
                if math.hypot(l.x - b.x, l.y - b.y) < 25:
                    add_shake(5); bpills.remove(b); bpills.append(BluePill())
                    texts.append(FloatingText("REFUTADO!", b.x-30, b.y, WHITE))
                    if l in p.lasers: p.lasers.remove(l)

        # Colisão Morflex vs Pílula Azul
        for b in bpills:
            if math.hypot(p.x - b.x, p.y - b.y) < p.r + 15: p.alien += 2; add_shake(5)

        if p.alien >= 100: state = "GAMEOVER"

    elif state == "BOSS":
        boss.update()
        
        # Colisão Laser vs Boss
        for l in p.lasers[:]:
            if boss.x < l.x < boss.x + boss.w and boss.y < l.y < boss.y + boss.h:
                boss.hp -= 2
                add_shake(8)
                texts.append(FloatingText("LÓGICA NELE!", l.x, l.y, YELLOW))
                if l in p.lasers: p.lasers.remove(l)
        
        # Colisão Brainrot vs Morflex
        for a in boss.ataques[:]:
            if math.hypot(p.x - a.x, p.y - a.y) < p.r + 15:
                p.alien += 5
                add_shake(10)
                texts.append(FloatingText("CÉREBRO DERRETENDO!", p.x-50, p.y, RED))
                if a in boss.ataques: boss.ataques.remove(a)
                
        if p.alien >= 100: state = "GAMEOVER"
        if boss.hp <= 0: state = "WIN"; add_shake(40)

    # --- RENDERIZAÇÃO ---
    surf = pygame.Surface((WIDTH, HEIGHT))
    # Fundo muda na boss fight
    if state == "BOSS":
        cor_fundo = (random.randint(0,20), 0, random.randint(0,20))
        surf.fill(cor_fundo)
        for r in rains: r.speed = 15; r.update(); r.draw(surf) # Chuva rápida e frenética
    else:
        bg_color = (min(255, int(p.desp * 2.5)), min(255, int(p.desp * 2.5)), min(255, int(p.desp * 2.5))) if p.desp > 50 else BLACK
        surf.fill(bg_color)
        for r in rains: r.speed = random.randint(4,12); r.update(); r.draw(surf)

    if state in ["PLAYING", "BOSS"]:
        if state == "PLAYING": rp.draw(surf)
        for b in bpills: b.draw(surf)
        if state == "BOSS": boss.draw(surf)
        p.draw(surf)
        for t in texts: t.draw(surf)
        
        # Barras de Status
        pygame.draw.rect(surf, (50,50,50), (20,20,250,25)); pygame.draw.rect(surf, GREEN, (20,20,int(2.5*min(100, p.desp)),25))
        surf.blit(font_small.render(f"DESPERTAR: {int(min(100, p.desp))}%", True, WHITE if p.desp < 50 else BLACK), (25,22))
        pygame.draw.rect(surf, (50,50,50), (20,55,250,25)); pygame.draw.rect(surf, BLUE, (20,55,int(2.5*min(100, p.alien)),25))
        surf.blit(font_small.render(f"ALIENAÇÃO: {int(min(100, p.alien))}%", True, WHITE), (25,57))

    elif state == "GAMEOVER":
        surf.fill((40,0,0))
        surf.blit(font_large.render("FALHOU NA ASCESE...", True, RED), (180, 200))
        surf.blit(font_med.render("Seu cérebro foi derretido pelo algoritmo.", True, WHITE), (150, 300))
        surf.blit(font_med.render("Pressione 'R' para tentar de novo", True, YELLOW), (200, 380))
    elif state == "WIN":
        surf.fill(WHITE)
        surf.blit(font_large.render("ASCESE COMPLETA! 🧘‍♂️☀️", True, YELLOW), (130, 200))
        surf.blit(font_med.render("Você derrotou o Algoritmo e saiu da Caverna!", True, BLACK), (100, 300))
        surf.blit(font_med.render("Sócrates chora de emoção.", True, BLUE), (250, 350))

    ox, oy = (random.randint(-shake, shake), random.randint(-shake, shake)) if shake > 0 else (0,0)
    if shake > 0: shake -= 1
    screen.fill(BLACK); screen.blit(surf, (ox, oy))
    pygame.display.flip()