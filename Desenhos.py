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
                rect = pygame.Rect(direita + x*BLOCK_SIZE, topo + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)   #Pos na tela por tam horizontal e vertical
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (40,40,40), rect,1) 

#Desenha a grid completa, com peças e pontuação
def desenha_grid_pygame(grid, proximo_formato):
    screen.blit(BG_IMAGE, (0,0))                                     #copia a imagem de fundo para a tela

    # Desenha a grade
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color_num = grid[y][x]  
            color = CORES[color_num]
            pygame.draw.rect(screen, color, (110 + x*BLOCK_SIZE, 200 + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))             #preenche o bloco
            pygame.draw.rect(screen, (40,40,40), (110 + x*BLOCK_SIZE, 200 + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),1)      #preenche a borda do bloco    

    # Desenha o formato 
    desenha_formato(proximo_formato)

    # Desenha pontuacao
    texto_pontuacao = fonte_media.render(f"Pontuação: {pontos}", True, (255,255,255))
    screen.blit(texto_pontuacao, (50, 30))


def del_linha(grid):
    global delay, pontos, evento_limpar
    linhas_deletar = []
    for y in range(len(grid)):                                  #Verifica se a linha esta cheia, se estiver adiciona na lista para deletar
        if all(cell !=0 and cell !=9 for cell in grid[y]):
            linhas_deletar.append(y)

    for y in linhas_deletar:
        del grid[y]
        grid.insert(0, [8]+[0]*12+[8])                          #Deleta as linhas cheias e adiciona uma nova linha vazia
        pontos += 100
        if pontos % 300 ==0 and delay >0.01:
            delay -=0.01                                         #Diminui o delay a cada 300 pontos
        if pontos %500 ==0 and pontos !=0:
            grid.pop(-2)                                         #Insere uma linha indestrutivel a cada 500 pontos
            grid.insert(1, [8]*14)
            pontos +=100