import pygame
import random
import time
import os
import sys
from Constantes import *


# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

# Carrega Imagens
try:
    BG_IMAGE = pygame.image.load('bg.png')
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (LARGURA, ALTURA))
except pygame.error as e:
    print(f"Error loading bg.png: {e}")
    sys.exit()

# Inicializa tela
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("TETRIS")
clock = pygame.time.Clock()
