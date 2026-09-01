import math
import random


import pygame




WIDTH, HEIGHT = 960, 600
FPS = 60
TOTAL_WAVES = 40
ARENA = pygame.Rect(34, 86, WIDTH - 68, HEIGHT - 120)
OBSTACLES = []
BOSS_WAVES = {4, 8, 12, 16, 20, 24, 28, 32, 36, 40}
EXTRA_ENEMIES = [
    "blade", "archer", "reflector", "shielder", "healer", "dasher", "tunneler", "frostling", "pyromancer", "splitter",
    "sentinel", "vampire", "summoner", "orbiter", "mine", "stormer", "duelist", "crusher", "phantom", "executioner",
]
BG = (8, 10, 18)
PANEL = (20, 22, 31)
WHITE = (231, 235, 224)
MUTED = (137, 145, 157)
CYAN = (133, 196, 205)
RED = (171, 50, 67)
GOLD = (218, 198, 137)
MANA = (74, 145, 214)




def clamp(value, low, high):
    return max(low, min(high, value))




def draw_text(screen, font, text, position, color=WHITE, center=False):
    image = font.render(text, True, color)
    rect = image.get_rect(center=position) if center else image.get_rect(topleft=position)
    screen.blit(image, rect)




def move_with_obstacles(position, movement, radius):
    position = pygame.Vector2(position)
    for axis in ("x", "y"):
        candidate = pygame.Vector2(position)
        setattr(candidate, axis, getattr(candidate, axis) + getattr(movement, axis))
        candidate.x = clamp(candidate.x, ARENA.left + radius, ARENA.right - radius)
        candidate.y = clamp(candidate.y, ARENA.top + radius, ARENA.bottom - radius)
        if not any(
            obstacle.inflate(radius * 2, radius * 2).collidepoint(candidate) for obstacle in OBSTACLES
        ):
            position = candidate
    return position




def spawn_point():
    side = random.randrange(4)
    if side == 0:
        return pygame.Vector2(random.randint(ARENA.left, ARENA.right), ARENA.top - 24)
    if side == 1:
        return pygame.Vector2(ARENA.right + 24, random.randint(ARENA.top, ARENA.bottom))
    if side == 2:
        return pygame.Vector2(random.randint(ARENA.left, ARENA.right), ARENA.bottom + 24)
    return pygame.Vector2(ARENA.left - 24, random.randint(ARENA.top, ARENA.bottom))




def active_bosses(game):
    return game["bosses"]




def nearest_target(game, position):
    targets = game["enemies"] + active_bosses(game)
    return min(targets, key=lambda target: target.position.distance_to(position), default=None)




class Particle:
    def __init__(self, position, color, speed=80, life=0.45, size=4):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(1, 0).rotate(random.randrange(360)) * random.uniform(speed * 0.35, speed)
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size


    def update(self, dt):
        self.position += self.velocity * dt
        self.velocity *= 0.92 ** (dt * 60)
        self.life -= dt


    def draw(self, screen):
        if self.life > 0:
            radius = max(1, int(self.size * self.life / self.max_life))
            pygame.draw.circle(screen, self.color, self.position, radius)




class Fireball:
    def __init__(self, position, target):
        self.position = pygame.Vector2(position)
        direction = pygame.Vector2(target) - self.position
        self.velocity = direction.normalize() * 610 if direction.length() else pygame.Vector2(1, 0) * 610
        self.life = 1.3
        self.radius = 9
        self.reflected = False


    def update(self, dt):
        self.position += self.velocity * dt
        self.life -= dt


    def draw(self, screen):
        pygame.draw.circle(screen, (185, 95, 255) if self.reflected else (255, 104, 35), self.position, 14)
        pygame.draw.circle(screen, (255, 226, 105), self.position, 8)
        pygame.draw.circle(screen, WHITE, self.position - self.velocity.normalize() * 8, 3)




class Arrow:
    def __init__(self, position, target):
        self.position = pygame.Vector2(position)
        direction = pygame.Vector2(target) - self.position
        self.velocity = direction.normalize() * 760 if direction.length() else pygame.Vector2(1, 0) * 760
        self.life = 1.1
        self.radius = 5
        self.reflected = False


    def update(self, dt):
        self.position += self.velocity * dt
        self.life -= dt


    def draw(self, screen):
        tail = self.position - self.velocity.normalize() * 13
        pygame.draw.line(screen, (185, 95, 255) if self.reflected else (196, 137, 76), tail, self.position, 4)
        pygame.draw.polygon(screen, WHITE, [self.position, self.position - self.velocity.normalize().rotate(25) * 9, self.position - self.velocity.normalize().rotate(-25) * 9])




class EnemyBolt:
    def __init__(self, position, target):
        self.position = pygame.Vector2(position)
        direction = pygame.Vector2(target) - self.position
        self.velocity = direction.normalize() * 185 if direction.length() else pygame.Vector2(1, 0) * 185
        self.life = 4


    def update(self, dt):
        self.position += self.velocity * dt
        self.life -= dt


    def draw(self, screen):
        pygame.draw.circle(screen, (255, 119, 78), self.position, 8)
        pygame.draw.circle(screen, (255, 226, 139), self.position, 4)




class PinAttack:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.life = 1.1
        self.radius = 28


    def update(self, dt):
        self.life -= dt


    @property
    def active(self):
        return self.life < 0.35


    def draw(self, screen):
        color = RED if self.active else GOLD
        pygame.draw.circle(screen, color, self.position, self.radius + 5, 3)
        pygame.draw.circle(screen, WHITE, self.position, max(4, int(self.radius * (1 - self.life / 1.1))), 2)




class BossField:
    def __init__(self, position, radius, kind, life=4.0):
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.kind = kind
        self.life = life
        self.max_life = life


    def update(self, dt):
        self.life -= dt


    def draw(self, screen):
        progress = max(0, self.life / self.max_life)
        color = (238, 35, 58) if self.kind == "corruption" else (126, 45, 188)
        pygame.draw.circle(screen, color, self.position, self.radius, 3)
        pygame.draw.circle(screen, (20, 4, 25), self.position, max(1, int(self.radius * progress)), 2)




class MagicEffect:
    def __init__(self, kind, position, target=None, radius=0):
        self.kind = kind
        self.position = pygame.Vector2(position)
        self.target = pygame.Vector2(target) if target is not None else None
        self.radius = radius
        self.life = 0.22 if kind == "lightning" else 0.42
        self.max_life = self.life


    def update(self, dt):
        self.life -= dt


    def draw(self, screen):
        if self.kind == "lightning":
            end = self.target or self.position
            pygame.draw.line(screen, WHITE, self.position, end, 5)
            pygame.draw.line(screen, CYAN, self.position, end, 2)
            pygame.draw.circle(screen, WHITE, end, 9)
        else:
            progress = 1 - self.life / self.max_life
            radius = max(1, int(self.radius * min(1, progress * 1.5)))
            pygame.draw.circle(screen, GOLD, self.position, radius, 4)
            pygame.draw.circle(screen, WHITE, self.position, max(1, radius - 9), 2)




