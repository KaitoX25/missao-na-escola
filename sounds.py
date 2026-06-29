import pygame
import os

class SoundManager:
    """Gerencia sons do jogo. Funciona mesmo sem arquivos de som."""

    def __init__(self):
        self._sons = {}
        self._ativo = False
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._ativo = True
            self._carregar("coletar",    os.path.join("assets", "sounds", "coin.wav"))
            self._carregar("pego",       os.path.join("assets", "sounds", "gameover.wav"))
            self._carregar("fase_ok",    os.path.join("assets", "sounds", "jump.wav"))
        except Exception:
            pass

    def _carregar(self, nome: str, caminho: str):
        try:
            if os.path.exists(caminho):
                self._sons[nome] = pygame.mixer.Sound(caminho)
        except Exception:
            pass

    def tocar(self, nome: str):
        if self._ativo and nome in self._sons:
            try:
                self._sons[nome].play()
            except Exception:
                pass
