import pygame
import math
import random
from config import (SCALE, MAP_X, MAP_Y, MAP_PX_W, MAP_PX_H, to_screen)
from level import WALLS

ITEM_RADIUS   = 14
COLLECT_DIST  = 28


def _inside_wall(px, py, margin=14):
    test = pygame.Rect(px - margin, py - margin, margin * 2, margin * 2)
    return any(w.colliderect(test) for w in WALLS)


def _in_bounds(px, py, margin=28):
    return (MAP_X + margin <= px <= MAP_X + MAP_PX_W - margin and
            MAP_Y + margin <= py <= MAP_Y + MAP_PX_H - margin)


def spawn_positions(count, avoid=None, min_dist=52):
    if avoid is None:
        avoid = []
    result = []
    attempts = 0
    while len(result) < count and attempts < 8000:
        attempts += 1
        gx = random.uniform(-17.5, 17.5)
        gz = random.uniform(-13.5, 13.5)
        px, py = to_screen(gx, gz)
        if not _in_bounds(px, py):
            continue
        if _inside_wall(px, py):
            continue
        if any(math.hypot(px - ax, py - ay) < min_dist for ax, ay in avoid + result):
            continue
        result.append((px, py))
    return result


# ── Funções de desenho ────────────────────────────────────────
def _glow(surf, cx, cy, r, color, alpha=60):
    """Aura suave em camadas."""
    for i in range(3):
        gr = r + 10 - i * 3
        s  = pygame.Surface((gr * 2 + 4, gr * 2 + 4), pygame.SRCALPHA)
        a  = alpha // (i + 1)
        pygame.draw.circle(s, (*color, a), (gr + 2, gr + 2), gr)
        surf.blit(s, (cx - gr - 2, cy - gr - 2))


def _shadow_item(surf, cx, cy, r):
    s = pygame.Surface((r * 2 + 4, 8), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 50), s.get_rect())
    surf.blit(s, (cx - r - 2, cy + r - 3))


def _draw_book(surf, cx, cy, bob=0.0):
    cy = int(cy + bob)
    s = 16  # meia-largura
    # Glow
    _glow(surf, cx, cy, s, (41, 128, 185), 50)
    # Sombra
    _shadow_item(surf, cx, cy, s)
    # Capa do livro
    rect = pygame.Rect(cx - s, cy - int(s * 1.1), s * 2, int(s * 2.2))
    pygame.draw.rect(surf, (25, 80, 140), rect, border_radius=3)
    pygame.draw.rect(surf, (41, 128, 185), pygame.Rect(cx - s + 2, cy - int(s * 1.1) + 2,
                                                        s * 2 - 4, int(s * 2.2) - 4), border_radius=2)
    # Lombada
    pygame.draw.rect(surf, (26, 188, 156), pygame.Rect(cx - s + 2, cy - int(s * 1.1),
                                                        6, int(s * 2.2)), border_radius=2)
    # Linhas de texto na capa
    for i in range(3):
        ly = cy - s + 6 + i * 7
        pygame.draw.rect(surf, (180, 220, 255),
                         pygame.Rect(cx - s + 12, ly, s - 4, 3), border_radius=1)
    # Destaque do canto
    pygame.draw.rect(surf, (100, 180, 255),
                     pygame.Rect(cx - s, cy - int(s * 1.1), s * 2, int(s * 2.2)), 1, border_radius=3)


def _draw_mochila(surf, cx, cy, bob=0.0):
    cy = int(cy + bob)
    r = 15
    _glow(surf, cx, cy, r, (39, 174, 96), 50)
    _shadow_item(surf, cx, cy, r)
    # Corpo principal
    pygame.draw.ellipse(surf, (25, 110, 60), pygame.Rect(cx - r, cy - r, r * 2, r * 2 + 4))
    pygame.draw.ellipse(surf, (39, 174, 96), pygame.Rect(cx - r + 1, cy - r + 1, r * 2 - 2, r * 2 + 2))
    # Bolso frontal
    pygame.draw.ellipse(surf, (30, 140, 75), pygame.Rect(cx - 9, cy - 5, 18, 14))
    pygame.draw.ellipse(surf, (55, 185, 100), pygame.Rect(cx - 8, cy - 4, 16, 12))
    # Alças
    pygame.draw.arc(surf, (20, 90, 50),
                    pygame.Rect(cx - 12, cy - r + 2, 10, 14), 0, math.pi, 3)
    pygame.draw.arc(surf, (20, 90, 50),
                    pygame.Rect(cx + 2,  cy - r + 2, 10, 14), 0, math.pi, 3)
    # Brilho
    pygame.draw.ellipse(surf, (130, 230, 160),
                        pygame.Rect(cx - 7, cy - r + 3, 8, 5))