class SlashEffect:
    def __init__(self, position, target):
        self.position = pygame.Vector2(position)
        direction = pygame.Vector2(target) - self.position
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) if direction.length_squared() else 0
        self.life = 0.18
        self.max_life = self.life


    def update(self, dt):
        self.life -= dt


    def draw(self, screen):
        progress = 1 - self.life / self.max_life
        radius = int(48 + progress * 30)
        rect = pygame.Rect(self.position.x - radius, self.position.y - radius, radius * 2, radius * 2)
        start = math.radians(self.angle - 62 + progress * 20)
        end = math.radians(self.angle + 62 + progress * 20)
        direction = pygame.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle)))
        perpendicular = pygame.Vector2(-direction.y, direction.x)
        blade_base = self.position + direction * 12
        blade_tip = self.position + direction * 64
        blade = [
            blade_base + perpendicular * 7,
            blade_tip,
            blade_base - perpendicular * 7,
        ]
        guard_center = self.position + direction * 9
        guard_start = guard_center - perpendicular * 15
        guard_end = guard_center + perpendicular * 15
        handle_start = self.position - direction * 15
        handle_end = self.position + direction * 7
        pygame.draw.arc(screen, (39, 78, 105), rect, start, end, 10)
        pygame.draw.arc(screen, WHITE, rect, start, end, 6)
        pygame.draw.arc(screen, CYAN, rect, start, end, 3)
        pygame.draw.line(screen, (25, 28, 39), handle_start, handle_end, 9)
        pygame.draw.line(screen, GOLD, handle_start, handle_end, 5)
        pygame.draw.line(screen, WHITE, guard_start, guard_end, 5)
        pygame.draw.polygon(screen, (31, 48, 66), [point + perpendicular * 3 for point in blade])
        pygame.draw.polygon(screen, WHITE, blade)
        pygame.draw.line(screen, CYAN, blade_base, blade_tip - direction * 5, 2)




class Enemy:
    def __init__(self, kind, wave, position=None):
        self.kind = kind
        self.position = pygame.Vector2(position) if position is not None else spawn_point()
        sizes = {"stalker": 16, "brute": 21, "charger": 18, "spitter": 17, "wisp": 14, "bomber": 19, "sniper": 16, "guardian": 24, "hexer": 15}
        sizes.update({kind: 15 + index % 4 for index, kind in enumerate(EXTRA_ENEMIES)})
        self.radius = sizes[kind]
        base_health = {"stalker": 28, "brute": 64, "charger": 42, "spitter": 36, "wisp": 25, "bomber": 48, "sniper": 34, "guardian": 105, "hexer": 30}
        base_health.update({kind: 34 + index * 3 for index, kind in enumerate(EXTRA_ENEMIES)})
        self.max_health = base_health[kind] + wave * (7 if kind != "brute" else 12)
        self.health = self.max_health
        base_speed = {"stalker": 82, "brute": 48, "charger": 65, "spitter": 42, "wisp": 105, "bomber": 58, "sniper": 30, "guardian": 35, "hexer": 70}
        base_speed.update({kind: 48 + index * 2 for index, kind in enumerate(EXTRA_ENEMIES)})
        self.speed = base_speed[kind] + wave * 4
        self.hit_flash = 0
        self.timer = random.uniform(0, 6)
        self.attack_timer = random.uniform(1.2, 2.5)
        self.skill_timer = random.uniform(2, 4)
        self.shield = 60 if kind in ("guardian", "shielder", "sentinel") else 0
        self.reflect = kind in ("reflector", "sentinel")
        self.resist = 0.35 if kind in ("crusher", "sentinel") else 0
        self.slow_timer = 0


    def update(self, player, dt, enemy_shots):
        self.timer += dt
        self.attack_timer -= dt
        self.skill_timer -= dt
        self.slow_timer = max(0, self.slow_timer - dt)
        direction = player.position - self.position
        if direction.length_squared():
            speed_factor = 0.48 if self.slow_timer > 0 else 1
            travel = direction.normalize()
            if self.kind == "wisp":
                travel = travel.rotate(math.sin(self.timer * 5) * 55)
            elif self.kind == "charger" and self.attack_timer <= 0:
                self.position = move_with_obstacles(self.position, travel * 270 * dt * speed_factor, self.radius)
                if self.attack_timer <= -0.55:
                    self.attack_timer = 2.2
            elif self.kind == "sniper":
                if direction.length() < 310:
                    travel = -travel
                self.position = move_with_obstacles(self.position, travel * self.speed * dt * speed_factor, self.radius)
            elif self.kind in ("dasher", "duelist", "executioner") and self.attack_timer <= 0:
                self.position = move_with_obstacles(self.position, travel * 330 * dt * speed_factor, self.radius)
                if self.attack_timer <= -0.45:
                    self.attack_timer = 2.1
            elif self.kind in ("archer", "pyromancer", "stormer", "orbiter"):
                if direction.length() < 280:
                    travel = -travel
                self.position = move_with_obstacles(self.position, travel * self.speed * dt * speed_factor, self.radius)
            else:
                self.position = move_with_obstacles(self.position, travel * self.speed * dt * speed_factor, self.radius)
            if self.kind in ("spitter", "sniper", "hexer") and self.attack_timer <= 0:
                enemy_shots.append(EnemyBolt(self.position, player.position))
                self.attack_timer = 1.4 if self.kind == "sniper" else 2.3
            if self.kind in ("archer", "pyromancer", "stormer", "orbiter") and self.attack_timer <= 0:
                enemy_shots.extend(EnemyBolt(self.position, player.position) for _ in range(3 if self.kind == "stormer" else 1))
                self.attack_timer = 1.2 if self.kind == "archer" else 2.4
            if self.kind == "bomber" and self.skill_timer <= 0:
                enemy_shots.extend(EnemyBolt(self.position, player.position) for _ in range(6))
                self.skill_timer = 4.5
            if self.kind == "guardian" and self.skill_timer <= 0:
                self.shield = min(60, self.shield + 30)
                self.skill_timer = 4
        self.hit_flash = max(0, self.hit_flash - dt)


    def draw(self, screen):
        colors = {"stalker": (187, 74, 207), "brute": (72, 174, 129), "charger": (239, 116, 55), "spitter": (68, 188, 198), "wisp": (239, 218, 91), "bomber": (232, 75, 93), "sniper": (112, 155, 226), "guardian": (173, 137, 69), "hexer": (123, 88, 190)}
        colors.update({kind: ((70 + index * 17) % 220, (45 + index * 29) % 190, (85 + index * 23) % 220) for index, kind in enumerate(EXTRA_ENEMIES)})
        color = WHITE if self.hit_flash else colors[self.kind]
        pygame.draw.circle(screen, (35, 42, 69), self.position, self.radius + 5)
        pygame.draw.circle(screen, color, self.position, self.radius)
        if self.kind == "stalker":
            pygame.draw.circle(screen, (247, 121, 229), self.position, 6)
            pygame.draw.line(screen, BG, self.position - (8, 8), self.position + (8, 8), 3)
            pygame.draw.line(screen, BG, self.position + (8, -8), self.position - (8, -8), 3)
        elif self.kind == "brute":
            pygame.draw.rect(screen, (180, 239, 189), pygame.Rect(self.position.x - 9, self.position.y - 5, 18, 10), border_radius=3)
        elif self.kind == "charger":
            pygame.draw.polygon(screen, WHITE, [(self.position.x + 10, self.position.y), (self.position.x - 5, self.position.y - 8), (self.position.x - 5, self.position.y + 8)])
        elif self.kind == "spitter":
            pygame.draw.circle(screen, (14, 43, 51), self.position, 6)
        elif self.kind == "bomber":
            pygame.draw.circle(screen, WHITE, self.position, 7, 2)
        elif self.kind == "sniper":
            pygame.draw.line(screen, WHITE, self.position - (9, 9), self.position + (9, 9), 3)
        elif self.kind == "guardian":
            pygame.draw.polygon(screen, WHITE, [(self.position.x, self.position.y - 12), (self.position.x + 11, self.position.y), (self.position.x, self.position.y + 12), (self.position.x - 11, self.position.y)])
            pygame.draw.circle(screen, CYAN, self.position, self.radius + 3, 2)
        elif self.kind == "hexer":
            pygame.draw.circle(screen, WHITE, self.position, 5)
        else:
            pygame.draw.circle(screen, WHITE, self.position, 3)
        bar = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius - 11, self.radius * 2, 4)
        pygame.draw.rect(screen, (54, 25, 45), bar)
        pygame.draw.rect(screen, RED, (bar.x, bar.y, bar.width * self.health / self.max_health, bar.height))
        if self.shield:
            pygame.draw.rect(screen, CYAN, (bar.x, bar.y - 5, bar.width * self.shield / 60, 3))




