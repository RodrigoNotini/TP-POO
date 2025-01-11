import pygame
import random
import time
import os
import sys
from Cores import *
from Constantes import *
from Carrega import *
from Fontes import *
from Globais import *
from Formato import *
from Leaderboard import *


# Desenha o formato da peça
def desenha_formato(formato):
    topo = 100
    direita = 200
    for y in range(formato.altura):
        for x in range(formato.largura):
            if formato.formato[y][x] == 1:
                color = CORES[formato.cor]
                rect = pygame.Rect(
                    direita + x * BLOCK_SIZE,
                    topo + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )  # Pos na tela por tam horizontal e vertical
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)


# Desenha a grid completa, com peças e pontuação
def desenha_grid_pygame(grid, shape, proximo_formato):
    screen.blit(BG_IMAGE, (0, 0))  # Copia a imagem de fundo para a tela

    # Desenha a grade
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color_num = grid[y][x]
            color = CORES[color_num]
            pygame.draw.rect(
                screen,
                color,
                (110 + x * BLOCK_SIZE, 200 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            )  # Preenche o bloco
            pygame.draw.rect(
                screen,
                (40, 40, 40),
                (110 + x * BLOCK_SIZE, 200 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1,
            )  # Preenche a borda

    # Desenha a peça atual na posição correta
    for y in range(shape.altura):
        for x in range(shape.largura):
            if shape.formato[y][x] == 1:
                color = CORES[shape.cor]
                rect = pygame.Rect(
                    110 + (shape.x + x) * BLOCK_SIZE,
                    200 + (shape.y + y) * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(screen, color, rect)  # Preenche o bloco da peça
                pygame.draw.rect(
                    screen, (40, 40, 40), rect, 1
                )  # Preenche a borda do bloco da peça

    # Desenha o próximo formato em uma área separada
    topo_proximo = 100
    direita_proximo = 400
    for y in range(proximo_formato.altura):
        for x in range(proximo_formato.largura):
            if proximo_formato.formato[y][x] == 1:
                color = CORES[proximo_formato.cor]
                rect = pygame.Rect(
                    direita_proximo + x * BLOCK_SIZE,
                    topo_proximo + y * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    # Desenha a pontuação
    texto_pontuacao = fonte_media.render(f"Pontuação: {pontos}", True, (255, 255, 255))
    screen.blit(texto_pontuacao, (50, 30))


def del_linha(grid):
    global delay, pontos, evento_limpar
    linhas_deletar = []

    # Identifica as linhas que precisam ser deletadas
    for y in range(len(grid)):
        if all(cell != 0 and cell != 9 for cell in grid[y]):
            linhas_deletar.append(y)

    # Deleta as linhas de forma segura
    for y in sorted(linhas_deletar, reverse=True):
        del grid[y]

    # Insere novas linhas no topo
    for _ in linhas_deletar:
        grid.insert(0, [8] + [0] * 12 + [8])

    # Atualiza pontuação e dificuldade
    pontos += len(linhas_deletar) * 100
    if pontos % 300 == 0 and delay > 0.01:
        delay -= 0.01

    # Adiciona linha indestrutível a cada 500 pontos
    if pontos % 500 == 0 and pontos != 0:
        grid.pop(-2)  # Remove a penúltima linha
        grid.insert(1, [8] * 14)  # Insere linha indestrutível
        pontos += 100
