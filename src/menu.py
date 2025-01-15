import pygame
import sys
from leaderboard import LeaderBoard
from utils.constantes import LARGURA, ALTURA


class Menu:
    def __init__(self, screen, fontes, imagens, leaderboard):
        self.screen = screen
        self.imagens = imagens
        self.fontes = fontes
        self.leaderboard = leaderboard

    def exibir_menu(self):
        """Exibe a tela principal do menu."""
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    return  # Inicia o jogo

            # Renderiza fundo
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.imagens["menu_bg"], (0, 0))

            # Renderiza textos
            self._render_texto("TETRIS", "titulo", (255, 255, 255), LARGURA // 2, 100)
            self._render_texto(
                "APERTE ESPAÇO PARA JOGAR",
                "grande",
                (255, 255, 255),
                LARGURA // 2,
                180,
            )
            self._render_texto(
                "MELHORES PONTUAÇÕES", "media", (255, 255, 255), LARGURA // 2, 280
            )

            # Renderiza leaderboard
            self._render_leaderboard()

            # Renderiza controles
            self._render_controles()

            pygame.display.update()

    def _render_texto(self, texto, fonte_key, cor, x, y):
        fonte = self.fontes[fonte_key]
        texto_renderizado = fonte.render(texto, True, cor)
        texto_rect = texto_renderizado.get_rect(center=(x, y))
        self.screen.blit(texto_renderizado, texto_rect)

    def _render_leaderboard(self):
        leaderboard = self.leaderboard.carregar_leaderboard()
        for idx, (player, pts) in enumerate(leaderboard):
            texto = f"{player}: {pts} pts"
            self._render_texto(
                texto, "media", (255, 255, 255), LARGURA // 2, 320 + idx * 30
            )

    def _render_controles(self):
        controles = "CONTROLES:\n← ou A: ESQUERDA\n→ ou D: DIREITA\n↑ ou W: ROTACIONAR\nP: PAUSAR O JOGO"
        linhas = controles.split("\n")
        for i, linha in enumerate(linhas):
            self._render_texto(
                linha, "pequena", (255, 255, 255), LARGURA // 2, 500 + i * 20
            )
