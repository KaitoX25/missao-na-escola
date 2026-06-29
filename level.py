import pygame
import math
from config import (MAP_X, MAP_Y, MAP_PX_W, MAP_PX_H, SCALE,
                    ROOM_COLORS, C_WALL, C_MAP_BORDER, to_screen)

# ── Salas ─────────────────────────────────────────────────────
ROOMS_DEF = [
    {"cx": -13, "cz": -10, "w": 13, "d": 10, "nome": "Sala 1",
     "tipo": "classroom"},
    {"cx":   0, "cz": -10, "w": 14, "d": 10, "nome": "Corredor",
     "tipo": "hallway"},
    {"cx":  13, "cz": -10, "w": 13, "d": 10, "nome": "Biblioteca",
     "tipo": "library"},
    {"cx":  -9, "cz":   0, "w": 22, "d": 10, "nome": "Pátio",
     "tipo": "patio"},
    {"cx":  10, "cz":   0, "w": 18, "d": 10, "nome": "Cantina",
     "tipo": "cafeteria"},
    {"cx":  -9, "cz":  10, "w": 22, "d": 10, "nome": "Laboratório",
     "tipo": "lab"},
    {"cx":  10, "cz":  10, "w": 19, "d": 10, "nome": "Sala dos Profs.",
     "tipo": "staffroom"},
]

def _wall_rect(cx, cz, w, d):
    px, py = to_screen(cx - w / 2, cz - d / 2)
    return pygame.Rect(px, py, int(w * SCALE), int(d * SCALE))

_WALL_DEFS = [
    (   0, -14.5, 40, 1), (   0, 14.5, 40, 1),
    (-19.5,    0,  1,30), ( 19.5,  0,  1,30),
    (-17,   -5,  6, 1),   (-6.5, -5, 11, 1),   (10.5, -5, 19, 1),
    (-15,    5, 10, 1),   ( 0.5,  5, 17, 1),   (15.5,  5,  9, 1),
    (-7, -13,  1,  4),    (-7,   -7,  1, 4),
    ( 7, -13,  1,  4),    ( 7,   -7,  1, 4),
    ( 2,  -3,  1,  4),    ( 2,    3,  1, 4),
    ( 1,   7,  1,  4),    ( 1,   13,  1, 4),
]
WALLS  = [_wall_rect(*d) for d in _WALL_DEFS]
MAP_BOUNDS = pygame.Rect(MAP_X, MAP_Y, MAP_PX_W, MAP_PX_H)


# ── Mobília e decorações por sala ─────────────────────────────
def _room_rect(r):
    rx, ry = to_screen(r["cx"] - r["w"] / 2, r["cz"] - r["d"] / 2)
    return pygame.Rect(rx, ry, int(r["w"] * SCALE), int(r["d"] * SCALE))


def _draw_classroom(surf, rect, cor):
    """Fileiras de carteiras + quadro negro."""
    # Quadro no topo
    pygame.draw.rect(surf, (80, 115, 80),
                     pygame.Rect(rect.left + 20, rect.top + 8, rect.width - 40, 18),
                     border_radius=3)
    pygame.draw.rect(surf, (120, 160, 115),
                     pygame.Rect(rect.left + 22, rect.top + 10, rect.width - 44, 14),
                     border_radius=2)
    pygame.draw.rect(surf, (160, 120, 60),
                     pygame.Rect(rect.left + 20, rect.top + 26, rect.width - 40, 5))

    # Carteiras em grade
    desk_col = (180, 140, 90)
    desk_drk = (140, 100, 60)
    for row in range(2):
        for col in range(3):
            dx = rect.left + 40 + col * 55
            dy = rect.top  + 55 + row * 55
            pygame.draw.rect(surf, desk_drk, pygame.Rect(dx, dy, 36, 28), border_radius=3)
            pygame.draw.rect(surf, desk_col, pygame.Rect(dx + 1, dy + 1, 34, 26), border_radius=3)
            # Livro na carteira
            pygame.draw.rect(surf, (70, 130, 200),
                             pygame.Rect(dx + 10, dy + 8, 14, 10), border_radius=1)


