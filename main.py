"""
Missão na Escola — Demo de Jogo
Disciplina: Linguagem de Programação Aplicada

Controles: ↑ ↓ ← →  ou  W A S D  para mover
"""

import sys
import json
import os
import pygame

from config import (SCREEN_W, SCREEN_H, FPS, TITULO,
                    MAX_FASE, TEMPO_POR_FASE, VIDAS_INICIAIS, FASE_CFG,
                    PONTOS, ALL_TEACHERS, TEACHER_META)
from level  import draw_map
from player import Player
from enemy  import Professor
from items  import criar_itens_fase
from sounds import SoundManager
from ui     import (criar_botoes_menu, Button,
                    draw_menu, draw_como_jogar, draw_recordes,
                    draw_hud, draw_pego, draw_game_over,
                    draw_fase_completa, draw_vitoria)

# ── Persistência ──────────────────────────────────────────────
SAVE_FILE = "save_data.json"

def carregar_save() -> dict:
    try:
        with open(SAVE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"high_score": 0, "achievements": {}}

def gravar_save(data: dict):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


class Jogo:
    """Classe principal que gerencia todo o estado do jogo."""

    # Estados possíveis
    MENU         = "menu"
    COMO_JOGAR   = "como_jogar"
    RECORDES     = "recordes"
    JOGANDO      = "jogando"
    PEGO         = "pego"
    FASE_COMPLETA = "fase_completa"
    VITORIA      = "vitoria"
    GAME_OVER    = "game_over"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(TITULO)
        self.clock  = pygame.time.Clock()

        # Fontes
        nome_fonte = pygame.font.match_font("arial,freesansbold")
        self.font_titulo = pygame.font.Font(nome_fonte, 42)
        self.font_btn    = pygame.font.Font(nome_fonte, 22)
        self.font_hud    = pygame.font.Font(nome_fonte, 26)
        self.font_small  = pygame.font.Font(nome_fonte, 15)

        # Persistência
        save = carregar_save()
        self.high_score  = save.get("high_score", 0)
        self.achievements = save.get("achievements", {})

        # Sons
        self.sons = SoundManager()

        # Estado
        self.estado = self.MENU

        # Botões reutilizáveis
        self.botoes_menu   = criar_botoes_menu(self.font_btn)
        self.btn_voltar    = Button(pygame.Rect(SCREEN_W//2-110, SCREEN_H-100, 220, 48), "← Voltar")
        self.btn_jogar_nov = Button(pygame.Rect(SCREEN_W//2-110, 0, 220, 48), "▶  Tentar Novamente",
                                    (39,174,96), (46,204,113))
        self.btn_menu_vol  = Button(pygame.Rect(SCREEN_W//2-110, 0, 220, 48), "← Menu Principal",
                                    (52,73,94), (74,101,128))
        self.btn_proxima   = Button(pygame.Rect(SCREEN_W//2-110, 0, 220, 48), "Próxima Fase ▶",
                                    (39,174,96), (46,204,113))
        self.btn_fim       = Button(pygame.Rect(SCREEN_W//2-110, 0, 220, 48), "← Menu Principal",
                                    (52,73,94), (74,101,128))

        # Objetos de jogo (inicializados em _nova_fase)
        self.jogador    = Player()
        self.professores: list[Professor] = []
        self.itens: dict = {}
        self.fase        = 1
        self.score       = 0
        self.vidas       = VIDAS_INICIAIS
        self.tempo       = float(TEMPO_POR_FASE[0])
        self.coletados   = 0
        self.time_bonus  = 0
        self.vidas_inicio_fase = VIDAS_INICIAIS
        self.countdown   = 5      # para tela de vitória
        self._countdown_acc = 0.0
        self._caught_cooldown = 0.0  # pequeno delay antes de mostrar "pego"

    # ── Inicialização de fase ─────────────────────────────────
    def _nova_fase(self, fase: int, manter_score: bool = True):
        self.fase  = fase
        self.tempo = float(TEMPO_POR_FASE[fase - 1])
        self.coletados = 0
        self.time_bonus = 0
        self.vidas_inicio_fase = self.vidas
        self.jogador.reset()
        self.itens = criar_itens_fase(fase)

        cfg = FASE_CFG[fase - 1]
        ativos = [t for t in ALL_TEACHERS if t["min_fase"] <= fase][:cfg["professores"]]
        self.professores = [Professor(t) for t in ativos]

        if not manter_score:
            self.score = 0
            self.vidas = VIDAS_INICIAIS
        self.estado = self.JOGANDO

    def _reiniciar_fase(self):
        """Tenta de novo a mesma fase."""
        self.itens = criar_itens_fase(self.fase)
        self.tempo = float(TEMPO_POR_FASE[self.fase - 1])
        self.coletados = 0
        self.jogador.reset()
        for p in self.professores:
            p.reset()
        self.estado = self.JOGANDO

    # ── Verificar conquistas ──────────────────────────────────
    def _unlock(self, *keys):
        mudou = False
        for k in keys:
            if not self.achievements.get(k):
                self.achievements[k] = True
                mudou = True
        if mudou:
            self._gravar()

    def _atualizar_hs(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self._gravar()

    def _gravar(self):
        gravar_save({"high_score": self.high_score,
                     "achievements": self.achievements})

    # ── Update jogando ────────────────────────────────────────
    def _update_jogando(self, dt: float, keys):
        # Cooldown antes de checar "pego" (evita detecção instantânea ao respawnar)
        if self._caught_cooldown > 0:
            self._caught_cooldown -= dt
            self._caught_cooldown = max(0.0, self._caught_cooldown)

        # Timer
        self.tempo -= dt
        if self.tempo <= 0:
            self.tempo = 0
            self._ser_pego()
            return

        # Jogador
        self.jogador.update(dt, keys)
        px, py = self.jogador.x, self.jogador.y

        # Professores
        cfg = FASE_CFG[self.fase - 1]
        for prof in self.professores:
            prof.update(dt, cfg["velocidade"])
            if self._caught_cooldown <= 0 and prof.checa_pegar(px, py):
                self._ser_pego()
                return

        # Coletar itens
        for livro in self.itens["livros"]:
            if livro.checar_coleta(px, py):
                self.score += PONTOS["livro"]
                self.coletados += 1
                self.sons.tocar("coletar")
                if self.coletados == 1:
                    self._unlock("primeiroLivro")
                if self.coletados >= len(self.itens["livros"]):
                    self._fase_completa()
                    return

        for mochila in self.itens["mochilas"]:
            if mochila.checar_coleta(px, py):
                self.score += PONTOS["mochila"]
                self.sons.tocar("coletar")

        for chave in self.itens["chaves"]:
            if chave.checar_coleta(px, py):
                self.score += PONTOS["chave"]
                self.sons.tocar("coletar")

        for coracao in self.itens["coracoes"]:
            if coracao.checar_coleta(px, py):
                self.vidas += 1
                self.sons.tocar("coletar")

    def _ser_pego(self):
        self.vidas -= 1
        self.sons.tocar("pego")
        if self.vidas <= 0:
            self._atualizar_hs()
            self.estado = self.GAME_OVER
        else:
            self.estado = self.PEGO

    def _fase_completa(self):
        self.time_bonus = int(self.tempo)
        self.score += self.time_bonus
        self.sons.tocar("fase_ok")

        if self.vidas >= self.vidas_inicio_fase:
            self._unlock("sobrevivente")
        if self.time_bonus >= 60:
            self._unlock("alunoNota10")

        if self.fase >= MAX_FASE:
            self._unlock("missaoCompleta")
            self._atualizar_hs()
            self.vidas += 1
            self.countdown = 5
            self._countdown_acc = 0.0
            self.estado = self.VITORIA
        else:
            self.vidas += 1
            self.estado = self.FASE_COMPLETA

    # ── Desenho do jogo ───────────────────────────────────────
    def _draw_jogo(self):
        self.screen.fill((17, 24, 39))
        draw_map(self.screen, self.font_small)

        # Itens (com animação de flutuação)
        time_ms = pygame.time.get_ticks()
        for grupo in self.itens.values():
            for item in grupo:
                item.draw(self.screen, time_ms)

        # Professores
        px, py = self.jogador.x, self.jogador.y
        for prof in self.professores:
            prof.draw(self.screen, self.font_small, px, py)

        # Jogador
        self.jogador.draw(self.screen, self.font_small)

        # HUD
        draw_hud(self.screen, self.font_hud, self.font_small,
                 self.fase, self.score, self.vidas, self.tempo,
                 self.coletados, len(self.itens["livros"]))

    # ── Loop principal ────────────────────────────────────────
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # limita delta em caso de lag
            mouse = pygame.mouse.get_pos()
            keys  = pygame.key.get_pressed()

            # ── Eventos ──────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.estado == self.MENU:
                    if self.botoes_menu[0].clicado(event):   # Jogar
                        self._nova_fase(1, manter_score=False)
                    elif self.botoes_menu[1].clicado(event): # Como jogar
                        self.estado = self.COMO_JOGAR
                    elif self.botoes_menu[2].clicado(event): # Recordes
                        self.estado = self.RECORDES
                    elif self.botoes_menu[3].clicado(event): # Sair
                        pygame.quit(); sys.exit()

                elif self.estado in (self.COMO_JOGAR, self.RECORDES):
                    if self.btn_voltar.clicado(event):
                        self.estado = self.MENU

                elif self.estado == self.PEGO:
                    if self.btn_jogar_nov.clicado(event):
                        self._reiniciar_fase()
                        self._caught_cooldown = 1.5
                    elif self.btn_menu_vol.clicado(event):
                        self.estado = self.MENU

                elif self.estado == self.GAME_OVER:
                    if self.btn_menu_vol.clicado(event):
                        self.estado = self.MENU

                elif self.estado == self.FASE_COMPLETA:
                    if self.btn_proxima.clicado(event):
                        self._nova_fase(self.fase + 1)
                        self._caught_cooldown = 1.5

                elif self.estado == self.VITORIA:
                    if self.btn_fim.clicado(event):
                        self.estado = self.MENU

                # ESC sempre vai ao menu (exceto se já no menu)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.estado not in (self.MENU,):
                        self.estado = self.MENU

            # ── Update ────────────────────────────────────────
            if self.estado == self.JOGANDO:
                self._update_jogando(dt, keys)

            if self.estado == self.VITORIA:
                self._countdown_acc += dt
                if self._countdown_acc >= 1.0:
                    self._countdown_acc -= 1.0
                    self.countdown -= 1
                    if self.countdown <= 0:
                        self.estado = self.MENU

            # ── Desenho ──────────────────────────────────────
            if self.estado == self.MENU:
                draw_menu(self.screen, self.font_titulo, self.font_btn, self.font_small,
                          self.botoes_menu, mouse, self.high_score)

            elif self.estado == self.COMO_JOGAR:
                draw_como_jogar(self.screen, self.font_titulo, self.font_btn, self.font_small,
                                self.btn_voltar, mouse)

            elif self.estado == self.RECORDES:
                draw_recordes(self.screen, self.font_titulo, self.font_btn, self.font_small,
                              self.high_score, self.achievements, self.btn_voltar, mouse)

            elif self.estado in (self.JOGANDO, self.PEGO, self.FASE_COMPLETA,
                                 self.VITORIA, self.GAME_OVER):
                self._draw_jogo()

                if self.estado == self.PEGO:
                    draw_pego(self.screen, self.font_titulo, self.font_btn, self.font_small,
                              self.btn_jogar_nov, self.btn_menu_vol, mouse, self.vidas)

                elif self.estado == self.GAME_OVER:
                    draw_game_over(self.screen, self.font_titulo, self.font_btn, self.font_small,
                                   self.btn_menu_vol, mouse, self.score)

                elif self.estado == self.FASE_COMPLETA:
                    draw_fase_completa(self.screen, self.font_titulo, self.font_btn, self.font_small,
                                       self.btn_proxima, mouse, self.fase, self.score, self.time_bonus)

                elif self.estado == self.VITORIA:
                    draw_vitoria(self.screen, self.font_titulo, self.font_btn, self.font_small,
                                 self.btn_fim, mouse, self.score, self.high_score, self.countdown)

            pygame.display.flip()


if __name__ == "__main__":
    Jogo().run()