class Boss:
    def __init__(self, wave):
        self.kind = {4: "MURALHA", 8: "LANCA-SOMBRIA", 12: "COLOSSO", 16: "ARQUIVISTA", 20: "ABISMO", 24: "CARRASCO", 28: "ORACULO", 32: "GENERAL", 36: "DEVORADOR", 40: "PECADOR SOMBRIO"}.get(wave, "MURALHA")
        self.radius = 38 if wave < 40 else 58
        self.position = spawn_point()
        self.max_health = 30000 if wave == 40 else 650 + wave * 90
        self.health = self.max_health
        self.timer = 0
        self.attack_timer = 2.4
        self.dash = 0
        self.dash_target = pygame.Vector2(self.position)
        self.hit_flash = 0
        self.wall_jump = 0
        self.pin_timer = 2.5
        self.rain_timer = 1.8
        self.phase = 1
        self.damage_resist = 0.82 if wave == 40 else 0
        self.previous_phase = 1
        self.summon_timer = 3.0
        self.effect_timer = 2.0


    def update(self, player, dt, particles, enemy_shots, attacks, minions):
        self.timer += dt
        self.attack_timer -= dt
        self.hit_flash = max(0, self.hit_flash - dt)
        self.pin_timer -= dt
        self.rain_timer -= dt
        if self.kind == "PECADOR SOMBRIO":
            ratio = self.health / self.max_health
            self.phase = 5 if ratio <= 0.2 else 4 if ratio <= 0.4 else 3 if ratio <= 0.6 else 2 if ratio <= 0.8 else 1
        else:
            self.phase = 2 if self.health <= self.max_health * 0.5 else 1
        self.summon_timer -= dt
        self.effect_timer -= dt
        if self.phase != self.previous_phase:
            self.previous_phase = self.phase
            self.summon_timer = 0
        if self.wall_jump > 0:
            movement = self.position.lerp(self.dash_target, min(1, dt * 7)) - self.position
            self.position = move_with_obstacles(self.position, movement, self.radius)
            self.wall_jump -= dt
        elif self.dash > 0:
            direction = self.dash_target - self.position
            if direction.length() > 5:
                self.position = move_with_obstacles(self.position, direction.normalize() * 460 * dt, self.radius)
            self.dash -= dt
        else:
            direction = player.position - self.position
            if direction.length() > 175:
                self.position = move_with_obstacles(self.position, direction.normalize() * 42 * dt, self.radius)
        if self.attack_timer <= 0:
            self.attack_timer = 3.4
            if self.kind == "MURALHA" or random.random() < 0.35:
                wall_targets = [pygame.Vector2(ARENA.left + 45, random.randint(ARENA.top + 30, ARENA.bottom - 30)), pygame.Vector2(ARENA.right - 45, random.randint(ARENA.top + 30, ARENA.bottom - 30))]
                self.dash_target = random.choice(wall_targets)
                self.wall_jump = 0.8
                for angle in range(0, 360, 45):
                    particles.append(ScytheWave(self.position, angle))
            elif random.random() < 0.5:
                self.dash_target = pygame.Vector2(player.position)
                self.dash = 0.65
            else:
                for angle in range(0, 360, 30):
                    particles.append(ScytheWave(self.position, angle))
        if self.pin_timer <= 0:
            pin_count = 14 if self.kind == "PECADOR SOMBRIO" else 1
            positions = [player.position] if pin_count == 1 else [pygame.Vector2(random.randint(ARENA.left + 35, ARENA.right - 35), random.randint(ARENA.top + 25, ARENA.bottom - 25)) for _ in range(pin_count)]
            attacks.extend(PinAttack(position) for position in positions)
            self.pin_timer = 1.25 if self.kind == "PECADOR SOMBRIO" else 4.5
        if self.kind == "PECADOR SOMBRIO" and self.rain_timer <= 0:
            for angle in range(0, 360, 13 if self.phase >= 4 else 22):
                particles.append(ScytheWave(self.position, angle))
            for _ in range(10 if self.phase == 2 else 5):
                enemy_shots.append(EnemyBolt(self.position, player.position))
            self.rain_timer = max(0.55, 2.2 - self.phase * 0.3)
        if self.kind == "PECADOR SOMBRIO" and self.summon_timer <= 0:
            minion_kinds = {
                1: ("archer", "shielder"),
                2: ("dasher", "pyromancer"),
                3: ("reflector", "stormer"),
                4: ("executioner", "sentinel"),
                5: ("crusher", "phantom"),
            }[self.phase]
            side_positions = [spawn_point() for _ in range(4)]
            for index, position in enumerate(side_positions):
                minion = Enemy(minion_kinds[index % 2], 20 + self.phase * 4, position)
                minion.max_health *= 2.2
                minion.health = minion.max_health
                minions.append(minion)
            self.summon_timer = max(1.0, 4.2 - self.phase * 0.65)
        if self.effect_timer <= 0:
            effect_kind = "corruption" if self.phase % 2 else "void"
            radius = 115 + self.phase * 20
            attacks.append(BossField(player.position, radius, effect_kind, 2.6 if self.phase >= 4 else 3.5))
            self.effect_timer = max(0.7, 3.2 - self.phase * 0.45)
        if self.kind in ("LANCA-SOMBRIA", "ARQUIVISTA") and self.attack_timer < 1.4 and random.random() < dt * 2:
            enemy_shots.append(EnemyBolt(self.position, player.position))


    def draw(self, screen):
        aura = 55 + int(math.sin(self.timer * 4) * 5)
        pygame.draw.circle(screen, (75, 25, 60), self.position, aura, 2)
        pygame.draw.circle(screen, (36, 22, 47), self.position, self.radius + 7)
        boss_color = (183, 42, 79) if self.kind == "PECADOR SOMBRIO" else (76, 104, 190)
        if self.kind == "PECADOR SOMBRIO":
            pygame.draw.circle(screen, (8, 3, 8), self.position, self.radius + 13, 5)
            pygame.draw.arc(screen, (255, 35, 57), (self.position.x - 65, self.position.y - 65, 130, 130), self.timer, self.timer + 4.8, 5)
        pygame.draw.circle(screen, WHITE if self.hit_flash else boss_color, self.position, self.radius)
        pygame.draw.circle(screen, (45, 17, 36), self.position, 28)
        pygame.draw.polygon(screen, GOLD, [(self.position.x - 11, self.position.y - 8), (self.position.x - 2, self.position.y - 19), (self.position.x + 8, self.position.y - 8), (self.position.x + 2, self.position.y + 3)])
        scythe_start = self.position + pygame.Vector2(29, -28).rotate(self.timer * 100)
        scythe_end = scythe_start + pygame.Vector2(0, 72).rotate(self.timer * 100)
        pygame.draw.line(screen, (220, 225, 242), scythe_start, scythe_end, 7)
        pygame.draw.arc(screen, GOLD, (scythe_end.x - 24, scythe_end.y - 25, 48, 50), 2.5, 5.7, 6)
        if self.kind == "PECADOR SOMBRIO":
            pygame.draw.polygon(screen, (255, 50, 55), [(self.position.x - 18, self.position.y - 30), (self.position.x - 8, self.position.y - 53), (self.position.x, self.position.y - 34), (self.position.x + 12, self.position.y - 55), (self.position.x + 21, self.position.y - 28)])
        bar = pygame.Rect(180, 57, 600, 12)
        pygame.draw.rect(screen, (48, 25, 47), bar, border_radius=5)
        pygame.draw.rect(screen, RED, (bar.x, bar.y, bar.width * self.health / self.max_health, bar.height), border_radius=5)




class ScytheWave:
    def __init__(self, position, angle):
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(1, 0).rotate(angle)
        self.distance = 0
        self.life = 1.5


    def update(self, dt):
        self.distance += 250 * dt
        self.life -= dt


    def draw(self, screen):
        start = self.position + self.direction * self.distance
        end = start + self.direction * 26
        pygame.draw.line(screen, GOLD, start, end, 5)
        pygame.draw.circle(screen, (255, 235, 145), end, 4)