def _draw_hallway(surf, rect, cor):
    """Corredor: armários e lixeira."""
    # Armários (lockers)
    locker_col = (120, 120, 135)
    locker_lne = (90, 90, 105)
    for i in range(8):
        lx = rect.left + 15 + i * 31
        if lx + 26 > rect.right - 10:
            break
        ly = rect.top + 10
        pygame.draw.rect(surf, locker_col, pygame.Rect(lx, ly, 26, 32), border_radius=2)
        pygame.draw.rect(surf, locker_lne, pygame.Rect(lx, ly, 26, 32), 1, border_radius=2)
        # maçaneta
        pygame.draw.circle(surf, (200, 200, 210), (lx + 20, ly + 16), 3)

    # Lixeira
    pygame.draw.rect(surf, (90, 90, 100),
                     pygame.Rect(rect.right - 30, rect.top + 12, 16, 22), border_radius=3)
    pygame.draw.rect(surf, (110, 110, 120),
                     pygame.Rect(rect.right - 29, rect.top + 13, 14, 5))


def _draw_library(surf, rect, cor):
    """Biblioteca: prateleiras de livros + mesas."""
    shelf_col = (120, 85, 45)
    book_cols = [(180,50,50),(50,150,200),(80,160,80),(200,150,50),(120,50,180)]

    # Prateleiras nas bordas
    for side in range(2):
        for row in range(3):
            sx = rect.left + 10 if side == 0 else rect.right - 45
            sy = rect.top + 20 + row * 50
            pygame.draw.rect(surf, shelf_col, pygame.Rect(sx, sy, 35, 40), border_radius=2)
            # Livros na prateleira
            for bi, bc in enumerate(book_cols[:4]):
                bx = sx + 3 + bi * 8
                pygame.draw.rect(surf, bc, pygame.Rect(bx, sy + 4, 7, 32))

    # Mesas de leitura
    for i in range(2):
        tx = rect.centerx - 20 + i * 10
        ty = rect.top + 40 + i * 60
        pygame.draw.ellipse(surf, (160, 115, 70),
                            pygame.Rect(tx - 20, ty - 12, 40, 25))
        pygame.draw.ellipse(surf, (180, 135, 90),
                            pygame.Rect(tx - 18, ty - 10, 36, 21))


def _draw_patio(surf, rect, cor):
    """Pátio: árvores + bancos."""
    # Árvores (círculos verdes)
    trees = [
        (rect.left + 40, rect.top + 40),
        (rect.left + 40, rect.bottom - 50),
        (rect.right - 50, rect.top + 40),
        (rect.right - 50, rect.bottom - 50),
        (rect.centerx, rect.centery),
    ]
    for tx, ty in trees:
        # Tronco
        pygame.draw.circle(surf, (100, 70, 30), (tx, ty), 8)
        # Copa
        pygame.draw.circle(surf, (40, 130, 50), (tx, ty - 3), 14)
        pygame.draw.circle(surf, (60, 155, 70), (tx - 4, ty - 5), 10)
        pygame.draw.circle(surf, (80, 175, 80), (tx + 3, ty - 7), 8)

    # Bancos
    bench_col = (140, 100, 55)
    for i in range(2):
        bx = rect.left + 90 + i * 120
        by = rect.centery - 8
        pygame.draw.rect(surf, bench_col, pygame.Rect(bx, by, 50, 12), border_radius=4)
        pygame.draw.rect(surf, bench_col, pygame.Rect(bx + 5,  by + 12, 8, 10))
        pygame.draw.rect(surf, bench_col, pygame.Rect(bx + 37, by + 12, 8, 10))


