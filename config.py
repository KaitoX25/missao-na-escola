import pygame

# ── Tela ─────────────────────────────────────────────────────
SCREEN_W = 1280
SCREEN_H = 720
FPS      = 60
TITULO   = "Missão na Escola"

# ── Mapa (pixels) ─────────────────────────────────────────────
SCALE    = 20          # pixels por unidade de jogo
MAP_X    = 60          # margem esquerda
MAP_Y    = 60          # margem superior
MAP_PX_W = 800         # 40 unidades × 20
MAP_PX_H = 600         # 30 unidades × 20

# ── Painel direito (HUD) ──────────────────────────────────────
HUD_X = MAP_X + MAP_PX_W + 20
HUD_W = SCREEN_W - HUD_X - 10

# ── Cores ─────────────────────────────────────────────────────
C_BG          = (17,  24,  39)
C_MAP_BORDER  = (50,  50,  50)
C_WALL        = (70,  70,  70)
C_WHITE       = (255, 255, 255)
C_BLACK       = (0,   0,   0)
C_PLAYER      = (39,  174, 96)
C_PLAYER_OUT  = (255, 255, 255)
C_BOOK        = (41,  128, 185)
C_BOOK_SPINE  = (26,  188, 156)
C_MOCHILA     = (39,  174, 96)
C_CHAVE       = (212, 172, 13)
C_CORACAO     = (192, 57,  43)
C_TIMER_OK    = (255, 255, 255)
C_TIMER_WARN  = (243, 156, 18)
C_TIMER_CRIT  = (231, 76,  60)
C_MENU_BTN    = (41,  128, 185)
C_MENU_BTN_H  = (52,  152, 219)
C_MENU_BG     = (13,  18,  30)

# Cores dos professores
TEACHER_META = {
    "skinner":   {"cor": (26,  82, 118),  "borda": (93, 173, 226),  "label": "Skinner",   "speed": 1.0, "catch_gu": 1.6},
    "krabappel": {"cor": (146, 43,  33),  "borda": (231, 76,  60),  "label": "Krabappel", "speed": 1.6, "catch_gu": 1.2},
    "chalmers":  {"cor": (44,  62,  80),  "borda": (133, 146, 158), "label": "Chalmers",  "speed": 0.6, "catch_gu": 2.8},
}

# Cores das salas
ROOM_COLORS = {
    "Sala 1":           (221, 213, 184),
    "Corredor":         (200, 200, 200),
    "Biblioteca":       (200, 168, 122),
    "Pátio":            (168, 200, 122),
    "Cantina":          (212, 196, 122),
    "Laboratório":      (138, 176, 200),
    "Sala dos Profs.":  (200, 138, 138),
}

# ── Balanceamento ─────────────────────────────────────────────
MAX_FASE = 3
TEMPO_POR_FASE = [120, 150, 180]
VIDAS_INICIAIS = 3

FASE_CFG = [
    {"livros": 10, "mochilas": 2, "chaves": 1, "coracoes": 1,
     "professores": 3, "velocidade": 2.2},
    {"livros": 15, "mochilas": 3, "chaves": 2, "coracoes": 1,
     "professores": 4, "velocidade": 3.0},
    {"livros": 20, "mochilas": 4, "chaves": 3, "coracoes": 2,
     "professores": 5, "velocidade": 3.8},
]

PONTOS = {"livro": 10, "mochila": 20, "chave": 50, "coracao": 0}

# ── Dados dos professores ─────────────────────────────────────
ALL_TEACHERS = [
    {"id": 0, "tipo": "skinner",   "a": (-10,-12), "b": (-2, -8),  "min_fase": 1},
    {"id": 1, "tipo": "krabappel", "a": (  8,-12), "b": (16, -7),  "min_fase": 1},
    {"id": 2, "tipo": "chalmers",  "a": ( -9,  2), "b": (-4, -2),  "min_fase": 1},
    {"id": 3, "tipo": "skinner",   "a": ( -9,  6), "b": (-16,12),  "min_fase": 2},
    {"id": 4, "tipo": "krabappel", "a": (  5,  8), "b": (16, 12),  "min_fase": 2},
    {"id": 5, "tipo": "chalmers",  "a": (  0,-14), "b": (0,  -6),  "min_fase": 3},
]

def to_screen(gx: float, gz: float) -> tuple:
    """Converte coordenadas de jogo para pixels na tela."""
    px = int(MAP_X + (gx + 20) * SCALE)
    py = int(MAP_Y + (gz + 15) * SCALE)
    return px, py

def to_game(px: int, py: int) -> tuple:
    """Converte pixels na tela para coordenadas de jogo."""
    gx = (px - MAP_X) / SCALE - 20
    gz = (py - MAP_Y) / SCALE - 15
    return gx, gz
