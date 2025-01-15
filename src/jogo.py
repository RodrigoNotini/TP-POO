import pygame
import sys
from tabuleiro import Tabuleiro
from peca import Peca


class Jogo:
    def __init__(self, screen, fontes, imagens, leaderboard, jogador, pause, game_over):
        self.screen = screen
        self.fontes = fontes
        self.imagens = imagens
        self.leaderboard = leaderboard
        self.jogador = jogador
        self.pause = pause
        self.game_over = game_over

        # Inicialização do jogo
        self.tabuleiro = Tabuleiro()
        self.peca_atual = Peca()
        self.proxima_peca = Peca()
        self.pontuacao = 0
        self.delay = 0.5
        self.running = False
        self.pausa = False

    def iniciar(self):
        """Inicia o loop principal do jogo."""
        if not self.jogador.nome:
            self.jogador.registrar_nome()

        self.running = True
        self.pontuacao = 0
        self.tabuleiro = Tabuleiro()
        self.peca_atual = Peca()
        self.proxima_peca = Peca()
        clock = pygame.time.Clock()

        while self.running:
            self._processar_eventos()
            if not self.pausa:
                self._atualizar_jogo()
            self._renderizar()
            clock.tick(60)

    def _processar_eventos(self):
        """Processa eventos do jogador."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    self.peca_atual.move_esquerda(self.tabuleiro.grid)
                elif evento.key == pygame.K_RIGHT:
                    self.peca_atual.move_direita(self.tabuleiro.grid)
                elif evento.key == pygame.K_UP:
                    self.peca_atual.rotaciona(self.tabuleiro.grid)
                elif evento.key == pygame.K_DOWN:
                    if self.peca_atual.pode_mover(self.tabuleiro.grid, dy=1):
                        self.peca_atual.y += 1
                elif evento.key == pygame.K_p:
                    self.pausa = not self.pausa
                    if self.pausa:
                        self.pause.exibir(lambda: None)

    def _atualizar_jogo(self):
        """Atualiza o estado do jogo."""
        if self.peca_atual.pode_mover(self.tabuleiro.grid):
            self.peca_atual.y += 1
        else:
            self.tabuleiro.adicionar_peca(self.peca_atual)
            linhas_removidas = self.tabuleiro.remover_linhas_completas()
            self.pontuacao += linhas_removidas * 100

            # Ajusta a dificuldade
            if self.pontuacao % 300 == 0:
                self.delay = max(0.1, self.delay - 0.05)

            # Verifica fim de jogo
            if not self.proxima_peca.pode_mover(self.tabuleiro.grid):
                self.running = False
                self._finalizar_jogo()

            self.peca_atual = self.proxima_peca
            self.proxima_peca = Peca()

    def _renderizar(self):
        """Renderiza o estado atual do jogo."""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.imagens["game_bg"], (0, 0))
        self.tabuleiro.desenhar(self.screen, self._desenhar_grid)
        self._desenhar_peca(self.peca_atual)
        self._desenhar_proxima_peca()
        self._desenhar_pontuacao()
        pygame.display.update()

    def _desenhar_grid(self, grid, superficie):
        """Desenha o grid do tabuleiro."""
        for y, linha in enumerate(grid):
            for x, celula in enumerate(linha):
                if celula:
                    pygame.draw.rect(
                        superficie,
                        (200, 200, 200) if celula == 8 else (50, 50, 50),
                        pygame.Rect(x * 30, y * 30, 30, 30),
                        0 if celula != 8 else 1,
                    )

    def _desenhar_peca(self, peca):
        """Desenha a peça atual."""
        for y in range(peca.altura):
            for x in range(peca.largura):
                if peca.formato[y][x] == 1:
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 0),
                        pygame.Rect((peca.x + x) * 30, (peca.y + y) * 30, 30, 30),
                    )

    def _desenhar_proxima_peca(self):
        """Desenha a próxima peça."""
        fonte = self.fontes["media"]
        texto = fonte.render("Próxima Peça:", True, (255, 255, 255))
        self.screen.blit(texto, (450, 50))

        for y, linha in enumerate(self.proxima_peca.formato):
            for x, celula in enumerate(linha):
                if celula:
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 255),
                        pygame.Rect(450 + x * 30, 100 + y * 30, 30, 30),
                    )

    def _desenhar_pontuacao(self):
        """Exibe a pontuação atual."""
        fonte = self.fontes["media"]
        texto = fonte.render(f"Pontuação: {self.pontuacao}", True, (255, 255, 255))
        self.screen.blit(texto, (450, 300))

    def _finalizar_jogo(self):
        """Finaliza o jogo, salva a pontuação e exibe a tela de Game Over."""
        self.leaderboard.salvar_leaderboard(self.jogador.nome, self.pontuacao)
        self.game_over.exibir(self.pontuacao, self.jogador.registrar_nome)
