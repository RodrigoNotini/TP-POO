import pygame
import random
import time
import os
import sys
from Desenhos import *

# Arquivo do leaderboard
LEADERBOARD_FILE = "leaderboard.txt"


 #Definindo telas, que interagem com a main
def main_menu_screen():
    global run, ja_executou, nome
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("APERTE ESPACO PARA COMECAR", fonte_media, (255,255,255), screen, LARGURA//2, 150, centro=True)
        render_text("HIGHSCORES", fonte_grande, (255,255,255), screen, LARGURA//2, 200, centro=True)
        leaderboard = carrega_leaderboard()
        for idx, (player, pts) in enumerate(leaderboard):
            render_text(f"{player}: {pts}", fonte_media, (255,255,255), screen, 90, 280 + idx*30)
        # Controles
        controls = "CONTROLES:\n← or a PARA ESQUERDA\n→ or d PARA DIREITA\n↑ or w PARA ROTACIONAR\np PARA PAUSAR O JOGO\n(O JOGO INICIA EM 3 SEGUNDOS APOS DESPAUSAR)"
        controls_lines = controls.split('\n')
        for i, line in enumerate(controls_lines):
            render_text(line, fonte_pequena, (255,255,255), screen, 50, 650 + i*20)
        # Botoes para creditos e detalhes
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        # Botao Creditos
        if 20 <= mouse[0] <= 120 and 468 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100,100,100), (20,468,100,32))
            if click:
                tela_creditos()
        else:
            pygame.draw.rect(screen, (150,150,150), (20,468,100,32))
        render_text("CREDITS", fonte_media, (0,0,0), screen, 70, 480, centro=True)
        # Botao Detalhes
        if 280 <= mouse[0] <= 380 and 468 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100,100,100), (280,468,100,32))
            if click:
                tela_detalhes()
        else:
            pygame.draw.rect(screen, (150,150,150), (280,468,100,32))
        render_text("DETAILS", fonte_media, (0,0,0), screen, 330, 480, centro=True)
        pygame.display.update()
        clock.tick(FPS)

def tela_creditos():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("FEITO POR:", fonte_grande, (255,255,255), screen, 40, 320)
        render_text("Rodrigo, Gabriel e Pedro", fonte_grande, (255,255,255), screen, 40, 350)
        # Botao Voltar
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        if 160 <= mouse[0] <= 240 and 470 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100,100,100), (160,470,80,30))
            if click:
                return
        else:
            pygame.draw.rect(screen, (150,150,150), (160,470,80,30))
        render_text("DONE", fonte_media, (0,0,0), screen, 200, 485, centro=True)
        pygame.display.update()
        clock.tick(FPS)

def tela_detalhes():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        # Objetivo do jogo
        render_text("OBJETIVO DO JOGO", fonte_grande, (255,255,255), screen, 35, 50)
        objective = ("No Tetris, seu objetivo é empilhar blocos\nem multiplas linhas e destruir eles\n\nUma linha e destruida quando ela esta\n\n"
                     "Colete o maximo de pontos possiveis antes que o\njogo acabe para garantir seu lugar\nna leaderboard.\n\n"
                     "Destruir cada linha faz gera um total de 100 pontos")
        linhas_objetivos = objective.split('\n')
        for i, line in enumerate(linhas_objetivos):
            render_text(line, fonte_pequena, (255,255,255), screen, 35, 80 + i*20)
        # Obstaculos do jogo
        render_text("OBSTACULOS", fonte_grande, (255,255,255), screen, 35, 270)
        obstacles = ("Ao longo do jogo voce sera desafiado\ncom certos obstaculos.\n\nA cada 300"
                     "pontos,o jogo vai ficar mais rapido.\n\nA cada 500 pontos, uma linha indestrutivel "
                     "sera adicionada no fundo da grid,\no que diminuira o seu espaço")
        obstacles_lines = obstacles.split('\n')
        for i, line in enumerate(obstacles_lines):
            render_text(line, fonte_pequena, (255,255,255), screen, 35, 300 + i*20)
        # Cheats
        render_text("CHEATS", fonte_grande, (255,255,255), screen, 120, 470)
        cheats = ("Aperte 'x' para passar o bloco que esta vindo.\n\nAperte 'z' para desacelerar o jogo.\n"
                  "(Efeitos especiais na pontuacao>300)\n\nAperte 'c' para destruir a linha mais ao fundo\n\nAperte 'ESC' "
                  "para ativar a tecla do chefe.")
        cheats_lines = cheats.split('\n')
        for i, line in enumerate(cheats_lines):
            render_text(line, fonte_pequena, (255,255,255), screen, 25, 500 + i*20)
        # Botao Voltar
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        if 160 <= mouse[0] <= 240 and 655 <= mouse[1] <= 685:
            pygame.draw.rect(screen, (100,100,100), (160,655,80,30))
            if click:
                return
        else:
            pygame.draw.rect(screen, (150,150,150), (160,655,80,30))
        render_text("VOLTAR", fonte_media, (0,0,0), screen, 200, 670, centro=True)
        pygame.display.update()
        clock.tick(FPS)

