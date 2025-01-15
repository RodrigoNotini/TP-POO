import pygame
import sys
from tabuleiro import Tabuleiro
from peca import Peca, Quadrado, LDireita, LEsquerda, Vertical, T, ZDireita, ZEsquerda
from utils.constantes import FPS, BLOCK_SIZE
from utils.cores import CORES
import time

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
        self.delay = 0.12
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
            clock.tick(FPS)

    def _processar_eventos(self):
        """Processa eventos do jogador."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    self.peca_atual.move_esquerda(self.tabuleiro.grid)
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    self.peca_atual.move_direita(self.tabuleiro.grid)
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    self.peca_atual.rotaciona(self.tabuleiro.grid)
                elif evento.key == pygame.K_DOWN:
                    if self.peca_atual.pode_mover(self.tabuleiro.grid, dy=1):
                        self.peca_atual.y += 1
                elif evento.key == pygame.K_x:
                    self.proxima_peca = Peca()
                elif evento.key == pygame.K_z:
                    self.delay = 0.25
                elif evento.key == pygame.K_q:
                    self.peca_atual = Quadrado()  # Define a peça atual como Quadrado
                    self.proxima_peca = (
                        Quadrado()
                    )  # Garante que a próxima peça também será Quadrado
                elif evento.key == pygame.K_l:
                    self.peca_atual = LDireita()  # Define a peça atual como LDireita
                    self.proxima_peca = (
                        LDireita()
                    )  # Garante que a próxima peça também será LDireita
                elif evento.key == pygame.K_j:
                    self.peca_atual = LEsquerda()  # Define a peça atual como LEsquerda
                    self.proxima_peca = (
                        LEsquerda()
                    )  # Garante que a próxima peça também será LEsquerda
                elif evento.key == pygame.K_i:
                    self.peca_atual = Vertical()  # Define a peça atual como Vertical
                    self.proxima_peca = (
                        Vertical()
                    )  # Garante que a próxima peça também será Vertical
                elif evento.key == pygame.K_t:
                    self.peca_atual = T()  # Define a peça atual como T
                    self.proxima_peca = T()  # Garante que a próxima peça também será T
                elif evento.key == pygame.K_n:
                    self.peca_atual = ZDireita()  # Define a peça atual como ZDireita
                    self.proxima_peca = (
                        ZDireita()
                    )  # Garante que a próxima peça também será ZDireita
                elif evento.key == pygame.K_b:
                    self.peca_atual = ZEsquerda()  # Define a peça atual como ZEsquerda
                    self.proxima_peca = (
                        ZEsquerda()
                    )  # Garante que a próxima peça também será Zesquerda
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
            if self.pontuacao % 600 == 0 and self.pontuacao != 0:
                self.delay = max(0.1, self.delay - 0.015)

            # Verifica fim de jogo
            if not self.proxima_peca.pode_mover(self.tabuleiro.grid):
                self.running = False
                self._finalizar_jogo()

            self.peca_atual = self.proxima_peca
            self.proxima_peca = Peca()

    def _renderizar(self):
        """Renderiza o estado atual do jogo."""
        self.screen.blit(self.imagens["game_bg"], (0, 0))
        self._desenhar_tabuleiro()
        self._desenhar_peca_atual()
        self._desenhar_proxima_peca()
        self._desenhar_pontuacao()
        self.pontuacao += 1
        time.sleep(self.delay)  # Atraso entre atualizações.
        pygame.display.update()

    def _desenhar_tabuleiro(self):
        """Desenha o grid do tabuleiro."""
        for y, linha in enumerate(self.tabuleiro.grid):
            for x, celula in enumerate(linha):
                cor = CORES[celula]
                rect = pygame.Rect(
                    110 + x * BLOCK_SIZE, 200 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(self.screen, cor, rect)
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

    def _desenhar_peca_atual(self):
        """Desenha a peça atual."""
        for y in range(self.peca_atual.altura):
            for x in range(self.peca_atual.largura):
                if self.peca_atual.formato[y][x] == 1:
                    cor = CORES[self.peca_atual.cor]
                    rect = pygame.Rect(
                        110 + (self.peca_atual.x + x) * BLOCK_SIZE,
                        200 + (self.peca_atual.y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    )
                    pygame.draw.rect(self.screen, cor, rect)
                    pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

    def _desenhar_proxima_peca(self):
        """Desenha a próxima peça."""
        topo_proximo = 100
        direita_proximo = 400
        for y in range(self.proxima_peca.altura):
            for x in range(self.proxima_peca.largura):
                if self.proxima_peca.formato[y][x] == 1:
                    cor = CORES[self.proxima_peca.cor]
                    rect = pygame.Rect(
                        direita_proximo + x * BLOCK_SIZE,
                        topo_proximo + y * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    )
                    pygame.draw.rect(self.screen, cor, rect)
                    pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

    def _desenhar_pontuacao(self):
        """Exibe a pontuação atual."""
        texto_pontuacao = self.fontes["media"].render(
            f"Pontuação: {self.pontuacao}", True, (255, 255, 255)
        )
        self.screen.blit(texto_pontuacao, (50, 30))

    def _finalizar_jogo(self):
        """Finaliza o jogo, salva a pontuação e exibe a tela de Game Over."""
        self.leaderboard.salvar_leaderboard(self.jogador.nome, self.pontuacao)
        self.game_over.exibir(self.pontuacao, lambda: self.jogador.registrar_nome())