def reset_game():
    return {
        "player": pygame.Vector2(WIDTH / 2 - 100, HEIGHT / 2),
        "player2": {
            "position": pygame.Vector2(WIDTH / 2 + 100, HEIGHT / 2),
            "health": 120,
            "max_health": 120,
            "shield": 0,
            "armor": 0,
            "damage": 0,
            "regen": 0,
            "sword": 0,
            "bow": False,
            "equipment": {"weapon": "sword", "armor": "none"},
            "timers": {"sword": 0, "shot": 0, "arrow": 0, "lightning": 0, "nova": 0, "meteor": 0, "frost": 0},
        },
        "coop": False,
        "lives": 10,
        "health": 120,
        "max_health": 120,
        "mana": 100,
        "max_mana": 100,
        "shield": 0,
        "xp": 0,
        "xp_next": 100,
        "level": 1,
        "gold": 0,
        "skill_points": 0,
        "fireballs": [],
        "arrows": [],
        "enemy_shots": [],
        "enemies": [],
        "particles": [],
        "magic_effects": [],
        "slash_effects": [],
        "wave_attacks": [],
        "wave": 1,
        "kills": 0,
        "spawned": 0,
        "spawn_timer": 0,
        "shoot_timer": 0,
        "sword_timer": 0,
        "arrow_timer": 0,
        "spell_timers": {"lightning": 0, "nova": 0, "meteor": 0, "frost": 0},
        "upgrades": {"damage": 0, "speed": 0, "health": 0, "cooldown": 0, "nova": 0, "meteor": 0, "sword": 0, "regen": 0, "armor": 0, "spell": 0, "crit": 0},
        "unlocked": {"lightning": True, "nova": False, "meteor": False, "frost": False},
        "equipment": {"weapon": "sword", "armor": "none", "bow": False, "shield": False},
        "upgrade_options": [],
        "shop_options": [],
        "wave_break": 1.5,
        "boss": None,
        "bosses": [],
        "state": "playing",
    }




def choose_upgrades(game):
    pool = [
        ("1", "FOGO BRUTO", "Bolas causam +10 de dano"),
        ("2", "PASSO FANTASMA", "Velocidade de movimento +35"),
        ("3", "CORACAO DE CINZAS", "Vida maxima +25 e cura 25"),
        ("4", "CANALIZACAO", "Magias recarregam 25% mais rapido"),
        ("5", "NOVA AMPLIADA", "A explosao da tecla E fica maior"),
    ]
    game["upgrade_options"] = random.sample(pool, 3)
    game["state"] = "upgrade"




def open_shop(game):
    game["shop_options"] = [
        ("1", "LAMINA TEMPERADA", "Espada +8 dano (35 ouro)"),
        ("2", "ARMADURA DE CINZAS", "+25 vida maxima (45 ouro)"),
        ("3", "ESCUDO VIVO", "+35 escudo (40 ouro)"),
        ("4", "GRIMORIO DA NOVA", "Desbloqueia a magia E (80 ouro)"),
        ("5", "ESSENCIA VITAL", "+2 regeneracao por segundo (50 ouro)"),
        ("6", "MACHADO DE GUERRA", "Espada +20 dano (90 ouro)"),
        ("7", "COURACA RUBRA", "+10 armadura (100 ouro)"),
        ("8", "TOMO DO METEORO", "Desbloqueia magia R (130 ouro)"),
        ("9", "ARCO DO VIGIA", "Desbloqueia arco e flechas (110 ouro)"),
        ("0", "TOMO DO INVERNO", "Desbloqueia magia F (150 ouro)"),
    ]
    game["state"] = "shop"




def buy_shop_item(game, key):
    prices = {"1": 35, "2": 45, "3": 40, "4": 80, "5": 50, "6": 90, "7": 100, "8": 130, "9": 110, "0": 150}
    if game["gold"] < prices[key]:
        return False
    if key == "4" and (game["unlocked"]["nova"] or game["wave"] < 3):
        return False
    if key == "8" and game["unlocked"]["meteor"]:
        return False
    if key == "0" and game["unlocked"]["frost"]:
        return False
    game["gold"] -= prices[key]
    if key == "1":
        game["upgrades"]["sword"] += 8
        game["equipment"]["weapon"] = "tempered_sword"
    elif key == "2":
        game["max_health"] += 25
        game["health"] += 25
        game["upgrades"]["health"] += 25
        game["equipment"]["armor"] = "ashes"
    elif key == "3":
        game["shield"] += 35
        game["equipment"]["shield"] = True
    elif key == "4":
        game["unlocked"]["nova"] = True
    elif key == "5":
        game["upgrades"]["regen"] += 2
    elif key == "6":
        game["upgrades"]["sword"] += 20
        game["equipment"]["weapon"] = "war_axe"
    elif key == "7":
        game["upgrades"]["armor"] += 10
        game["equipment"]["armor"] = "red_cuirass"
    elif key == "8":
        game["unlocked"]["meteor"] = True
    elif key == "9":
        game["equipment"]["bow"] = True
        game["equipment"]["weapon"] = "bow"
    elif key == "0":
        game["unlocked"]["frost"] = True
    return True




def spend_skill(game, key):
    if game["skill_points"] <= 0:
        return False
    costs = {"1": "damage", "2": "health", "3": "regen", "4": "armor", "5": "spell", "6": "crit"}
    attribute = costs.get(key)
    if not attribute:
        return False
    game["skill_points"] -= 1
    if attribute == "damage":
        game["upgrades"]["damage"] += 6
    elif attribute == "health":
        game["max_health"] += 15
        game["health"] += 15
    elif attribute == "regen":
        game["upgrades"]["regen"] += 1
    else:
        game["upgrades"][attribute] += 4 if attribute == "armor" else 1
    return True




def award_xp(game, amount, gold):
    game["xp"] += amount
    game["gold"] += gold
    while game["xp"] >= game["xp_next"]:
        game["xp"] -= game["xp_next"]
        game["xp_next"] = int(game["xp_next"] * 1.25)
        game["level"] += 1
        game["skill_points"] += 1




def damage_player(game, amount):
    amount = max(1, amount - game["upgrades"]["armor"])
    absorbed = min(game["shield"], amount)
    game["shield"] -= absorbed
    game["health"] -= amount - absorbed




def damage_player_two(player, amount):
    amount = max(1, amount - player["armor"])
    absorbed = min(player["shield"], amount)
    player["shield"] -= absorbed
    player["health"] -= amount - absorbed




def respawn_at_checkpoint(game):
    if game["lives"] <= 0:
        return False
    game["lives"] -= 1
    game["health"] = game["max_health"]
    game["shield"] = 0
    game["player"] = pygame.Vector2(WIDTH / 2 - 100, HEIGHT / 2)
    player2 = game["player2"]
    player2["health"] = player2["max_health"]
    player2["shield"] = 0
    player2["position"] = pygame.Vector2(WIDTH / 2 + 100, HEIGHT / 2)
    game["enemies"].clear()
    game["enemy_shots"].clear()
    game["wave_attacks"].clear()
    game["bosses"].clear()
    game["boss"] = None
    game["spawned"] = 0
    game["spawn_timer"] = 1.0
    game["wave_break"] = 1.0
    return True




def damage_enemy(enemy, amount):
    amount *= 1 - getattr(enemy, "damage_resist", 0)
    amount *= 1 - getattr(enemy, "resist", 0)
    absorbed = min(getattr(enemy, "shield", 0), amount)
    enemy.shield = max(0, getattr(enemy, "shield", 0) - absorbed)
    enemy.health -= amount - absorbed




def reflect_projectile(enemy, projectile):
    if not getattr(enemy, "reflect", False) or getattr(projectile, "reflected", False):
        return False
    projectile.velocity *= -1
    projectile.reflected = True
    projectile.life = 0.75
    return True




