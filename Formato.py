import pygame
import random
import time
import os
import sys
#Definindo possiveis formatos do jogo
FORMATOS = {
    'Quadrado': [[1, 1],
               [1, 1]],
    'horizontal': [[1, 1, 1, 1]],
    'vertical': [[1],
                [1],
                [1],
                [1]],
    'LEsquerda': [[1, 0, 0],
              [1, 1, 1]],
    'LDireita': [[0, 0, 1],
               [1, 1, 1]],
    'ZDireita': [[0, 1, 1],
               [1, 1, 0]],
    'ZEsquerda': [[1, 1, 0],
              [0, 1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]]
}
FORMATOS_list = list(FORMATOS.values())


class Formato:
    def __init__(self):
        self.x = 6        #posicao mais a esquerda do formato no grid
        self.y = 0        #posicao mais acima do formato no grid
        self.cor = random.randint(1,7)         #um inteiro que refere a uma serie de cores pre-definidas
        self.contador = 0
        self.formato = random.choice(FORMATOS_list) #formato sorteado aleatoriamente(matriz)
        self.altura = len(self.formato)
        self.largura = len(self.formato[0])

    def move_esquerda(self, grid):
        if self.x > 0 and self.pode_mover(grid, dx=-1):
            self.x -= 1

    def move_direita(self, grid):
        if self.x < 13 - self.largura and self.pode_mover(grid, dx=1):
            self.x += 1

    def fixa_formato(self, grid):
        for y in range(self.altura):
            for x in range(self.largura):
                if self.formato[y][x] == 1:
                    grid[self.y + y][self.x + x] = self.cor

    def apaga_formato(self, grid):
        for y in range(self.altura):
            for x in range(self.largura):
                if self.formato[y][x] == 1:
                    grid[self.y + y][self.x + x] = 0

    def pode_mover(self, grid, dy=1, dx=0):
        for y in range(self.altura):
            for x in range(self.largura):
                if self.formato[y][x] == 1:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    # Verifica se os índices estão dentro dos limites da grid
                    if new_x < 0 or new_x >= len(grid[0]) or new_y < 0 or new_y >= len(grid):
                        print(f"Erro de movimentação: ({new_x}, {new_y}) fora dos limites")
                        return False
                    if grid[new_y][new_x] != 0:
                        return False
        return True

    def rotaciona(self, grid):
        global rodar
        self.contador += 1
        if self.contador > 10:
            rodar = True

        # Gera o formato rotacionado
        rotated_shape = list(zip(*self.formato[::-1]))  # Rotação de 90 graus
        rotated_shape = [list(row) for row in rotated_shape]
        new_altura = len(rotated_shape)
        new_largura = len(rotated_shape[0])

        # Ajusta a posição se a rotação ultrapassar os limites horizontais
        if self.x + new_largura > len(grid[0]):  # Limite direito
            self.x = len(grid[0]) - new_largura
        elif self.x < 0:  # Limite esquerdo
            self.x = 0

        # Ajusta a posição se a rotação ultrapassar os limites verticais
        if self.y + new_altura > len(grid):  # Limite inferior
            self.y = len(grid) - new_altura
        elif self.y < 0:  # Limite superior
            self.y = 0

        # Confere colisão com outras peças
        for y in range(new_altura):
            for x in range(new_largura):
                if rotated_shape[y][x] == 1:
                    new_x = self.x + x
                    new_y = self.y + y
                    if new_y >= len(grid) or new_x >= len(grid[0]) or new_y < 0 or new_x < 0:
                        return  # Colisão ou fora do grid
                    if grid[new_y][new_x] != 0:
                        return  # Colisão com outra peça

        # Apaga o formato antigo, aplica a rotação e desenha o novo formato
        self.apaga_formato(grid)
        self.formato = rotated_shape
        self.altura = new_altura
        self.largura = new_largura
        