def _draw_cafeteria(surf, rect, cor):
    """Cantina: mesas redondas + balcão."""
    # Balcão de comida
    pygame.draw.rect(surf, (160, 120, 80),
                     pygame.Rect(rect.left + 10, rect.top + 10, rect.width - 20, 28),
                     border_radius=4)
    pygame.draw.rect(surf, (200, 160, 110),
                     pygame.Rect(rect.left + 12, rect.top + 12, rect.width - 24, 12),
                     border_radius=3)
    # Bandejas no balcão
    for i in range(4):
        pygame.draw.ellipse(surf, (180, 180, 170),
                            pygame.Rect(rect.left + 20 + i * 70, rect.top + 14, 40, 12))

    # Mesas redondas com cadeiras
    table_pos = [
        (rect.left + 70,  rect.top + 100),
        (rect.left + 200, rect.top + 80),
        (rect.left + 320, rect.top + 110),
        (rect.left + 130, rect.top + 160),
        (rect.left + 270, rect.top + 165),
    ]
    for tx, ty in table_pos:
        # Cadeiras (pequenos círculos ao redor)
        for a in range(0, 360, 90):
            ang = math.radians(a)
            cx2 = int(tx + math.cos(ang) * 22)
            cy2 = int(ty + math.sin(ang) * 22)
            pygame.draw.circle(surf, (130, 85, 45), (cx2, cy2), 8)
        # Tampa da mesa
        pygame.draw.circle(surf, (150, 100, 55), (tx, ty), 16)
        pygame.draw.circle(surf, (175, 125, 75), (tx, ty), 14)


def _draw_lab(surf, rect, cor):
    """Laboratório: bancadas + equipamentos."""
    bench_col = (130, 145, 145)
    bench_drk = (100, 115, 115)

    # Bancadas
    for row in range(2):
        bx = rect.left + 15
        by = rect.top + 20 + row * 85
        pygame.draw.rect(surf, bench_drk, pygame.Rect(bx, by, rect.width - 30, 60),
                         border_radius=4)
        pygame.draw.rect(surf, bench_col, pygame.Rect(bx + 2, by + 2, rect.width - 34, 56),
                         border_radius=3)
        # Equipamentos na bancada
        for i in range(4):
            ex = bx + 20 + i * 75
            # Béquer
            pygame.draw.rect(surf, (100, 180, 220),
                             pygame.Rect(ex, by + 12, 14, 18), border_radius=2)
            pygame.draw.rect(surf, (140, 210, 240),
                             pygame.Rect(ex + 2, by + 14, 10, 8), border_radius=1)
            # Microscópio simplificado
            mx = ex + 35
            pygame.draw.rect(surf, (80, 80, 90), pygame.Rect(mx, by + 8, 14, 22))
            pygame.draw.circle(surf, (80, 80, 90), (mx + 7, by + 6), 6)


def _draw_staffroom(surf, rect, cor):
    """Sala dos professores: mesa grande + arquivos."""
    # Mesa grande no centro
    tx = rect.centerx
    ty = rect.centery
    pygame.draw.rect(surf, (120, 85, 45),
                     pygame.Rect(tx - 55, ty - 35, 110, 70), border_radius=6)
    pygame.draw.rect(surf, (150, 110, 65),
                     pygame.Rect(tx - 53, ty - 33, 106, 66), border_radius=5)
    # Papéis na mesa
    for i in range(3):
        pygame.draw.rect(surf, (240, 235, 220),
                         pygame.Rect(tx - 40 + i * 28, ty - 20, 22, 30), border_radius=2)

    # Arquivadores nas bordas
    for i in range(3):
        fx = rect.right - 30
        fy = rect.top + 15 + i * 55
        pygame.draw.rect(surf, (80, 85, 100), pygame.Rect(fx, fy, 22, 45), border_radius=2)
        pygame.draw.rect(surf, (100, 105, 120), pygame.Rect(fx + 2, fy + 2, 18, 41))
        # puxador
        pygame.draw.rect(surf, (180, 180, 190), pygame.Rect(fx + 6, fy + 20, 10, 4))


_FURNITURE_FN = {
    "classroom": _draw_classroom,
    "hallway":   _draw_hallway,
    "library":   _draw_library,
    "patio":     _draw_patio,
    "cafeteria": _draw_cafeteria,
    "lab":       _draw_lab,
    "staffroom": _draw_staffroom,
}