def tela_registro_nome():
    global nome, ja_executou
    ativo = True
    input_usuario = ''
    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if len(input_usuario) ==3:
                        nome = input_usuario
                        ja_executou = True
                        ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    input_usuario = input_usuario[:-1]
                else:
                    if len(input_usuario) <3 and evento.unicode.isalnum():
                        input_usuario += evento.unicode.upper()
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("DIGITE SEU NOME", fonte_grande, (255,255,255), screen, LARGURA//2, 400, centro=True)
        render_text("(APENAS 3 LETRAS)", fonte_pequena, (255,255,255), screen, LARGURA//2, 450, centro=True)
        # Caixa de input
        pygame.draw.rect(screen, (255,255,255), (LARGURA//2 -50, 500, 100, 40),2)
        render_text(input_usuario, fonte_grande, (255,255,255), screen, LARGURA//2, 520, centro=True)
        pygame.display.update()
        clock.tick(FPS)

def tela_game_over():
    global pontos, nome
    salva_leaderboard(nome, pontos)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0,0,0))
        screen.blit(BG_IMAGE, (0,0))
        render_text("Game Over!", fonte_grande, (255,0,0), screen, LARGURA//2, 300, centro=True)
        render_text(f"Pontuação: {pontos}", fonte_media, (255,255,255), screen, LARGURA//2, 350, centro=True)
        render_text("Pressione Enter para reiniciar", fonte_pequena, (255,255,255), screen, LARGURA//2, 400, centro=True)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            main()

def tela_pause():
    global pause, p
    pause_menu = True
    while pause_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Detecta se a tecla 'p' foi pressionada
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                # Atraso de 3 segundos antes de retomar o jogo
                time.sleep(3)
                pause_menu = False  # Sai do loop de pausa
                pause = False       # Desativa o estado de pausa
                p = 1               # Define a variável auxiliar

        # Renderização da tela de pausa
        screen.fill((0, 0, 0))
        render_text("PAUSADO", fonte_grande, (255, 255, 255), screen, LARGURA // 2, 400, centro=True)
        render_text("PRESSIONE 'p' PARA CONTINUAR.\nVOCE TERA\n3 SEGUNDOS PARA\n     VOLTAR AO JOGO.", fonte_pequena, (255, 255, 255), screen, LARGURA // 2, 450, centro=True)
        pygame.display.update()

        clock.tick(FPS)


def main():
    global delay, grid, pontos, run, pause, p, rodar, evento_limpar, primeira_execucao, nome, ja_executou
    run = True
    pause = False
    p =0
    rodar = False
    evento_limpar = False
    pontos =0
    grid = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,0,0,0,0,0,0,0,0,0,0,0,0,8],
        [8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    ]
    shape = Formato()
    nshape = Formato()
    pause = False
    primeira_execucao = True
    while run:
        for event in pygame.event.get():      #Define as repostas as teclas pressionadas chamando funcoes
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    shape.move_esquerda(grid)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    shape.move_direita(grid)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    shape.rotaciona(grid)
                if event.key == pygame.K_p:
                    pause = True
                if event.key == pygame.K_x:      #tecla para pular peca
                    nshape = Formato()
                if event.key == pygame.K_z:      #tecla para diminuir a velocidade de queda das pecas
                    delay =0.10
                if event.key == pygame.K_c:
                    # Limpa a penultima linha e acresenta 100 pontos
                    for x in range(len(grid[-2])):
                        grid[-2][x] =0
                    pontos +=100
        if not pause:
            if shape.y ==23 - shape.altura +1 or not shape.pode_mover(grid):
                if shape.y ==0:
                    tela_game_over()                                            #Se a peça mais "alta" do formato estiver na posicao 0, usuario perde o jogo
                else:
                    shape.fixa_formato(grid)
                    shape = nshape                                          #Se a peca nao pode mover, ela e fixada e uma nova peca e gerada
                    nshape = Formato()
                    del_linha(grid)
            if shape.pode_mover(grid):
                shape.y +=1                                                #Faz a peca se mover verticalmente
            else:
                shape.fixa_formato(grid)
                shape = nshape
                nshape = Formato()
                del_linha(grid)
            pontos +=1
            desenha_grid_pygame(grid,shape,nshape)
            pygame.display.update()
            time.sleep(delay)                                           #Delay entre as pecas, atualizacoes da tela
        else:
            pause=True
            tela_pause()
        clock.tick(FPS)

# Start the game
def start_game():
    main_menu_screen()
    tela_registro_nome()
    main()

if __name__ == "__main__":
    start_game()
