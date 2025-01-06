from Globais import *
import pygame
import random
import time
import os
import sys

# Arquivo do leaderboard
LEADERBOARD_FILE = "leaderboard.txt"


def del_linha(grid):
    global delay, pontos, evento_limpar
    linhas_deletar = []
    for y in range(len(grid)):                            #Verifica se a linha esta cheia, se estiver adiciona na lista para deletar
        if all(cell !=0 and cell !=9 for cell in grid[y]):
            linhas_deletar.append(y)

    for y in linhas_deletar:
        del grid[y]
        grid.insert(0, [8]+[0]*12+[8])                   #Deleta as linhas cheias e adiciona uma nova linha vazia
        pontos += 100
        if pontos % 300 ==0 and delay >0.01:
            delay -=0.01                                 #Diminui o delay a cada 300 pontos
        if pontos %500 ==0 and pontos !=0:
            grid.pop(-2)                                #Insere uma linha indestrutivel a cada 500 pontos
            grid.insert(1, [8]*14)
            pontos +=100

def carrega_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):            #Cria LeaderBoard, separando nome de pontuação por vírgulas
        with open(LEADERBOARD_FILE, 'w') as f:
            f.write("AAA,100,BBB,90,CCC,80,DDD,70,EEE,60")
    with open(LEADERBOARD_FILE, 'r') as f:
        data = f.read().strip().split(',')
    leaderboard = []
    for i in range(0, len(data),2):
        try:
            leaderboard.append((data[i], int(data[i+1])))
        except IndexError:
            continue
    return leaderboard

def salva_leaderboard(nome, pontuacao):
    leaderboard = carrega_leaderboard()
    leaderboard.append((nome, pontuacao))
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:5]       #Seleciona apenas as 5 maiores pontuações no leaderboard e coloca elas no arquivo do LEADERBOARD
    with open(LEADERBOARD_FILE, 'w') as f:
        for entry in leaderboard:
            f.write(f"{entry[0]},{entry[1]},")

def render_text(texto, fonte, cor, superficie, x, y, centro=False):
    lines = texto.split('\n')
    for i, line in enumerate(lines):
        textobj = fonte.render(line, True, cor)
        textrect = textobj.get_rect()
        if centro:                                                  #Permite renderizar textos com varias linhas
            textrect.center = (x, y + i * 20)
        else:
            textrect.topleft = (x, y + i * 20)
        superficie.blit(textobj, textrect)