def apply_upgrade(game, option):
    key = option[0]
    if key == "1":
        game["upgrades"]["damage"] += 10
    elif key == "2":
        game["upgrades"]["speed"] += 35
    elif key == "3":
        game["upgrades"]["health"] += 25
        game["max_health"] += 25
        game["health"] += 25
    elif key == "4":
        game["upgrades"]["cooldown"] += 1
    else:
        game["upgrades"]["nova"] += 1
    game["wave"] += 1
    game["spawned"] = 0
    game["spawn_timer"] = 0.6
    game["wave_break"] = 1.4
    game["state"] = "playing"




def main():
    pygame.init()
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cinzas da Foice")
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 44)
    font = pygame.font.Font(None, 25)
    small_font = pygame.font.Font(None, 20)
    game = reset_game()
    state = "title"


    while state != "quit":
        dt = min(clock.tick(FPS) / 1000, 0.04)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                state = "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "quit"
                if event.key == pygame.K_RETURN and state in ("title", "lost", "won"):
                    game = reset_game()
                    state = "playing"
                if state == "shop":
                    if event.unicode in "1234567890":
                        buy_shop_item(game, event.unicode)
                    elif event.key == pygame.K_k:
                        state = "skills"
                    elif event.key in (pygame.K_s, pygame.K_RETURN):
                        choose_upgrades(game)
                        state = "upgrade"
                if state == "skills":
                    if event.unicode in "123456":
                        spend_skill(game, event.unicode)
                    elif event.key in (pygame.K_b, pygame.K_ESCAPE):
                        state = "shop"
                if state == "upgrade" and event.unicode in "12345":
                    for option in game["upgrade_options"]:
                        if option[0] == event.unicode:
                            apply_upgrade(game, option)
                            state = "playing"
                            break


        if state == "title":
            screen.fill(BG)
            pygame.draw.rect(screen, PANEL, (110, 92, WIDTH - 220, HEIGHT - 170), border_radius=10)
            draw_text(screen, title_font, "CINZAS DA FOICE", (WIDTH // 2, 165), GOLD, True)
            draw_text(screen, font, "Um RPG de arena em ondas", (WIDTH // 2, 208), MUTED, True)
            draw_text(screen, font, "WASD / setas: mover     X: espada em area     ESPACO: bola de fogo", (WIDTH // 2, 300), WHITE, True)
            draw_text(screen, font, "Q/E/R/F: magias     B: arco     X: espada     Derrote 40 waves e o Pecador Sombrio.", (WIDTH // 2, 340), WHITE, True)
            draw_text(screen, font, "ENTER: começar partida solo", (WIDTH // 2, 380), CYAN, True)
            draw_text(screen, font, "PRESSIONE ENTER PARA COMECAR", (WIDTH // 2, 435), CYAN, True)
            pygame.display.flip()
            continue


        player = game["player"]
        player2 = game["player2"]
        if state == "playing":
            keys = pygame.key.get_pressed()
            horizontal = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
            vertical = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
            movement = pygame.Vector2(horizontal, vertical)
            player.x = clamp(player.x, ARENA.left + 18, ARENA.right - 18)
            player.y = clamp(player.y, ARENA.top + 18, ARENA.bottom - 18)


            game["shoot_timer"] -= dt
            game["sword_timer"] -= dt
            game["arrow_timer"] -= dt
            game["health"] = min(game["max_health"], game["health"] + game["upgrades"]["regen"] * dt)
            game["mana"] = min(game["max_mana"], game["mana"] + 8 * dt)
            movement_speed = 245 + game["upgrades"]["speed"]
            if movement.length_squared():
                player = move_with_obstacles(player, movement.normalize() * movement_speed * dt, 18)
                game["player"] = player
                player.x = clamp(player.x, ARENA.left + 18, ARENA.right - 18)
                player.y = clamp(player.y, ARENA.top + 18, ARENA.bottom - 18)


            if game["coop"]:
                p2_keys = pygame.key.get_pressed()
                p2_movement = pygame.Vector2(
                    p2_keys[pygame.K_RIGHT] - p2_keys[pygame.K_LEFT],
                    p2_keys[pygame.K_DOWN] - p2_keys[pygame.K_UP],
                )
                if p2_movement.length_squared():
                    player2["position"] = move_with_obstacles(player2["position"], p2_movement.normalize() * movement_speed * dt, 18)
                player2["position"].x = clamp(player2["position"].x, ARENA.left + 18, ARENA.right - 18)
                player2["position"].y = clamp(player2["position"].y, ARENA.top + 18, ARENA.bottom - 18)
                player2["health"] = min(player2["max_health"], player2["health"] + player2["regen"] * dt)
                for timer in player2["timers"]:
                    player2["timers"][timer] = max(0, player2["timers"][timer] - dt)
            game["spell_timers"]["lightning"] = max(0, game["spell_timers"]["lightning"] - dt)
            game["spell_timers"]["nova"] = max(0, game["spell_timers"]["nova"] - dt)
            game["spell_timers"]["meteor"] = max(0, game["spell_timers"]["meteor"] - dt)
            game["spell_timers"]["frost"] = max(0, game["spell_timers"]["frost"] - dt)
            cooldown_factor = max(0.5, 1 - game["upgrades"]["cooldown"] * 0.25)
            spell_costs = {"lightning": 18, "nova": 30, "meteor": 45, "frost": 35}
            if keys[pygame.K_q] and game["spell_timers"]["lightning"] <= 0 and game["mana"] >= spell_costs["lightning"]:
                game["mana"] -= spell_costs["lightning"]
                target = nearest_target(game, player)
                if target:
                    damage_enemy(target, 75 + game["upgrades"]["damage"] + game["upgrades"]["spell"])
                    target.hit_flash = 0.12
                    game["magic_effects"].append(MagicEffect("lightning", player, target.position))
                    for _ in range(18):
                        game["particles"].append(Particle(target.position, CYAN, 180, 0.35, 4))
                else:
                    game["magic_effects"].append(MagicEffect("lightning", player, player))
                game["spell_timers"]["lightning"] = 1.8 * cooldown_factor
            if game["unlocked"]["nova"] and keys[pygame.K_e] and game["spell_timers"]["nova"] <= 0 and game["mana"] >= spell_costs["nova"]:
                game["mana"] -= spell_costs["nova"]
                nova_radius = 115 + game["upgrades"]["nova"] * 25
                targets = game["enemies"] + active_bosses(game)
                for target in targets:
                    if target.position.distance_to(player) < nova_radius + target.radius:
                        damage_enemy(target, 55 + game["upgrades"]["damage"] + game["upgrades"]["spell"])
                        target.hit_flash = 0.12
                game["magic_effects"].append(MagicEffect("nova", player, radius=nova_radius))
                for _ in range(30):
                    game["particles"].append(Particle(player, GOLD, 240, 0.5, 6))
                game["spell_timers"]["nova"] = 4.5 * cooldown_factor


            if game["unlocked"]["meteor"] and keys[pygame.K_r] and game["spell_timers"]["meteor"] <= 0 and game["mana"] >= spell_costs["meteor"]:
                game["mana"] -= spell_costs["meteor"]
                target = nearest_target(game, player)
                meteor_target = target.position if target else player
                for target in game["enemies"] + active_bosses(game):
                    if target and target.position.distance_to(meteor_target) < 105 + target.radius:
                        damage_enemy(target, 130 + game["upgrades"]["spell"] * 2)
                        target.hit_flash = 0.2
                game["magic_effects"].append(MagicEffect("nova", meteor_target, radius=105))
                for _ in range(45):
                    game["particles"].append(Particle(meteor_target, RED, 280, 0.65, 7))
                game["spell_timers"]["meteor"] = 8 * cooldown_factor


            if game["unlocked"]["frost"] and keys[pygame.K_f] and game["spell_timers"]["frost"] <= 0 and game["mana"] >= spell_costs["frost"]:
                game["mana"] -= spell_costs["frost"]
                target = nearest_target(game, player)
                frost_target = target.position if target else player
                for target in game["enemies"] + active_bosses(game):
                    if target and target.position.distance_to(frost_target) < 135 + target.radius:
                        damage_enemy(target, 65 + game["upgrades"]["spell"])
                        target.hit_flash = 0.15
                game["magic_effects"].append(MagicEffect("nova", frost_target, radius=135))
                game["spell_timers"]["frost"] = 6 * cooldown_factor


            player_target = nearest_target(game, player)
            if keys[pygame.K_x] and game["sword_timer"] <= 0:
                slash_radius = 92
                slash_damage = 34 + game["upgrades"]["damage"] + game["upgrades"]["sword"] + game["upgrades"]["crit"] * 3
                for target in game["enemies"] + active_bosses(game):
                    if target and target.position.distance_to(player) <= slash_radius + target.radius:
                        damage_enemy(target, slash_damage)
                        target.hit_flash = 0.12
                slash_target = player_target.position if player_target else player + pygame.Vector2(1, 0)
                game["slash_effects"].append(SlashEffect(player, slash_target))
                game["sword_timer"] = 0.42
                for _ in range(8):
                    game["particles"].append(Particle(player, CYAN, 100, 0.3, 4))


            if keys[pygame.K_SPACE] and game["shoot_timer"] <= 0:
                fireball_target = player_target.position if player_target else player + pygame.Vector2(1, 0)
                game["fireballs"].append(Fireball(player, fireball_target))
                game["shoot_timer"] = 0.22
                for _ in range(4):
                    game["particles"].append(Particle(player, (255, 150, 48), 45, 0.25, 3))


            if game["coop"]:
                p2_keys = pygame.key.get_pressed()
                p2_position = player2["position"]
                p2_target = nearest_target(game, p2_position)
                p2_target_position = p2_target.position if p2_target else p2_position + pygame.Vector2(1, 0)
                if p2_keys[pygame.K_RSHIFT] and player2["timers"]["sword"] <= 0:
                    for target in game["enemies"] + active_bosses(game):
                        if target and target.position.distance_to(p2_position) <= 92 + target.radius:
                            damage_enemy(target, 34 + player2["damage"] + player2["sword"])
                            target.hit_flash = 0.12
                    game["slash_effects"].append(SlashEffect(p2_position, p2_target_position))
                    player2["timers"]["sword"] = 0.42
                if p2_keys[pygame.K_KP0] and player2["timers"]["shot"] <= 0:
                    game["fireballs"].append(Fireball(p2_position, p2_target_position))
                    player2["timers"]["shot"] = 0.22
                if p2_keys[pygame.K_KP5] and player2["bow"] and player2["timers"]["arrow"] <= 0:
                    game["arrows"].append(Arrow(p2_position, p2_target_position))
                    player2["timers"]["arrow"] = 0.3
                p2_targets = game["enemies"] + active_bosses(game)
                if p2_keys[pygame.K_KP1] and player2["timers"]["lightning"] <= 0 and p2_targets and game["mana"] >= spell_costs["lightning"]:
                    game["mana"] -= spell_costs["lightning"]
                    target = p2_target
                    damage_enemy(target, 75 + player2["damage"])
                    game["magic_effects"].append(MagicEffect("lightning", p2_position, target.position))
                    player2["timers"]["lightning"] = 1.8 * cooldown_factor
                if p2_keys[pygame.K_KP2] and game["unlocked"]["nova"] and player2["timers"]["nova"] <= 0 and game["mana"] >= spell_costs["nova"]:
                    game["mana"] -= spell_costs["nova"]
                    for target in p2_targets:
                        if target.position.distance_to(p2_position) < 115 + target.radius:
                            damage_enemy(target, 55 + player2["damage"])
                    game["magic_effects"].append(MagicEffect("nova", p2_position, radius=115))
                    player2["timers"]["nova"] = 4.5 * cooldown_factor
                if p2_keys[pygame.K_KP3] and game["unlocked"]["meteor"] and player2["timers"]["meteor"] <= 0 and game["mana"] >= spell_costs["meteor"]:
                    game["mana"] -= spell_costs["meteor"]
                    for target in p2_targets:
                        if target.position.distance_to(p2_target_position) < 105 + target.radius:
                            damage_enemy(target, 130 + player2["damage"])
                    game["magic_effects"].append(MagicEffect("nova", p2_target_position, radius=105))
                    player2["timers"]["meteor"] = 8 * cooldown_factor
                if p2_keys[pygame.K_KP4] and game["unlocked"]["frost"] and player2["timers"]["frost"] <= 0 and game["mana"] >= spell_costs["frost"]:
                    game["mana"] -= spell_costs["frost"]
                    for target in p2_targets:
                        if target.position.distance_to(p2_target_position) < 135 + target.radius:
                            damage_enemy(target, 65 + player2["damage"])
                    game["magic_effects"].append(MagicEffect("nova", p2_target_position, radius=135))
                    player2["timers"]["frost"] = 6 * cooldown_factor


            if game["equipment"]["bow"] and keys[pygame.K_b] and game["arrow_timer"] <= 0:
                bow_target = player_target.position if player_target else player + pygame.Vector2(1, 0)
                game["arrows"].append(Arrow(player, bow_target))
                game["arrow_timer"] = 0.3


            if not active_bosses(game):
                target = 8 + game["wave"] * 5
                if game["spawned"] < target:
                    game["spawn_timer"] -= dt
                    if game["spawn_timer"] <= 0:
                        kinds = ["stalker"] * 5 + ["brute"]
                        if game["wave"] >= 3:
                            kinds += ["charger"]
                        if game["wave"] >= 4:
                            kinds += ["spitter"]
                        if game["wave"] >= 6:
                            kinds += ["wisp"]
                        if game["wave"] >= 5:
                            kinds += ["bomber", "sniper"]
                        if game["wave"] >= 7:
                            kinds += ["guardian"]
                        if game["wave"] >= 9:
                            kinds += ["hexer"] * 2
                        if game["wave"] >= 10:
                            kinds += EXTRA_ENEMIES[:8]
                        if game["wave"] >= 15:
                            kinds += EXTRA_ENEMIES[8:16]
                        if game["wave"] >= 18:
                            kinds += EXTRA_ENEMIES[16:]
                        kind = random.choice(kinds)
                        game["enemies"].append(Enemy(kind, game["wave"]))
                        game["spawned"] += 1
                        game["spawn_timer"] = max(0.28, 0.85 - game["wave"] * 0.07)
                elif not game["enemies"]:
                    game["wave_break"] -= dt
                    if game["wave_break"] <= 0 and game["wave"] in BOSS_WAVES:
                        boss_count = 3 if game["wave"] in (12, 20, 32, 40) else 2 if game["wave"] in (8, 16, 24, 36) else 1
                        game["bosses"] = [Boss(game["wave"]) for _ in range(boss_count)]
                        game["boss"] = game["bosses"][0]
                        game["wave_break"] = 0
                    elif game["wave_break"] <= 0:
                        open_shop(game)
                        state = "shop"


            for fireball in game["fireballs"][:]:
                fireball.update(dt)
                if fireball.life <= 0:
                    game["fireballs"].remove(fireball)
                    continue
                targets = game["enemies"] + active_bosses(game)
                for target in targets:
                    if target and fireball.position.distance_to(target.position) < fireball.radius + target.radius:
                        if reflect_projectile(target, fireball):
                            continue
                        damage_enemy(target, 24 + game["upgrades"]["damage"] + game["upgrades"]["spell"])
                        target.hit_flash = 0.08
                        game["fireballs"].remove(fireball)
                        for _ in range(7):
                            game["particles"].append(Particle(fireball.position, GOLD, 110, 0.4, 5))
                        break


            for arrow in game["arrows"][:]:
                arrow.update(dt)
                if arrow.life <= 0 or not ARENA.inflate(100, 100).collidepoint(arrow.position):
                    game["arrows"].remove(arrow)
                    continue
                targets = game["enemies"] + active_bosses(game)
                for target in targets:
                    if target and arrow.position.distance_to(target.position) < arrow.radius + target.radius:
                        if reflect_projectile(target, arrow):
                            continue
                        damage_enemy(target, 48 + game["upgrades"]["damage"])
                        target.hit_flash = 0.1
                        game["arrows"].remove(arrow)
                        break


            for enemy in game["enemies"][:]:
                enemy.update(type("Player", (), {"position": player})(), dt, game["enemy_shots"])
                if enemy.position.distance_to(player) < enemy.radius + 15:
                    damage_player(game, (18 if enemy.kind == "stalker" else 28) * dt)
                if enemy.health <= 0 and enemy in game["enemies"]:
                    game["enemies"].remove(enemy)
                    game["kills"] += 1
                    award_xp(game, 24 + game["wave"] * 3, 7 + game["wave"])
                    for _ in range(12):
                        game["particles"].append(Particle(enemy.position, (202, 83, 207), 150, 0.6, 5))


            for shot in game["enemy_shots"][:]:
                shot.update(dt)
                if shot.life <= 0 or not ARENA.inflate(100, 100).collidepoint(shot.position):
                    game["enemy_shots"].remove(shot)
                elif shot.position.distance_to(player) < 18:
                    damage_player(game, 16)
                    game["enemy_shots"].remove(shot)


            if active_bosses(game):
                boss_reward_count = len(active_bosses(game))
                for boss in active_bosses(game):
                    boss.update(type("Player", (), {"position": player})(), dt, game["particles"], game["enemy_shots"], game["wave_attacks"], game["enemies"])
                    if boss.position.distance_to(player) < boss.radius + 15:
                        damage_player(game, 34 * dt)
                for attack in game["wave_attacks"][:]:
                    attack.update(dt)
                    if attack.position.distance_to(player) > 1200 or attack.life <= 0:
                        game["wave_attacks"].remove(attack)
                    elif attack.position.distance_to(player) < 24:
                        damage_player(game, (36 if isinstance(attack, PinAttack) and attack.active else 22) * dt)
                    if game["coop"] and attack.position.distance_to(player2["position"]) < 24:
                        damage_player_two(player2, (36 if isinstance(attack, PinAttack) and attack.active else 22) * dt)
                    if isinstance(attack, BossField):
                        if attack.position.distance_to(player) < attack.radius:
                            damage_player(game, (20 + game["wave"] * 2) * dt)
                        for enemy in game["enemies"]:
                            if attack.position.distance_to(enemy.position) < attack.radius:
                                enemy.slow_timer = 0.3
                        if game["coop"] and attack.position.distance_to(player2["position"]) < attack.radius:
                            damage_player_two(player2, (20 + game["wave"] * 2) * dt)
                game["bosses"] = [boss for boss in game["bosses"] if boss.health > 0]
                game["boss"] = game["bosses"][0] if game["bosses"] else None
                if not game["bosses"]:
                    if game["wave"] == TOTAL_WAVES:
                        game["state"] = "won"
                        state = "won"
                    else:
                        award_xp(game, 180 * boss_reward_count + game["wave"] * 10, 60 * boss_reward_count + game["wave"] * 5)
                        game["wave_break"] = 0
                        open_shop(game)
                        state = "shop"


            for particle in game["particles"][:]:
                particle.update(dt)
                if particle.life <= 0:
                    game["particles"].remove(particle)
            for effect in game["magic_effects"][:]:
                effect.update(dt)
                if effect.life <= 0:
                    game["magic_effects"].remove(effect)
            for slash in game["slash_effects"][:]:
                slash.update(dt)
                if slash.life <= 0:
                    game["slash_effects"].remove(slash)
            if game["health"] <= 0 or (game["coop"] and player2["health"] <= 0):
                if not respawn_at_checkpoint(game):
                    state = "lost"


        screen.fill(BG)
        for x in range(0, WIDTH, 48):
            pygame.draw.line(screen, (13, 20, 34), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 48):
            pygame.draw.line(screen, (13, 20, 34), (0, y), (WIDTH, y), 1)
        pygame.draw.rect(screen, (17, 21, 32), (0, 0, WIDTH, 72))
        pygame.draw.line(screen, (74, 100, 111), (0, 71), (WIDTH, 71), 2)
        pygame.draw.rect(screen, (34, 45, 72), ARENA, 2, border_radius=8)
        pygame.draw.rect(screen, (11, 15, 26), ARENA.inflate(-10, -10), 1, border_radius=6)
        for obstacle in OBSTACLES:
            pygame.draw.rect(screen, (40, 55, 72), obstacle, border_radius=5)
            pygame.draw.rect(screen, (74, 100, 111), obstacle, 2, border_radius=5)
        draw_text(screen, title_font, "CINZAS DA FOICE", (28, 11), GOLD)
        draw_text(screen, small_font, "SOBREVIVA A 40 ONDAS", (30, 48), MUTED)
        draw_text(screen, font, f"WAVE {game['wave']} / {TOTAL_WAVES}", (WIDTH - 170, 12), WHITE)
        draw_text(screen, small_font, f"ABATES {game['kills']}  OURO {game['gold']}", (WIDTH - 170, 39), GOLD)
        draw_text(screen, small_font, f"VIDAS {game['lives']}", (WIDTH - 320, 39), RED)
        spells = "Q RELAMPAGO"
        spells += "  E NOVA" if game["unlocked"]["nova"] else "  E BLOQUEADA"
        spells += "  R METEORO" if game["unlocked"]["meteor"] else "  R BLOQUEADO"
        spells += "  F GELO" if game["unlocked"]["frost"] else "  F BLOQUEADO"
        draw_text(screen, small_font, spells, (405, 18), CYAN)
        draw_text(screen, small_font, f"NIVEL {game['level']}  XP {game['xp']}/{game['xp_next']}  PONTOS {game['skill_points']}", (500, 43), WHITE)
        health_bar = pygame.Rect(245, 24, 220, 17)
        pygame.draw.rect(screen, (50, 29, 51), health_bar, border_radius=7)
        pygame.draw.rect(screen, RED, (health_bar.x, health_bar.y, health_bar.width * max(0, game["health"]) / game["max_health"], health_bar.height), border_radius=7)
        draw_text(screen, small_font, f"VIDA {max(0, int(game['health']))}/{game['max_health']}  ESCUDO {int(game['shield'])}", (health_bar.x + 8, health_bar.y + 1), WHITE)
        draw_text(screen, small_font, f"MANA {int(game['mana'])}/{game['max_mana']}", (245, 48), MANA)
        if game["coop"]:
            draw_text(screen, small_font, f"P2 VIDA {max(0, int(player2['health']))}/{player2['max_health']}  ESCUDO {int(player2['shield'])}", (245, 4), (126, 178, 255))


        for particle in game["particles"]:
            particle.draw(screen)
        for attack in game["wave_attacks"]:
            attack.draw(screen)
        for effect in game["magic_effects"]:
            effect.draw(screen)
        for slash in game["slash_effects"]:
            slash.draw(screen)
        for fireball in game["fireballs"]:
            fireball.draw(screen)
        for arrow in game["arrows"]:
            arrow.draw(screen)
        for shot in game["enemy_shots"]:
            shot.draw(screen)
        for enemy in game["enemies"]:
            enemy.draw(screen)
        if active_bosses(game):
            for boss in active_bosses(game):
                boss.draw(screen)
            draw_text(screen, small_font, " + ".join(boss.kind for boss in active_bosses(game)), (WIDTH // 2, 73), RED, True)
        armor_colors = {"none": WHITE, "ashes": (174, 189, 198), "red_cuirass": (201, 44, 55), "titan": (219, 164, 53)}
        armor_color = armor_colors[game["equipment"]["armor"]]
        pygame.draw.ellipse(screen, (24, 28, 39), (player.x - 19, player.y - 13, 38, 34))
        pygame.draw.polygon(screen, armor_color, [(player.x - 14, player.y - 7), (player.x - 8, player.y - 18), (player.x, player.y - 13), (player.x + 8, player.y - 18), (player.x + 14, player.y - 7), (player.x + 10, player.y + 11), (player.x, player.y + 16), (player.x - 10, player.y + 11)])
        if game["equipment"]["armor"] != "none":
            pygame.draw.line(screen, WHITE, (player.x - 12, player.y + 3), (player.x + 12, player.y + 3), 3)
            pygame.draw.circle(screen, armor_color, (int(player.x), int(player.y - 16)), 8, 2)
        pygame.draw.circle(screen, BG, (int(player.x - 5), int(player.y - 3)), 3)
        pygame.draw.circle(screen, BG, (int(player.x + 5), int(player.y - 3)), 3)
        if game["shield"] > 0:
            pygame.draw.circle(screen, CYAN, player, 24, 2)
        target = nearest_target(game, player)
        aim = (target.position - player) if target else pygame.Vector2(1, 0)
        if game["equipment"]["weapon"] == "bow":
            pygame.draw.arc(screen, GOLD, (player.x - 25, player.y - 16, 25, 32), -1.3, 1.3, 3)
        elif game["equipment"]["weapon"] == "war_axe":
            pygame.draw.line(screen, (116, 75, 43), player, player + aim.normalize() * 34 if aim.length_squared() else player + (30, 0), 4)
        if aim.length_squared():
            pygame.draw.line(screen, WHITE, player, player + aim.normalize() * 28, 3)


        if game["coop"]:
            p2_position = player2["position"]
            p2_armor_colors = {"none": (126, 178, 255), "ashes": (174, 189, 198), "red_cuirass": (201, 44, 55), "titan": (219, 164, 53)}
            p2_color = p2_armor_colors[player2["equipment"]["armor"]]
            pygame.draw.ellipse(screen, (20, 28, 48), (p2_position.x - 19, p2_position.y - 13, 38, 34))
            pygame.draw.polygon(screen, p2_color, [(p2_position.x - 14, p2_position.y - 7), (p2_position.x - 8, p2_position.y - 18), (p2_position.x, p2_position.y - 13), (p2_position.x + 8, p2_position.y - 18), (p2_position.x + 14, p2_position.y - 7), (p2_position.x + 10, p2_position.y + 11), (p2_position.x, p2_position.y + 16), (p2_position.x - 10, p2_position.y + 11)])
            pygame.draw.circle(screen, (126, 178, 255), (int(p2_position.x - 5), int(p2_position.y - 3)), 3)
            pygame.draw.circle(screen, (126, 178, 255), (int(p2_position.x + 5), int(p2_position.y - 3)), 3)
            if player2["equipment"]["armor"] != "none":
                pygame.draw.line(screen, WHITE, (p2_position.x - 12, p2_position.y + 3), (p2_position.x + 12, p2_position.y + 3), 3)
            if player2["shield"] > 0:
                pygame.draw.circle(screen, (126, 178, 255), p2_position, 24, 2)
            p2_target = nearest_target(game, p2_position)
            p2_aim = (p2_target.position - p2_position) if p2_target else pygame.Vector2(1, 0)
            if player2["equipment"]["weapon"] == "bow":
                pygame.draw.arc(screen, GOLD, (p2_position.x - 25, p2_position.y - 16, 25, 32), -1.3, 1.3, 3)
            if p2_aim.length_squared():
                pygame.draw.line(screen, (126, 178, 255), p2_position, p2_position + p2_aim.normalize() * 28, 3)


        if game["wave_break"] > 0 and not game["enemies"] and game["wave"] < TOTAL_WAVES and game["spawned"] > 0:
            draw_text(screen, font, f"WAVE {game['wave']} CONCLUIDA", (WIDTH // 2, HEIGHT // 2 - 20), GOLD, True)
        if state == "upgrade":
            pygame.draw.rect(screen, (8, 11, 23), (90, 105, WIDTH - 180, HEIGHT - 170), border_radius=10)
            draw_text(screen, title_font, "ESCOLHA UM UPGRADE", (WIDTH // 2, 150), GOLD, True)
            draw_text(screen, small_font, "Pressione a tecla correspondente para continuar", (WIDTH // 2, 184), MUTED, True)
            for index, option in enumerate(game["upgrade_options"]):
                y = 245 + index * 75
                draw_text(screen, font, f"[{option[0]}]  {option[1]}", (170, y), CYAN)
                draw_text(screen, small_font, option[2], (205, y + 29), WHITE)
        if state == "shop":
            market_panel = pygame.Rect(72, 82, WIDTH - 144, HEIGHT - 112)
            pygame.draw.rect(screen, (7, 11, 20), market_panel, border_radius=12)
            pygame.draw.rect(screen, (48, 61, 83), market_panel, 2, border_radius=12)
            pygame.draw.line(screen, GOLD, (market_panel.left + 24, 184), (market_panel.right - 24, 184), 2)
            draw_text(screen, title_font, "MERCADO DAS CINZAS", (WIDTH // 2, 119), GOLD, True)
            draw_text(screen, small_font, "EQUIPAMENTOS E RELIQUIAS PARA A PROXIMA ONDA", (WIDTH // 2, 151), MUTED, True)
            pygame.draw.rect(screen, (55, 43, 30), (market_panel.right - 245, 101, 205, 38), border_radius=7)
            draw_text(screen, font, f"OURO  {game['gold']}", (market_panel.right - 225, 109), GOLD)
            draw_text(screen, small_font, "[K] HABILIDADES   [S] PROXIMA WAVE", (market_panel.left + 24, 166), CYAN)
            for index, option in enumerate(game["shop_options"]):
                column = index // 5
                row = index % 5
                card = pygame.Rect(105 + column * 382, 198 + row * 62, 350, 54)
                color = WHITE
                if (option[0] == "4" and game["unlocked"]["nova"]) or (option[0] == "8" and game["unlocked"]["meteor"]) or (option[0] == "0" and game["unlocked"]["frost"]):
                    color = MUTED
                card_color = (25, 31, 45) if color != MUTED else (20, 24, 34)
                pygame.draw.rect(screen, card_color, card, border_radius=7)
                pygame.draw.rect(screen, (61, 78, 103) if color != MUTED else (42, 48, 61), card, 1, border_radius=7)
                pygame.draw.circle(screen, GOLD if color != MUTED else (91, 94, 98), (card.left + 23, card.centery), 13, 2)
                draw_text(screen, font, option[0], (card.left + 18, card.top + 14), GOLD if color != MUTED else MUTED)
                draw_text(screen, small_font, option[1], (card.left + 47, card.top + 7), color)
                draw_text(screen, small_font, option[2], (card.left + 47, card.top + 29), MUTED if color == MUTED else WHITE)
        if state == "skills":
            pygame.draw.rect(screen, (8, 11, 23), (125, 105, WIDTH - 250, HEIGHT - 175), border_radius=10)
            draw_text(screen, title_font, "ARVORE DE HABILIDADES", (WIDTH // 2, 145), GOLD, True)
            draw_text(screen, font, f"PONTOS DISPONIVEIS: {game['skill_points']}     [B] VOLTAR", (WIDTH // 2, 180), CYAN, True)
            skill_options = [
                "[1] FORCA: +6 dano por ponto",
                "[2] VITALIDADE: +15 vida maxima por ponto",
                "[3] REGENERACAO: +1 vida por segundo",
                "[4] ARMADURA: -4 dano recebido",
                "[5] ARCANO: +1 dano em cada magia",
                "[6] PRECISAO: +3 dano na espada",
            ]
            for index, text in enumerate(skill_options):
                draw_text(screen, font, text, (220, 250 + index * 55), WHITE)
        if state in ("lost", "won"):
            pygame.draw.rect(screen, (8, 11, 23), (0, 0, WIDTH, HEIGHT), 0)
            headline = "O PECADOR SOMBRIO FOI DERROTADO" if state == "won" else "SUA CHAMA SE APAGOU"
            color = GOLD if state == "won" else RED
            draw_text(screen, title_font, headline, (WIDTH // 2, HEIGHT // 2 - 48), color, True)
            draw_text(screen, font, "PRESSIONE ENTER PARA JOGAR NOVAMENTE", (WIDTH // 2, HEIGHT // 2 + 20), WHITE, True)
        pygame.display.flip()


    pygame.quit()




if __name__ == "__main__":
    main()
