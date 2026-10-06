import pygame, random, math, sys

pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MORFLEX V2: A ASCESE DEFINITIVA ☀️🕶️")
clock = pygame.time.Clock()

# Cores
BLACK, WHITE, GREEN, RED, BLUE, YELLOW, SKIN = (0,0,0), (255,255,255), (0,255,70), (255,30,60), (30,144,255), (255,255,0), (255,205,148)
font_small = pygame.font.SysFont("Comic Sans MS", 18, bold=True)
font_med = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
font_large = pygame.font.SysFont("Comic Sans MS", 50, bold=True)

shake = 0
def add_shake(a): global shake; shake = max(shake, a)

class FloatingText:
    def __init__(self, t, x, y, c=YELLOW):
        self.t, self.x, self.y, self.c, self.life = t, x, y, c, 40
    def update(self): self.y -= 2; self.life -= 1
    def draw(self, s):
        if self.life > 0: s.blit(font_med.render(self.t, True, self.c), (self.x, self.y))

class LaserSocratico:
    def __init__(self, x, y):
        self.x, self.y, self.speed = x, y, -10
    def update(self): self.y += self.speed
    def draw(self, s):
        pygame.draw.rect(s, YELLOW, (self.x-3, self.y, 6, 20))
        s.blit(font_small.render("LÓGICA!", True, YELLOW), (self.x+10, self.y))

class Morflex:
    def __init__(self):
        self.x, self.y, self.r, self.s = WIDTH//2, HEIGHT//2, 28, 8
        self.desp, self.alien = 0, 0
        self.lasers = []
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
        self.lasers.append(LaserSocratico(self.x, self.y - 20))
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
        self.vx, self.vy = random.choice([-5,5]), random.choice([-5,5])
        self.q = random.choice(["FICA NA MATRIX!", "DORME MAIS!", "6X1 É VIDA!"])
    def update(self):
        self.x += self.vx; self.y += self.vy
        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < -100 or self.y > HEIGHT+100: self.vy *= -1
    def draw(self, s):
        pygame.draw.ellipse(s, BLUE, (self.x-16, self.y-10, 32, 20))
        s.blit(font_small.render(self.q, True, BLUE), (self.x-40, self.y+12))

# Setup
p, rp, bpills, texts, state = Morflex(), RedPill(), [BluePill() for _ in range(5)], [], "PLAYING"
score = 0

while True:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT: sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and state == "PLAYING": p.atirar()
            if e.key == pygame.K_r and state != "PLAYING":
                p, rp, bpills, texts, state, score = Morflex(), RedPill(), [BluePill() for _ in range(5)], [], "PLAYING", 0

    if state == "PLAYING":
        p.move(pygame.key.get_pressed())
        for b in bpills: b.update()
        for t in texts[:]: t.update(); texts.remove(t) if t.life <= 0 else None

        # Pílula Vermelha
        if math.hypot(p.x - rp.x, p.y - rp.y) < p.r + 15:
            score += 1; p.desp += 10; add_shake(15); rp.respawn()
            texts.append(FloatingText("MAIS PERTO DO SOL!", p.x-50, p.y-30, GREEN))
            if score % 2 == 0: bpills.append(BluePill())

        # Colisão Laser vs Pílula Azul
        for l in p.lasers[:]:
            for b in bpills[:]:
                if math.hypot(l.x - b.x, l.y - b.y) < 25:
                    add_shake(8); bpills.remove(b); bpills.append(BluePill())
                    texts.append(FloatingText("REFUTADO!", b.x-30, b.y, WHITE))
                    if l in p.lasers: p.lasers.remove(l)

        # Colisão Morflex vs Pílula Azul
        for b in bpills:
            if math.hypot(p.x - b.x, p.y - b.y) < p.r + 15:
                p.alien += 2; add_shake(5)

        if p.alien >= 100: state = "GAMEOVER"
        elif p.desp >= 100: state = "WIN"

    # Efeito do "Sol" (Mundo Inteligível clareando a tela)
    bg_color = (min(255, int(p.desp * 2.5)), min(255, int(p.desp * 2.5)), min(255, int(p.desp * 2.5))) if p.desp > 50 else BLACK
    surf = pygame.Surface((WIDTH, HEIGHT)); surf.fill(bg_color)

    if state == "PLAYING":
        rp.draw(surf)
        for b in bpills: b.draw(surf)
        p.draw(surf)
        for t in texts: t.draw(surf)
        
        # Barras
        pygame.draw.rect(surf, (50,50,50), (20,20,250,25)); pygame.draw.rect(surf, GREEN, (20,20,int(2.5*p.desp),25))
        surf.blit(font_small.render(f"DESPERTAR: {int(p.desp)}%", True, WHITE if p.desp < 50 else BLACK), (25,22))
        pygame.draw.rect(surf, (50,50,50), (20,55,250,25)); pygame.draw.rect(surf, BLUE, (20,55,int(2.5*p.alien),25))
        surf.blit(font_small.render(f"ALIENAÇÃO: {int(p.alien)}%", True, WHITE), (25,57))

    elif state == "GAMEOVER":
        surf.fill((40,0,0))
        surf.blit(font_large.render("FALHOU NA ASCESE...", True, RED), (200, 200))
        surf.blit(font_med.render("Pressione 'R' para tentar de novo", True, WHITE), (220, 300))
    elif state == "WIN":
        surf.fill(WHITE)
        surf.blit(font_large.render("O SOL DO BEM SUPREMO! ☀️", True, YELLOW), (100, 200))
        surf.blit(font_med.render("Você quebrou as correntes da caverna.", True, BLACK), (150, 300))

    ox, oy = (random.randint(-shake, shake), random.randint(-shake, shake)) if shake > 0 else (0,0)
    if shake > 0: shake -= 1
    screen.fill(BLACK); screen.blit(surf, (ox, oy))
    pygame.display.flip()