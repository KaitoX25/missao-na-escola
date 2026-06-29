import pygame
import math
import random
from config import TEACHER_META, SCALE, to_screen

TEACHER_RADIUS = 14   # px colisão

SKIN   = (235, 190, 145)
SKIN_D = (195, 150, 110)


def _shadow(surf, cx, cy, r):
    s = pygame.Surface((r * 2 + 10, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 50), s.get_rect())
    surf.blit(s, (cx - r - 5, cy + r - 4))


def _label(surf, font, text, cx, cy, cor=(255,255,255)):
    for ox, oy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        surf.blit(font.render(text, True, (0,0,0)), (cx+ox, cy+oy))
    surf.blit(font.render(text, True, cor), (cx, cy))


# ── Skinner — Diretor ─────────────────────────────────────────
def _draw_skinner(surf, cx, cy, ang, r, anim_t):
    perp = ang + math.pi / 2
    fx, fy = math.cos(ang), math.sin(ang)

    _shadow(surf, cx, cy, r)

    # Sapatos
    phase = math.sin(anim_t) * 3
    for side in [-1, 1]:
        sx = int(cx + math.cos(perp) * side * (r - 6) + fx * phase * side)
        sy = int(cy + math.sin(perp) * side * (r - 6) + fy * phase * side)
        pygame.draw.ellipse(surf, (30, 25, 20), pygame.Rect(sx - 5, sy - 3, 10, 6))

    # Corpo: terno azul-marinho
    pygame.draw.circle(surf, (30, 55, 110), (cx, cy), r)
    pygame.draw.circle(surf, (15, 35, 80),  (cx, cy), r, 2)

    # Gravata vermelha
    tie_pts = [
        (int(cx + math.cos(perp) * 2),  int(cy + math.sin(perp) * 2)),
        (int(cx - math.cos(perp) * 2),  int(cy - math.sin(perp) * 2)),
        (int(cx + fx * (r - 6)),        int(cy + fy * (r - 6))),
    ]
    pygame.draw.polygon(surf, (185, 20, 20), tie_pts)

    # Cabeça: careca
    hx = int(cx + fx * (r - 5))
    hy = int(cy + fy * (r - 5))
    hr = 10
    pygame.draw.circle(surf, SKIN_D, (hx, hy), hr + 1)
    pygame.draw.circle(surf, SKIN,   (hx, hy), hr)

    # Reflexo de careca (oval brilhante)
    shine_x = int(hx + math.cos(ang + math.pi) * 3)
    shine_y = int(hy + math.sin(ang + math.pi) * 3)
    pygame.draw.ellipse(surf, (255, 230, 210),
                        pygame.Rect(shine_x - 4, shine_y - 3, 8, 5))

    # Óculos
    for side in [-1, 1]:
        gx = int(hx + math.cos(perp) * side * 3 + fx * 4)
        gy = int(hy + math.sin(perp) * side * 3 + fy * 4)
        pygame.draw.circle(surf, (180, 180, 220), (gx, gy), 3)
        pygame.draw.circle(surf, (180, 180, 220), (gx, gy), 3, 1)
        pygame.draw.circle(surf, (50, 50, 70),    (gx, gy), 1)
    # ponte dos óculos
    g1x = int(hx + math.cos(perp) * (-3) + fx * 4)
    g1y = int(hy + math.sin(perp) * (-3) + fy * 4)
    g2x = int(hx + math.cos(perp) * 3  + fx * 4)
    g2y = int(hy + math.sin(perp) * 3  + fy * 4)
    pygame.draw.line(surf, (180, 180, 220), (g1x, g1y), (g2x, g2y), 1)

    # Sobrancelhas carrancudas
    for side in [-1, 1]:
        bx = int(hx + math.cos(perp) * side * 3 + fx * 2)
        by = int(hy + math.sin(perp) * side * 3 + fy * 2)
        ex = int(bx + math.cos(perp) * side * 2 + fx)
        ey = int(by + math.sin(perp) * side * 2 + fy)
        pygame.draw.line(surf, (60, 40, 20), (bx, by), (ex, ey), 2)

    # Boca franzida
    mx = int(hx + fx * 3)
    my = int(hy + fy * 3)
    pygame.draw.arc(surf, (130, 70, 50),
                    pygame.Rect(mx - 4, my - 2, 8, 5),
                    0, math.pi, 1)


