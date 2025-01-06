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

    def colorir_formato(self, grid):
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
                    if new_x < 0 or new_x >= 14 or new_y >= 24:
                        return False
                    if grid[new_y][new_x] != 0:
                        return False
        return True

    def rotaciona(self, grid):
        global rodar
        self.contador +=1
        if self.contador >10:
            rodar = True
        rotated_shape = list(zip(*self.formato[::-1]))        #Representa uma rotação de 90 graus
        rotated_shape = [list(row) for row in rotated_shape]
        new_altura = len(rotated_shape)
        new_largura = len(rotated_shape[0])
        if self.x + new_largura > 14:
            return
        # Confere colisão
        for y in range(new_altura):
            for x in range(new_largura):
                if rotated_shape[y][x] == 1:
                    if self.y + y >= len(grid) or self.x + x >= len(grid[0]) or self.y + y < 0 or self.x + x <0:
                        return
                    if grid[self.y + y][self.x + x] !=0:
                        return
        self.apaga_formato(grid)
        self.formato = rotated_shape
        self.altura = new_altura
        self.largura = new_largura
        self.colorir_formato(grid)