import pygame
import sys
from utils.constantes import LARGURA

class Jogador:
    def __init__(self, screen, fontes, imagens):
        self.screen = screen
        self.fontes = fontes
        self.imagens = imagens
        self.nome = ""

    def registrar_nome(self):
        """Exibe a tela para registrar o nome do jogador."""
        ativo = True
        input_usuario = ""
        while ativo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and len(input_usuario) > 0:
                        self.nome = input_usuario.upper()
                        ativo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        input_usuario = input_usuario[:-1]
                    elif len(input_usuario) < 5 and evento.unicode.isalnum():
                        input_usuario += evento.unicode.upper()

            # Renderiza tela de registro
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.imagens["menu_bg"], (0, 0))
            self._render_texto("DIGITE SEU NOME", "grande", (255, 255, 255), LARGURA // 2, 200)
            self._render_texto("(MÁXIMO 5 LETRAS)", "pequena", (255, 255, 255), LARGURA // 2, 250)

            # Caixa de entrada
            pygame.draw.rect(
                self.screen, (255, 255, 255), (LARGURA // 2 - 100, 300, 200, 50), 2
            )
            self._render_texto(input_usuario, "grande", (255, 255, 255), LARGURA // 2, 325)

            pygame.display.update()

    def _render_texto(self, texto, fonte_key, cor, x, y):
        """Renderiza um texto na tela."""
        fonte = self.fontes[fonte_key]
        texto_renderizado = fonte.render(texto, True, cor)
        texto_rect = texto_renderizado.get_rect(center=(x, y))
        self.screen.blit(texto_renderizado, texto_rect)