# ── Krabappel — Professora ────────────────────────────────────
def _draw_krabappel(surf, cx, cy, ang, r, anim_t):
    perp = ang + math.pi / 2
    fx, fy = math.cos(ang), math.sin(ang)

    _shadow(surf, cx, cy, r)

    # Sapatos femininos
    phase = math.sin(anim_t) * 3
    for side in [-1, 1]:
        sx = int(cx + math.cos(perp) * side * (r - 6) + fx * phase * side)
        sy = int(cy + math.sin(perp) * side * (r - 6) + fy * phase * side)
        pygame.draw.ellipse(surf, (100, 40, 40), pygame.Rect(sx - 4, sy - 3, 9, 6))

    # Corpo: vestido laranja-rosado
    pygame.draw.circle(surf, (205, 95, 65), (cx, cy), r)
    pygame.draw.circle(surf, (165, 65, 40), (cx, cy), r, 2)

    # Detalhes do vestido (botões)
    for i in range(3):
        bx = int(cx + fx * (r - 8 - i * 4))
        by = int(cy + fy * (r - 8 - i * 4))
        pygame.draw.circle(surf, (240, 220, 200), (bx, by), 2)

    # Cabeça
    hx = int(cx + fx * (r - 5))
    hy = int(cy + fy * (r - 5))
    hr = 10
    pygame.draw.circle(surf, SKIN_D, (hx, hy), hr + 1)
    pygame.draw.circle(surf, SKIN,   (hx, hy), hr)

    # Cabelo vermelho cacheado (grande e redondo)
    hair_r = hr + 5
    pygame.draw.circle(surf, (175, 35, 25), (hx, hy), hair_r)
    # Textura ondulada
    for i in range(6):
        ha = ang + math.pi + math.pi * i / 3
        hpx = int(hx + math.cos(ha) * (hair_r - 2))
        hpy = int(hy + math.sin(ha) * (hair_r - 2))
        pygame.draw.circle(surf, (195, 55, 40), (hpx, hpy), 4)
    # Rosto por cima do cabelo
    pygame.draw.circle(surf, SKIN, (hx, hy), hr)

    # Óculos redondos
    for side in [-1, 1]:
        gx = int(hx + math.cos(perp) * side * 3 + fx * 4)
        gy = int(hy + math.sin(perp) * side * 3 + fy * 4)
        pygame.draw.circle(surf, (50, 30, 30), (gx, gy), 3)
        pygame.draw.circle(surf, (50, 30, 30), (gx, gy), 3, 1)
        pygame.draw.circle(surf, (50, 50, 100), (gx, gy), 1)

    # Sorriso levemente sarcástico
    mx = int(hx + fx * 3)
    my = int(hy + fy * 3)
    pygame.draw.arc(surf, (140, 80, 60),
                    pygame.Rect(mx - 4, my - 3, 8, 6),
                    math.pi, math.pi * 2, 1)


