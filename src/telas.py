import pygame
import sys
from utils.constantes import LARGURA


class Tela:
    def __init__(self, screen, fontes, imagens):
        self.screen = screen
        self.fontes = fontes
        self.imagens = imagens

    # def render_texto(self, texto, fonte_key, cor, x, y, centro=True):
    #     """Renderiza texto na tela."""
    #     fonte = self.fontes[fonte_key]
    #     texto_renderizado = fonte.render(texto, True, cor)
    #     texto_rect = texto_renderizado.get_rect(center=(x, y) if centro else (x, y))
    #     self.screen.blit(texto_renderizado, texto_rect)

    def render_texto(self, texto, fonte_key, cor, x, y, centro=False):
        lines = texto.split("\n")
        fonte = self.fontes[fonte_key]
        for i, line in enumerate(lines):
            texto_renderizado = fonte.render(line, True, cor)
            texto_rect = texto_renderizado.get_rect(
                center=(x, y + i * 20) if centro else (x, y)
            )
            self.screen.blit(texto_renderizado, texto_rect)

    def render_botao(
        self, texto, fonte_key, cor, x, y, largura, altura, evento_click=None
    ):
        """Renderiza um botão na tela e executa o evento de clique."""
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

        # Renderiza texto do botão
        self.render_texto(texto, fonte_key, cor, x + largura // 2, y + altura // 2)

        # Verifica clique
        if (
            click
            and evento_click
            and x <= mouse[0] <= x + largura
            and y <= mouse[1] <= y + altura
        ):
            evento_click()


class Detalhes(Tela):
    def exibir(self):
        """Exibe a tela de detalhes."""
        rodando = True

        def fechar_tela():
            nonlocal rodando
            rodando = False

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Renderiza fundo e conteúdo
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.imagens["menu_bg"], (0, 0))

            # Renderiza texto
            self.render_texto(
                "OBJETIVO DO JOGO", "grande", (255, 255, 255), LARGURA // 4, 50
            )
            self.render_texto(
                "Empilhe blocos para completar linhas.\n"
                "Colete o máximo de pontos antes que o jogo termine.\n"
                "Cada linha vale 100 pontos.",
                "pequena",
                (255, 255, 255),
                LARGURA // 2,
                100,
                centro=True,
            )

            self.render_texto(
                "OBSTÁCULOS", "grande", (255, 255, 255), LARGURA // 4, 200
            )
            self.render_texto(
                "Ao longo do jogo voce sera desafiado com certos obstaculos.\n"
                "A cada 300 pontos, o jogo fica mais rápido.\n"
                "A cada 500 pontos, uma linha indestrutível é adicionada.",
                "pequena",
                (255, 255, 255),
                LARGURA // 2,
                250,
                centro=True,
            )

            self.render_texto("CHEATS", "grande", (255, 255, 255), LARGURA // 4, 340)
            self.render_texto(
                "Aperte 'x' para passar o bloco que esta vindo.\n\nAperte 'z' para desacelerar o jogo.\n"
                "(Efeitos especiais na pontuacao>300)\n\nAperte 'c' para destruir a linha mais ao fundo\n\nAperte 'ESC' "
                "para ativar a tecla do chefe.",
                "pequena",
                (255, 255, 255),
                LARGURA // 2,
                390,
                centro=True,
            )

            # Botão "Voltar"
            self.render_botao(
                "VOLTAR",
                "media",
                (0, 0, 0),
                LARGURA // 2 - 50,
                550,
                100,
                50,
                evento_click=fechar_tela,
            )

            pygame.display.update()


class Creditos(Tela):
    def exibir(self):
        """Exibe a tela de créditos."""
        rodando = True

        def fechar_tela():
            nonlocal rodando
            rodando = False

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Renderiza fundo
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.imagens["menu_bg"], (0, 0))

            # Renderiza texto
            self.render_texto("CRÉDITOS", "grande", (255, 255, 255), LARGURA // 2, 100)
            self.render_texto("FEITO POR:", "media", (255, 255, 255), LARGURA // 2, 200)
            self.render_texto(
                "Rodrigo, Gabriel e Pedro", "media", (255, 255, 255), LARGURA // 2, 250
            )

            # Botão "Voltar"
            self.render_botao(
                "VOLTAR",
                "media",
                (0, 0, 0),
                LARGURA // 2 - 50,
                400,
                100,
                50,
                evento_click=fechar_tela,
            )

            pygame.display.update()


class GameOver(Tela):
    def __init__(self, screen, fontes, imagens, leaderboard):
        super().__init__(screen, fontes, imagens)
        self.leaderboard = leaderboard  # Armazena o leaderboard para uso posterior

    def exibir(self, pontuacao, reiniciar_callback):
        """Exibe a tela de Game Over."""
        rodando = True

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Renderiza fundo
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.imagens["menu_bg"], (0, 0))

            # Renderiza texto
            self.render_texto("GAME OVER", "titulo", (255, 0, 0), LARGURA // 2, 100)
            self.render_texto(
                f"PONTUAÇÃO: {pontuacao}", "grande", (255, 255, 255), LARGURA // 2, 200
            )

            # Renderiza leaderboard atualizado
            self.leaderboard.exibir_leaderboard(
                self.fontes["media"], (255, 255, 255), self.screen, LARGURA // 2, 250
            )

            # Botão "Reiniciar"
            self.render_botao(
                "REINICIAR",
                "media",
                (0, 0, 0),
                LARGURA // 2 - 50,
                300,
                100,
                50,
                evento_click=reiniciar_callback,
            )

            pygame.display.update()


class Pause(Tela):
    def exibir(self, continuar_callback):
        """Exibe a tela de pausa."""
        rodando = True

        def continuar_jogo():
            nonlocal rodando
            rodando = False

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Renderiza fundo
            self.screen.fill((0, 0, 0))

            # Renderiza texto
            self.render_texto("PAUSADO", "titulo", (255, 255, 255), LARGURA // 2, 100)
            self.render_texto(
                "APERTE 'P' PARA CONTINUAR", "media", (255, 255, 255), LARGURA // 2, 200
            )

            # Botão "Continuar"
            self.render_botao(
                "CONTINUAR",
                "media",
                (0, 0, 0),
                LARGURA // 2 - 50,
                300,
                100,
                50,
                evento_click=continuar_jogo,
            )

            pygame.display.update()