def _draw_chave(surf, cx, cy, bob=0.0):
    cy = int(cy + bob)
    _glow(surf, cx, cy, 13, (212, 172, 13), 55)
    _shadow_item(surf, cx, cy, 13)
    # Cabeça da chave (argola)
    pygame.draw.circle(surf, (160, 120, 5),  (cx - 5, cy - 2), 9)
    pygame.draw.circle(surf, (212, 172, 13), (cx - 5, cy - 2), 7)
    pygame.draw.circle(surf, (160, 120, 5),  (cx - 5, cy - 2), 4)
    pygame.draw.circle(surf, (240, 200, 60), (cx - 5, cy - 2), 4, 1)
    # Haste
    pygame.draw.rect(surf, (180, 140, 10), pygame.Rect(cx + 2, cy - 4, 14, 4), border_radius=2)
    pygame.draw.rect(surf, (212, 172, 13), pygame.Rect(cx + 3, cy - 3, 12, 2))
    # Dentes
    for i in range(2):
        pygame.draw.rect(surf, (180, 140, 10),
                         pygame.Rect(cx + 7 + i * 5, cy, 3, 6), border_radius=1)
    # Brilho
    pygame.draw.circle(surf, (255, 240, 120), (cx - 7, cy - 4), 3)


def _draw_coracao(surf, cx, cy, bob=0.0):
    cy = int(cy + bob)
    r  = 12
    _glow(surf, cx, cy, r, (192, 57, 43), 60)
    _shadow_item(surf, cx, cy, r)
    # Coração com dois círculos + polígono
    pygame.draw.circle(surf, (140, 20, 20), (cx - r // 2, cy - r // 4 + 1), r // 2 + 2)
    pygame.draw.circle(surf, (140, 20, 20), (cx + r // 2, cy - r // 4 + 1), r // 2 + 2)
    pygame.draw.circle(surf, (192, 57, 43), (cx - r // 2, cy - r // 4),     r // 2 + 1)
    pygame.draw.circle(surf, (192, 57, 43), (cx + r // 2, cy - r // 4),     r // 2 + 1)
    pygame.draw.polygon(surf, (192, 57, 43), [
        (cx - r,     cy - r // 4 + 1),
        (cx + r,     cy - r // 4 + 1),
        (cx,         cy + r + 2),
    ])
    # Destaques brancos
    pygame.draw.circle(surf, (255, 120, 120), (cx - r // 2 - 2, cy - r // 4 - 3), 3)
    pygame.draw.circle(surf, (255, 120, 120), (cx + r // 2 - 1, cy - r // 4 - 3), 2)


# ── Classes de itens ──────────────────────────────────────────
class Item:
    def __init__(self, px, py, tipo):
        self.px       = px
        self.py       = py
        self.tipo     = tipo
        self.coletado = False
        self._phase   = random.uniform(0, math.pi * 2)  # fase da animação

    def checar_coleta(self, player_x, player_y):
        if self.coletado:
            return False
        if math.hypot(player_x - self.px, player_y - self.py) < COLLECT_DIST:
            self.coletado = True
            return True
        return False

    def _bob(self, time_ms):
        return math.sin(time_ms / 500 + self._phase) * 2.5


class Livro(Item):
    def __init__(self, px, py):
        super().__init__(px, py, "livro")

    def draw(self, surf, time_ms=0):
        if not self.coletado:
            _draw_book(surf, self.px, self.py, self._bob(time_ms))


class Mochila(Item):
    def __init__(self, px, py):
        super().__init__(px, py, "mochila")

    def draw(self, surf, time_ms=0):
        if not self.coletado:
            _draw_mochila(surf, self.px, self.py, self._bob(time_ms))


class Chave(Item):
    def __init__(self, px, py):
        super().__init__(px, py, "chave")

    def draw(self, surf, time_ms=0):
        if not self.coletado:
            _draw_chave(surf, self.px, self.py, self._bob(time_ms))


class Coracao(Item):
    def __init__(self, px, py):
        super().__init__(px, py, "coracao")

    def draw(self, surf, time_ms=0):
        if not self.coletado:
            _draw_coracao(surf, self.px, self.py, self._bob(time_ms))


def criar_itens_fase(fase):
    from config import FASE_CFG
    cfg = FASE_CFG[fase - 1]
    livros_pos   = spawn_positions(cfg["livros"])
    mochilas_pos = spawn_positions(cfg["mochilas"],  livros_pos)
    chaves_pos   = spawn_positions(cfg["chaves"],    livros_pos + mochilas_pos)
    coracoes_pos = spawn_positions(cfg["coracoes"],  livros_pos + mochilas_pos + chaves_pos)
    return {
        "livros":   [Livro(px, py)   for px, py in livros_pos],
        "mochilas": [Mochila(px, py) for px, py in mochilas_pos],
        "chaves":   [Chave(px, py)   for px, py in chaves_pos],
        "coracoes": [Coracao(px, py) for px, py in coracoes_pos],
    }
