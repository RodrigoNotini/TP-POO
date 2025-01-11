import pygame
import sys
from Constantes import *


# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

# Carrega Imagens
try:
    MENU_BG_IMAGE = pygame.image.load("./images/menu_bg.jpg")  # For the menu
    MENU_BG_IMAGE = pygame.transform.scale(MENU_BG_IMAGE, (LARGURA, ALTURA))
    GAME_BG_IMAGE = pygame.image.load("./images/game_bg.png")
    GAME_BG_IMAGE = pygame.transform.scale(GAME_BG_IMAGE, (LARGURA, ALTURA))
except pygame.error as e:
    print(f"Erro ao carregar imagens de fundo: {e}")
    sys.exit()

# Inicializa tela
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("TETRIS")
clock = pygame.time.Clock()