# ── Chalmers — Superintendente ────────────────────────────────
def _draw_chalmers(surf, cx, cy, ang, r, anim_t):
    perp = ang + math.pi / 2
    fx, fy = math.cos(ang), math.sin(ang)

    _shadow(surf, cx, cy, r)

    # Sapatos
    phase = math.sin(anim_t) * 2
    for side in [-1, 1]:
        sx = int(cx + math.cos(perp) * side * (r - 6) + fx * phase * side)
        sy = int(cy + math.sin(perp) * side * (r - 6) + fy * phase * side)
        pygame.draw.ellipse(surf, (20, 15, 10), pygame.Rect(sx - 5, sy - 3, 11, 6))

    # Corpo: terno preto autoritário
    pygame.draw.circle(surf, (38, 38, 50), (cx, cy), r)
    pygame.draw.circle(surf, (20, 20, 30), (cx, cy), r, 2)

    # Abas do terno
    for side in [-1, 1]:
        lx = int(cx + math.cos(perp) * side * (r // 2))
        ly = int(cy + math.sin(perp) * side * (r // 2))
        tx = int(cx + fx * (r - 7))
        ty = int(cy + fy * (r - 7))
        pygame.draw.polygon(surf, (55, 55, 70), [(cx, cy), (lx, ly), (tx, ty)])

    # Gravata fina amarela
    tie_pts = [
        (int(cx + math.cos(perp) * 1.5), int(cy + math.sin(perp) * 1.5)),
        (int(cx - math.cos(perp) * 1.5), int(cy - math.sin(perp) * 1.5)),
        (int(cx + fx * (r - 7)),         int(cy + fy * (r - 7))),
    ]
    pygame.draw.polygon(surf, (200, 170, 30), tie_pts)

    # Cabeça: largo e autoritário
    hx = int(cx + fx * (r - 5))
    hy = int(cy + fy * (r - 5))
    hr = 11
    pygame.draw.circle(surf, SKIN_D, (hx, hy), hr + 1)
    pygame.draw.circle(surf, SKIN,   (hx, hy), hr)

    # Cabelo cinza nas laterais (Chalmers tem pouco cabelo)
    for side in [-1, 1]:
        ghx = int(hx + math.cos(perp) * side * (hr - 1))
        ghy = int(hy + math.sin(perp) * side * (hr - 1))
        pygame.draw.circle(surf, (140, 140, 150), (ghx, ghy), 4)

    # Sobrancelhas grossas e furiosas
    for side in [-1, 1]:
        b1x = int(hx + math.cos(perp) * side * 5 + fx)
        b1y = int(hy + math.sin(perp) * side * 5 + fy)
        b2x = int(hx + math.cos(perp) * side + fx * 3)
        b2y = int(hy + math.sin(perp) * side + fy * 3)
        pygame.draw.line(surf, (50, 35, 20), (b1x, b1y), (b2x, b2y), 3)

    # Olhos (pequenos e assustadores)
    for side in [-1, 1]:
        ex = int(hx + math.cos(perp) * side * 3 + fx * 4)
        ey = int(hy + math.sin(perp) * side * 3 + fy * 4)
        pygame.draw.circle(surf, (30, 20, 10), (ex, ey), 2)

    # Boca fechada/brava
    mx = int(hx + fx * 3)
    my = int(hy + fy * 3)
    pygame.draw.line(surf, (130, 80, 60),
                     (mx - 4, my), (mx + 4, my), 2)


# ── Dispatcher ───────────────────────────────────────────────
_DRAW_FN = {
    "skinner":   _draw_skinner,
    "krabappel": _draw_krabappel,
    "chalmers":  _draw_chalmers,
}


class Professor:
    def __init__(self, dados: dict):
        self.tipo  = dados["tipo"]
        self.meta  = TEACHER_META[self.tipo]
        self.label = self.meta["label"]

        ax, ay = to_screen(*dados["a"])
        bx, by = to_screen(*dados["b"])
        self.patrol_a = (float(ax), float(ay))
        self.patrol_b = (float(bx), float(by))

        self.t        = random.uniform(0, math.pi * 2)
        self.x        = float(ax)
        self.y        = float(ay)
        self.catch_px = self.meta["catch_gu"] * SCALE
        self.anim_t   = 0.0
        self._ang     = math.atan2(
            self.patrol_b[1] - self.patrol_a[1],
            self.patrol_b[0] - self.patrol_a[0]
        )

    def reset(self):
        self.t = random.uniform(0, math.pi * 2)
        self.x, self.y = self.patrol_a
        self.anim_t = 0.0

    def update(self, dt: float, velocidade_base: float):
        speed = velocidade_base * self.meta["speed"]
        self.t += dt * speed * 0.4
        self.anim_t += dt * 8
        fator = (math.sin(self.t) + 1) / 2
        px = self.patrol_a[0] + (self.patrol_b[0] - self.patrol_a[0]) * fator
        py = self.patrol_a[1] + (self.patrol_b[1] - self.patrol_a[1]) * fator

        # Direção do movimento
        dx = px - self.x
        dy = py - self.y
        if abs(dx) > 0.5 or abs(dy) > 0.5:
            self._ang = math.atan2(dy, dx)
        self.x, self.y = px, py

    def _get_ang(self, player_x, player_y):
        """Olha para o jogador."""
        dx = player_x - self.x
        dy = player_y - self.y
        return math.atan2(dy, dx)

    def checa_pegar(self, player_x: float, player_y: float) -> bool:
        return math.hypot(player_x - self.x, player_y - self.y) < self.catch_px

    def draw(self, surf: pygame.Surface, font_small, player_x: float, player_y: float):
        cx, cy = int(self.x), int(self.y)
        ang = self._get_ang(player_x, player_y)
        r   = TEACHER_RADIUS

        # Raio de captura do Chalmers
        if self.tipo == "chalmers":
            rp = int(self.catch_px)
            s  = pygame.Surface((rp * 2 + 6, rp * 2 + 6), pygame.SRCALPHA)
            pygame.draw.circle(s, (44, 62, 80, 22), (rp + 3, rp + 3), rp)
            pygame.draw.circle(s, (133, 146, 158, 65), (rp + 3, rp + 3), rp, 1)
            surf.blit(s, (cx - rp - 3, cy - rp - 3))

        # Desenho específico do professor
        _DRAW_FN[self.tipo](surf, cx, cy, ang, r, self.anim_t)

        # Rótulo com cor da equipe
        cor_label = self.meta["borda"]
        lbl = font_small.render(self.label, True, cor_label)
        _label(surf, font_small, self.label, cx - lbl.get_width() // 2,
               cy - r - lbl.get_height() - 14, cor_label)
