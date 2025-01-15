import pygame
import sys
from utils.constantes import LARGURA, ALTURA


class Menu:
    def __init__(self, screen, fontes, imagens, leaderboard):
        self.screen = screen
        self.imagens = imagens
        self.fontes = fontes
        self.leaderboard = leaderboard

    def exibir_menu(self, tela_detalhes, tela_creditos):
        """Exibe a tela principal do menu."""
        rodando = True

        while rodando:
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
            self.leaderboard.exibir_leaderboard(
                self.fontes["media"], (255, 255, 255), self.screen, LARGURA // 4, 320
            )

            # Renderiza controles
            self._render_controles()

            # Renderiza botões interativos
            self._render_botao(
                "CRÉDITOS",
                "media",
                (0, 0, 0),
                100,
                490,
                120,
                40,
                evento_click=tela_creditos.exibir,
            )
            self._render_botao(
                "DETALHES",
                "media",
                (0, 0, 0),
                280,
                490,
                120,
                40,
                evento_click=tela_detalhes.exibir,
            )

            pygame.display.update()

    def _render_texto(self, texto, fonte_key, cor, x, y):
        fonte = self.fontes[fonte_key]
        texto_renderizado = fonte.render(texto, True, cor)
        texto_rect = texto_renderizado.get_rect(center=(x, y))
        self.screen.blit(texto_renderizado, texto_rect)

    def _render_controles(self):
        controles = "CONTROLES:\n← ou A: ESQUERDA\n→ ou D: DIREITA\n↑ ou W: ROTACIONAR\nP: PAUSAR O JOGO"
        linhas = controles.split("\n")
        for i, linha in enumerate(linhas):
            self._render_texto(
                linha, "pequena", (255, 255, 255), LARGURA // 2, 600 + i * 20
            )

    def _render_botao(self, texto, fonte_key, cor, x, y, largura, altura, evento_click):
        """Renderiza um botão e executa o evento de clique."""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        # Cor do botão com hover
        cor_fundo = (
            (100, 100, 100)
            if x <= mouse[0] <= x + largura and y <= mouse[1] <= y + altura
            else (150, 150, 150)
        )

        # Renderiza botão
        pygame.draw.rect(self.screen, cor_fundo, (x, y, largura, altura))

        # Renderiza texto no botão
        self._render_texto(texto, fonte_key, cor, x + largura // 2, y + altura // 2)

        # Verifica clique
        if (
            click
            and evento_click
            and x <= mouse[0] <= x + largura
            and y <= mouse[1] <= y + altura
        ):
            evento_click()
