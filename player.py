import pygame
import math
from config import to_screen
from level import WALLS, MAP_BOUNDS

PLAYER_RADIUS = 14   # px colisão
PLAYER_SPEED  = 160  # px/s

SKIN      = (235, 190, 145)
SKIN_SOM  = (195, 150, 110)
HAIR_COL  = (70,  40,  10)
SHIRT_COL = (55,  95,  185)
PANTS_COL = (35,  55,  110)
SHOE_COL  = (35,  30,  25)
PACK_COL  = (160, 80,  20)
PACK_DRK  = (110, 55,  10)


def _resolve_wall(cx, cy, r, rect):
    closest_x = max(rect.left,   min(cx, rect.right))
    closest_y = max(rect.top,    min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    d2 = dx * dx + dy * dy
    if d2 == 0:
        ox = min(cx - rect.left, rect.right - cx)
        oy = min(cy - rect.top,  rect.bottom - cy)
        if ox < oy: cx = rect.left - r if cx < rect.centerx else rect.right + r
        else:       cy = rect.top - r  if cy < rect.centery else rect.bottom + r
    elif d2 < r * r:
        d = math.sqrt(d2)
        cx += dx / d * (r - d)
        cy += dy / d * (r - d)
    return cx, cy


def _shadow(surf, cx, cy, r):
    s = pygame.Surface((r * 2 + 10, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 55), s.get_rect())
    surf.blit(s, (cx - r - 5, cy + r - 4))


def _label(surf, font, text, cx, cy):
    for ox, oy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        surf.blit(font.render(text, True, (0,0,0)), (cx+ox, cy+oy))
    surf.blit(font.render(text, True, (255,255,255)), (cx, cy))


class Player:
    def __init__(self):
        self.x, self.y = map(float, to_screen(0, -10))
        self.facing  = (0.0, 1.0)
        self.radius  = PLAYER_RADIUS
        self.anim_t  = 0.0
        self.moving  = False

    def reset(self):
        self.x, self.y = map(float, to_screen(0, -10))
        self.facing = (0.0, 1.0)
        self.anim_t = 0.0
        self.moving = False

    def update(self, dt: float, keys):
        dx = dy = 0.0
        sp = PLAYER_SPEED * dt
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= 1; self.facing = ( 0.0,-1.0)
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += 1; self.facing = ( 0.0, 1.0)
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= 1; self.facing = (-1.0, 0.0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += 1; self.facing = ( 1.0, 0.0)
        self.moving = dx != 0 or dy != 0
        if self.moving:
            self.anim_t += dt * 10
            if dx != 0 and dy != 0: dx *= 0.7071; dy *= 0.7071
        nx, ny = self.x + dx * sp, self.y + dy * sp
        r = self.radius
        nx = max(MAP_BOUNDS.left + r, min(MAP_BOUNDS.right  - r, nx))
        ny = max(MAP_BOUNDS.top  + r, min(MAP_BOUNDS.bottom - r, ny))
        for _ in range(3):
            for w in WALLS:
                nx, ny = _resolve_wall(nx, ny, r, w)
        self.x, self.y = nx, ny

    def pos(self):
        return int(self.x), int(self.y)

    def draw(self, surf: pygame.Surface, font_small):
        cx, cy = int(self.x), int(self.y)
        r  = self.radius
        fx, fy = self.facing
        ang  = math.atan2(fy, fx)
        perp = ang + math.pi / 2

        # Sombra
        _shadow(surf, cx, cy, r)

        # Mochila (atrás do personagem)
        bx = int(cx - fx * (r - 3))
        by = int(cy - fy * (r - 3))
        pygame.draw.ellipse(surf, PACK_DRK, pygame.Rect(bx - 8, by - 6, 16, 12))
        pygame.draw.ellipse(surf, PACK_COL, pygame.Rect(bx - 7, by - 5, 14, 10))
        # bolso da mochila
        pygame.draw.ellipse(surf, PACK_DRK, pygame.Rect(bx - 4, by - 2, 8, 6))

        # Corpo (camisa)
        pygame.draw.circle(surf, SHIRT_COL, (cx, cy), r)

        # Calças (meia lua oposta ao facing)
        pygame.draw.arc(surf, PANTS_COL,
                        pygame.Rect(cx - r + 1, cy - r + 1, (r - 1) * 2, (r - 1) * 2),
                        ang + math.pi * 0.6, ang + math.pi * 1.4, r - 3)

        # Pés com animação de caminhada
        phase = math.sin(self.anim_t) if self.moving else 0
        for side in [-1, 1]:
            fx2 = math.cos(perp) * side * (r - 6) + math.cos(ang) * phase * side * 4
            fy2 = math.sin(perp) * side * (r - 6) + math.sin(ang) * phase * side * 4
            sx, sy = int(cx + fx2), int(cy + fy2)
            pygame.draw.circle(surf, SHOE_COL, (sx, sy), 4)
            pygame.draw.circle(surf, (60, 55, 50), (sx, sy), 4, 1)

        # Borda da camisa
        pygame.draw.circle(surf, (35, 65, 145), (cx, cy), r, 2)

        # Cabeça (na direção do facing)
        hx = int(cx + fx * (r - 5))
        hy = int(cy + fy * (r - 5))
        hr = 10

        # Pescoço
        pygame.draw.circle(surf, SKIN_SOM, (hx, hy), hr + 1)

        # Pele da cara
        pygame.draw.circle(surf, SKIN, (hx, hy), hr)

        # Cabelo (arco na parte traseira da cabeça)
        h_start = ang + math.pi * 0.55
        h_end   = ang + math.pi * 1.45
        pygame.draw.arc(surf, HAIR_COL,
                        pygame.Rect(hx - hr - 1, hy - hr - 1, (hr + 1) * 2, (hr + 1) * 2),
                        h_start, h_end, 5)
        # franja
        fringe_x = int(hx + math.cos(ang + math.pi) * (hr - 2))
        fringe_y = int(hy + math.sin(ang + math.pi) * (hr - 2))
        pygame.draw.circle(surf, HAIR_COL, (fringe_x, fringe_y), 4)

        # Olhos
        for side in [-1, 1]:
            ex = int(hx + math.cos(perp) * side * 3 + math.cos(ang) * 4)
            ey = int(hy + math.sin(perp) * side * 3 + math.sin(ang) * 4)
            pygame.draw.circle(surf, (255, 255, 255), (ex, ey), 3)
            pygame.draw.circle(surf, (30, 30, 50),   (ex, ey), 1)

        # Sorriso leve
        sm_cx = int(hx + math.cos(ang) * 3)
        sm_cy = int(hy + math.sin(ang) * 3)
        pygame.draw.arc(surf, SKIN_SOM,
                        pygame.Rect(sm_cx - 4, sm_cy - 4, 8, 7),
                        math.pi, math.pi * 2, 1)

        # Rótulo
        lbl = font_small.render("Você", True, (255,255,255))
        _label(surf, font_small, "Você",
               cx - lbl.get_width() // 2, cy - r - lbl.get_height() - 3)