# ── Padrão de piso por sala ───────────────────────────────────
def _draw_floor_pattern(surf, rect, tipo, cor):
    """Desenha textura de piso sutil para cada tipo de sala."""
    if tipo in ("classroom", "staffroom"):
        # Grade de azulejos
        tc = tuple(max(0, c - 12) for c in cor)
        for x in range(rect.left, rect.right, 30):
            pygame.draw.line(surf, tc, (x, rect.top), (x, rect.bottom), 1)
        for y in range(rect.top, rect.bottom, 30):
            pygame.draw.line(surf, tc, (rect.left, y), (rect.right, y), 1)

    elif tipo in ("library",):
        # Diagonal escura
        tc = tuple(max(0, c - 10) for c in cor)
        for offset in range(-rect.height, rect.width, 25):
            x1 = rect.left + offset
            x2 = x1 + rect.height
            pygame.draw.line(surf, tc,
                             (max(rect.left, x1), rect.top if x1 >= rect.left else rect.top + (rect.left - x1)),
                             (min(rect.right, x2), rect.top + min(rect.height, rect.height + offset)), 1)

    elif tipo in ("patio",):
        # Pontos de grama
        tc = tuple(max(0, c - 15) for c in cor)
        for x in range(rect.left + 5, rect.right, 15):
            for y in range(rect.top + 5, rect.bottom, 15):
                pygame.draw.circle(surf, tc, (x, y), 1)

    elif tipo in ("lab",):
        # Linhas horizontais de bancada
        tc = tuple(max(0, c - 8) for c in cor)
        for y in range(rect.top + 20, rect.bottom, 20):
            pygame.draw.line(surf, tc, (rect.left, y), (rect.right, y), 1)


# ── Função principal de desenho ───────────────────────────────
def draw_map(surf: pygame.Surface, font: pygame.font.Font):
    """Desenha mapa completo: piso, padrões, mobília, paredes."""

    # Fundo geral (área de passagem)
    pygame.draw.rect(surf, (95, 95, 100), pygame.Rect(MAP_X, MAP_Y, MAP_PX_W, MAP_PX_H))

    # Salas: piso + padrão + mobília
    for r in ROOMS_DEF:
        rect = _room_rect(r)
        cor  = ROOM_COLORS.get(r["nome"], (200, 200, 200))

        # Piso base
        pygame.draw.rect(surf, cor, rect)

        # Padrão sutil
        _draw_floor_pattern(surf, rect, r["tipo"], cor)

        # Sombra interna nas bordas da sala
        for espessura, alpha in [(3, 30), (1, 50)]:
            borda = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(borda, (0, 0, 0, alpha), borda.get_rect(), espessura)
            surf.blit(borda, rect.topleft)

    # Mobília
    for r in ROOMS_DEF:
        rect = _room_rect(r)
        cor  = ROOM_COLORS.get(r["nome"], (200, 200, 200))
        fn   = _FURNITURE_FN.get(r["tipo"])
        if fn:
            fn(surf, rect, cor)

    # Nome das salas (texto semitransparente)
    for r in ROOMS_DEF:
        rect = _room_rect(r)
        lbl  = font.render(r["nome"], True, (0, 0, 0))
        s    = pygame.Surface(lbl.get_size(), pygame.SRCALPHA)
        s.blit(lbl, (0, 0))
        s.set_alpha(45)
        surf.blit(s, (rect.centerx - lbl.get_width() // 2,
                      rect.centery - lbl.get_height() // 2))

    # Paredes
    for w in WALLS:
        # Sombra da parede
        sombra = pygame.Rect(w.x + 2, w.y + 2, w.width, w.height)
        pygame.draw.rect(surf, (30, 30, 30), sombra)
        # Corpo da parede
        pygame.draw.rect(surf, (75, 75, 82), w)
        pygame.draw.rect(surf, (95, 95, 105), w, 1)
        # Destaque superior
        topo = pygame.Rect(w.x, w.y, w.width, 3)
        pygame.draw.rect(surf, (105, 108, 118), topo)

    # Borda do mapa
    pygame.draw.rect(surf, C_MAP_BORDER,
                     pygame.Rect(MAP_X, MAP_Y, MAP_PX_W, MAP_PX_H), 2)
