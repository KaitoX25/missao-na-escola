import pygame
from config import (SCREEN_W, SCREEN_H, HUD_X, HUD_W,
                    C_BG, C_WHITE, C_BLACK, C_MENU_BTN, C_MENU_BTN_H,
                    C_MENU_BG, C_TIMER_OK, C_TIMER_WARN, C_TIMER_CRIT,
                    C_CORACAO, FASE_CFG, TEMPO_POR_FASE)


def _outlined(surf, font, text, color, x, y, outline=(0, 0, 0)):
    for ox, oy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        surf.blit(font.render(text, True, outline), (x+ox, y+oy))
    surf.blit(font.render(text, True, color), (x, y))


class Button:
    def __init__(self, rect: pygame.Rect, texto: str, cor=C_MENU_BTN, cor_hover=C_MENU_BTN_H):
        self.rect      = rect
        self.texto     = texto
        self.cor       = cor
        self.cor_hover = cor_hover
        self.hover     = False

    def verificar_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def clicado(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))

    def draw(self, surf, font):
        cor = self.cor_hover if self.hover else self.cor
        pygame.draw.rect(surf, cor, self.rect, border_radius=10)
        pygame.draw.rect(surf, (255, 255, 255, 40), self.rect, 1, border_radius=10)
        txt = font.render(self.texto, True, (255, 255, 255))
        surf.blit(txt, (self.rect.centerx - txt.get_width() // 2,
                        self.rect.centery - txt.get_height() // 2))


# ── MENU ──────────────────────────────────────────────────────
def criar_botoes_menu(font_btn) -> list[Button]:
    cx = SCREEN_W // 2
    bw, bh, gap = 280, 52, 14
    botoes = []
    rotulos = ["▶  Jogar", "📖  Como jogar", "🏆  Recordes", "✖  Sair"]
    cores   = [C_MENU_BTN, (52,73,94), (125,102,8), (96,40,40)]
    cores_h = [C_MENU_BTN_H, (74,101,128), (183,149,11), (146,64,64)]
    for i, (rot, cor, corh) in enumerate(zip(rotulos, cores, cores_h)):
        y = SCREEN_H // 2 - 80 + i * (bh + gap)
        botoes.append(Button(pygame.Rect(cx - bw//2, y, bw, bh), rot, cor, corh))
    return botoes


def draw_menu(surf: pygame.Surface, font_title, font_btn, font_small,
              botoes: list[Button], mouse_pos, high_score: int):
    # Fundo
    surf.fill(C_MENU_BG)

    # Ícone escola
    emoji_font = font_title
    escola = font_title.render("🏫", True, (255, 255, 255))
    surf.blit(escola, (SCREEN_W // 2 - escola.get_width() // 2, 110))

    # Título
    t1 = font_title.render("MISSÃO NA", True, (255, 255, 255))
    t2 = font_title.render("ESCOLA",   True, (255, 255, 255))
    surf.blit(t1, (SCREEN_W // 2 - t1.get_width() // 2, 180))
    surf.blit(t2, (SCREEN_W // 2 - t2.get_width() // 2, 230))

    sub = font_small.render("Colete livros  ·  Evite professores  ·  Sobreviva", True, (150, 160, 180))
    surf.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 290))

    # Controles (exigência do trabalho)
    ctrl = font_small.render("Controles:  ↑ ↓ ← →  ou  W A S D  para mover", True, (180, 200, 220))
    surf.blit(ctrl, (SCREEN_W // 2 - ctrl.get_width() // 2, SCREEN_H - 60))

    # High score
    if high_score > 0:
        hs = font_small.render(f"Recorde: {high_score} pts", True, (212, 172, 13))
        surf.blit(hs, (SCREEN_W // 2 - hs.get_width() // 2, SCREEN_H - 90))

    # Botões
    for b in botoes:
        b.verificar_hover(mouse_pos)
        b.draw(surf, font_btn)

    # Fase info
    for i, cfg in enumerate(FASE_CFG):
        lx = SCREEN_W // 2 - 180 + i * 130
        ly = SCREEN_H - 170
        pygame.draw.rect(surf, (30, 45, 70), pygame.Rect(lx, ly, 120, 50), border_radius=8)
        f_lbl = font_small.render(f"Fase {i+1}", True, (180, 200, 255))
        f_det = font_small.render(f"{cfg['livros']} livros · {TEMPO_POR_FASE[i]}s", True, (140, 155, 175))
        surf.blit(f_lbl, (lx + 60 - f_lbl.get_width()//2, ly + 8))
        surf.blit(f_det, (lx + 60 - f_det.get_width()//2, ly + 28))


def draw_como_jogar(surf, font_title, font_btn, font_small, btn_voltar, mouse_pos):
    surf.fill(C_MENU_BG)
    t = font_btn.render("Como Jogar", True, (255, 255, 255))
    surf.blit(t, (SCREEN_W // 2 - t.get_width() // 2, 80))

    linhas = [
        "↑ ↓ ← →  ou  W A S D  para mover",
        "",
        "📚  Livro       — +10 pts cada",
        "🎒  Mochila     — +20 pts",
        "🔑  Chave       — +50 pts",
        "❤   Coração     — +1 vida",
        "",
        "Evite os professores:",
        "  Skinner    — velocidade média",
        "  Krabappel  — muito rápido",
        "  Chalmers   — lento mas grande raio de captura",
        "",
        "Colete todos os livros antes do tempo acabar!",
        "Você tem 3 vidas. Se perder todas → Game Over.",
    ]
    y = 150
    for linha in linhas:
        s = font_small.render(linha, True, (200, 210, 230))
        surf.blit(s, (SCREEN_W // 2 - s.get_width() // 2, y))
        y += 32

    btn_voltar.verificar_hover(mouse_pos)
    btn_voltar.draw(surf, font_btn)


def draw_recordes(surf, font_title, font_btn, font_small,
                  high_score, achievements, btn_voltar, mouse_pos):
    surf.fill(C_MENU_BG)
    t = font_btn.render("Recordes", True, (255, 255, 255))
    surf.blit(t, (SCREEN_W // 2 - t.get_width() // 2, 80))

    hs = font_title.render(f"{high_score} pts", True, (212, 172, 13))
    surf.blit(hs, (SCREEN_W // 2 - hs.get_width() // 2, 150))

    achs = [
        ("primeiroLivro",  "📚", "Primeiro Livro",   "Coletou o 1º livro"),
        ("sobrevivente",   "🛡", "Sobrevivente",      "Completou fase sem perder vida"),
        ("alunoNota10",    "⭐", "Aluno Nota 10",     "Terminou com mais de 60s sobrando"),
        ("missaoCompleta", "🏆", "Missão Completa",   "Concluiu todas as fases"),
    ]
    y = 250
    for key, icon, nome, desc in achs:
        unlocked = achievements.get(key, False)
        cor = (255, 215, 0) if unlocked else (70, 80, 100)
        bg  = (30, 45, 70) if unlocked else (20, 28, 45)
        pygame.draw.rect(surf, bg, pygame.Rect(SCREEN_W//2 - 230, y, 460, 52), border_radius=8)
        pygame.draw.rect(surf, cor, pygame.Rect(SCREEN_W//2 - 230, y, 460, 52), 1, border_radius=8)
        n_s = font_small.render(f"{icon}  {nome}", True, cor)
        d_s = font_small.render(desc, True, (120, 130, 150) if not unlocked else (180, 200, 220))
        surf.blit(n_s, (SCREEN_W//2 - 215, y + 6))
        surf.blit(d_s, (SCREEN_W//2 - 215, y + 28))
        y += 62

    btn_voltar.verificar_hover(mouse_pos)
    btn_voltar.draw(surf, font_btn)


# ── HUD em jogo ───────────────────────────────────────────────
def draw_hud(surf, font_hud, font_small,
             fase, score, vidas, tempo, coletados, total_livros):
    # Painel direito
    panel = pygame.Rect(HUD_X, 55, HUD_W - 5, SCREEN_H - 70)
    pygame.draw.rect(surf, (13, 20, 35), panel, border_radius=10)
    pygame.draw.rect(surf, (30, 50, 90), panel, 1, border_radius=10)

    x = HUD_X + 15
    y = 75

    def linha(txt, cor=(220, 230, 255), grande=False):
        nonlocal y
        f = font_hud if grande else font_small
        s = f.render(txt, True, cor)
        surf.blit(s, (x, y))
        y += s.get_height() + (8 if grande else 5)

    def sep():
        nonlocal y
        pygame.draw.line(surf, (30, 50, 90), (x, y + 3), (HUD_X + HUD_W - 20, y + 3))
        y += 14

    linha(f"FASE {fase}", (180, 200, 255), grande=True)
    sep()

    linha("📚 Livros")
    linha(f"  {coletados} / {total_livros}", (88, 214, 141) if coletados < total_livros else (212, 172, 13))
    sep()

    # Timer
    cor_timer = C_TIMER_OK
    if tempo < 30:
        cor_timer = C_TIMER_CRIT
    elif tempo < 60:
        cor_timer = C_TIMER_WARN
    mins = int(tempo) // 60
    secs = int(tempo) % 60
    linha("⏱ Tempo")
    linha(f"  {mins}:{secs:02d}", cor_timer, grande=True)
    sep()

    linha("Pontuação")
    linha(f"  {score} pts", (255, 215, 0))
    sep()

    linha("❤  Vidas")
    coracao_str = "❤ " * vidas
    linha(f"  {vidas}", (231, 76, 60))
    sep()

    y = SCREEN_H - 130
    linha("─── Professores ───", (80, 100, 140))
    tipos = [("Skinner",   (93, 173, 226)),
             ("Krabappel", (231, 76, 60)),
             ("Chalmers",  (133, 146, 158))]
    for nome, cor in tipos:
        pygame.draw.circle(surf, cor, (x + 8, y + 7), 7)
        s = font_small.render(nome, True, cor)
        surf.blit(s, (x + 22, y))
        y += 22


# ── Overlays em jogo ──────────────────────────────────────────
def _overlay_base(surf, alpha=180):
    s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    s.fill((0, 0, 0, alpha))
    surf.blit(s, (0, 0))


def _card(surf, w, h):
    cx = SCREEN_W // 2
    cy = SCREEN_H // 2
    rect = pygame.Rect(cx - w//2, cy - h//2, w, h)
    pygame.draw.rect(surf, (13, 20, 35), rect, border_radius=16)
    pygame.draw.rect(surf, (50, 80, 140), rect, 2, border_radius=16)
    return rect


def draw_pego(surf, font_title, font_btn, font_small,
              btn_tentar, btn_menu, mouse_pos, vidas_restantes):
    _overlay_base(surf)
    r = _card(surf, 420, 320)
    cx = r.centerx
    y  = r.top + 30

    t = font_title.render("😱 PEGO!", True, (231, 76, 60))
    surf.blit(t, (cx - t.get_width()//2, y)); y += t.get_height() + 12

    v = font_small.render(f"Vidas restantes: {vidas_restantes}", True, (255, 200, 200))
    surf.blit(v, (cx - v.get_width()//2, y)); y += v.get_height() + 30

    btn_tentar.rect.centerx = cx
    btn_tentar.rect.y = y; y += btn_tentar.rect.height + 12
    btn_menu.rect.centerx = cx
    btn_menu.rect.y = y

    for b in [btn_tentar, btn_menu]:
        b.verificar_hover(mouse_pos)
        b.draw(surf, font_btn)


def draw_game_over(surf, font_title, font_btn, font_small,
                   btn_menu, mouse_pos, score):
    _overlay_base(surf)
    r = _card(surf, 420, 280)
    cx = r.centerx
    y  = r.top + 30

    t = font_title.render("GAME OVER", True, (192, 57, 43))
    surf.blit(t, (cx - t.get_width()//2, y)); y += t.get_height() + 12

    s = font_small.render(f"Pontuação final: {score} pts", True, (220, 220, 220))
    surf.blit(s, (cx - s.get_width()//2, y)); y += s.get_height() + 30

    btn_menu.rect.centerx = cx
    btn_menu.rect.y = y
    btn_menu.verificar_hover(mouse_pos)
    btn_menu.draw(surf, font_btn)


def draw_fase_completa(surf, font_title, font_btn, font_small,
                       btn_proxima, mouse_pos, fase, score, time_bonus):
    _overlay_base(surf)
    r = _card(surf, 440, 320)
    cx = r.centerx
    y  = r.top + 28

    t = font_title.render(f"✓ Fase {fase} Completa!", True, (46, 204, 113))
    surf.blit(t, (cx - t.get_width()//2, y)); y += t.get_height() + 10

    s1 = font_small.render(f"Bônus de tempo: +{time_bonus} pts", True, (212, 172, 13))
    surf.blit(s1, (cx - s1.get_width()//2, y)); y += s1.get_height() + 6

    s2 = font_small.render(f"Pontuação: {score} pts", True, (200, 220, 255))
    surf.blit(s2, (cx - s2.get_width()//2, y)); y += s2.get_height() + 28

    btn_proxima.rect.centerx = cx
    btn_proxima.rect.y = y
    btn_proxima.verificar_hover(mouse_pos)
    btn_proxima.draw(surf, font_btn)


def draw_vitoria(surf, font_title, font_btn, font_small,
                 btn_menu, mouse_pos, score, high_score, countdown):
    _overlay_base(surf)
    r = _card(surf, 480, 340)
    cx = r.centerx
    y  = r.top + 25

    t = font_title.render("🏆 MISSÃO CUMPRIDA!", True, (212, 172, 13))
    surf.blit(t, (cx - t.get_width()//2, y)); y += t.get_height() + 12

    s1 = font_small.render(f"Pontuação final: {score} pts", True, (255, 220, 100))
    surf.blit(s1, (cx - s1.get_width()//2, y)); y += s1.get_height() + 6

    s2 = font_small.render(f"Recorde: {high_score} pts", True, (255, 215, 0))
    surf.blit(s2, (cx - s2.get_width()//2, y)); y += s2.get_height() + 20

    s3 = font_small.render(f"Voltando ao menu em {countdown}s...", True, (150, 160, 180))
    surf.blit(s3, (cx - s3.get_width()//2, y)); y += s3.get_height() + 18

    btn_menu.rect.centerx = cx
    btn_menu.rect.y = y
    btn_menu.verificar_hover(mouse_pos)
    btn_menu.draw(surf, font_btn)
