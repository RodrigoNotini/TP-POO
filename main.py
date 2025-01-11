import pygame
import random
import time
import os
import sys
from Desenhos import *

# Arquivo do leaderboard
LEADERBOARD_FILE = "leaderboard.txt"


# Função que exibe a tela principal do menu.
# Permite ao usuário visualizar os highscores, controles e navegar para outras telas (créditos, detalhes).
def main_menu_screen():
    global run, ja_executou, nome
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Pressionar espaço inicia o jogo
                    return
        # Renderização da tela principal do menu
        screen.fill((0, 0, 0))
        screen.blit(BG_IMAGE, (0, 0))
        render_text(
            "APERTE ESPACO PARA COMECAR",
            fonte_media,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            150,
            centro=True,
        )
        render_text(
            "HIGHSCORES",
            fonte_grande,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            200,
            centro=True,
        )

        # Exibição do leaderboard
        leaderboard = carrega_leaderboard()
        for idx, (player, pts) in enumerate(leaderboard):
            render_text(
                f"{player}: {pts}",
                fonte_media,
                (255, 255, 255),
                screen,
                90,
                280 + idx * 30,
            )

        # Exibição dos controles do jogo
        controls = "CONTROLES:\n← or a PARA ESQUERDA\n→ or d PARA DIREITA\n↑ or w PARA ROTACIONAR\np PARA PAUSAR O JOGO\n(O JOGO INICIA EM 3 SEGUNDOS APOS DESPAUSAR)"
        controls_lines = controls.split("\n")
        for i, line in enumerate(controls_lines):
            render_text(line, fonte_pequena, (255, 255, 255), screen, 50, 650 + i * 20)

        # Botões interativos (créditos e detalhes)
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True

        # Botão "CREDITS"
        if 20 <= mouse[0] <= 120 and 468 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100, 100, 100), (20, 468, 100, 32))
            if click:
                tela_creditos()
        else:
            pygame.draw.rect(screen, (150, 150, 150), (20, 468, 100, 32))
        render_text("CREDITS", fonte_media, (0, 0, 0), screen, 70, 480, centro=True)

        # Botão "DETAILS"
        if 280 <= mouse[0] <= 380 and 468 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100, 100, 100), (280, 468, 100, 32))
            if click:
                tela_detalhes()
        else:
            pygame.draw.rect(screen, (150, 150, 150), (280, 468, 100, 32))
        render_text("DETAILS", fonte_media, (0, 0, 0), screen, 330, 480, centro=True)

        pygame.display.update()
        clock.tick(FPS)


# Função que exibe a tela de créditos.
# Mostra os criadores do jogo e possui um botão "DONE" para voltar ao menu anterior.
def tela_creditos():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.fill((0, 0, 0))
        screen.blit(BG_IMAGE, (0, 0))
        render_text("FEITO POR:", fonte_grande, (255, 255, 255), screen, 40, 320)
        render_text(
            "Rodrigo, Gabriel e Pedro", fonte_grande, (255, 255, 255), screen, 40, 350
        )

        # Botão "DONE"
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        if 160 <= mouse[0] <= 240 and 470 <= mouse[1] <= 500:
            pygame.draw.rect(screen, (100, 100, 100), (160, 470, 80, 30))
            if click:
                return
        else:
            pygame.draw.rect(screen, (150, 150, 150), (160, 470, 80, 30))
        render_text("DONE", fonte_media, (0, 0, 0), screen, 200, 485, centro=True)

        pygame.display.update()
        clock.tick(FPS)


# Função que exibe os detalhes do jogo.
# Mostra o objetivo, os obstáculos e possíveis cheats para o jogador.
def tela_detalhes():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.fill((0, 0, 0))
        screen.blit(BG_IMAGE, (0, 0))

        # Objetivo do jogo
        render_text("OBJETIVO DO JOGO", fonte_grande, (255, 255, 255), screen, 35, 50)
        objective = (
            "No Tetris, seu objetivo é empilhar blocos\nem multiplas linhas e destruir eles\n\nUma linha e destruida quando ela esta\n\n"
            "Colete o maximo de pontos possiveis antes que o\njogo acabe para garantir seu lugar\nna leaderboard.\n\n"
            "Destruir cada linha faz gera um total de 100 pontos"
        )
        objective_lines = objective.split("\n")
        for i, line in enumerate(objective_lines):
            render_text(line, fonte_pequena, (255, 255, 255), screen, 35, 80 + i * 20)

        # Obstáculos do jogo
        render_text("OBSTACULOS", fonte_grande, (255, 255, 255), screen, 35, 270)
        obstacles = (
            "Ao longo do jogo voce sera desafiado\ncom certos obstaculos.\n\nA cada 300"
            "pontos,o jogo vai ficar mais rapido.\n\nA cada 500 pontos, uma linha indestrutivel "
            "sera adicionada no fundo da grid,\no que diminuira o seu espaço"
        )
        obstacles_lines = obstacles.split("\n")
        for i, line in enumerate(obstacles_lines):
            render_text(line, fonte_pequena, (255, 255, 255), screen, 35, 300 + i * 20)

        # Cheats
        render_text("CHEATS", fonte_grande, (255, 255, 255), screen, 120, 470)
        cheats = (
            "Aperte 'x' para passar o bloco que esta vindo.\n\nAperte 'z' para desacelerar o jogo.\n"
            "(Efeitos especiais na pontuacao>300)\n\nAperte 'c' para destruir a linha mais ao fundo\n\nAperte 'ESC' "
            "para ativar a tecla do chefe."
        )
        cheats_lines = cheats.split("\n")
        for i, line in enumerate(cheats_lines):
            render_text(line, fonte_pequena, (255, 255, 255), screen, 25, 500 + i * 20)

        # Botão "DONE"
        mouse = pygame.mouse.get_pos()
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        if 160 <= mouse[0] <= 240 and 655 <= mouse[1] <= 685:
            pygame.draw.rect(screen, (100, 100, 100), (160, 655, 80, 30))
            if click:
                return
        else:
            pygame.draw.rect(screen, (150, 150, 150), (160, 655, 80, 30))
        render_text("DONE", fonte_media, (0, 0, 0), screen, 200, 670, centro=True)

        pygame.display.update()
        clock.tick(FPS)


# Função para registrar o nome do jogador.
# Limita o nome a 3 caracteres e permite apenas caracteres alfanuméricos.
def tela_registro_nome():
    global nome, ja_executou
    ativo = True
    input_usuario = ""
    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if len(input_usuario) == 3:
                        nome = input_usuario
                        ja_executou = True
                        ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    input_usuario = input_usuario[:-1]
                else:
                    if len(input_usuario) < 3 and evento.unicode.isalnum():
                        input_usuario += evento.unicode.upper()

        # Renderização da tela de registro do nome
        screen.fill((0, 0, 0))
        screen.blit(BG_IMAGE, (0, 0))
        render_text(
            "DIGITE SEU NOME",
            fonte_grande,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            400,
            centro=True,
        )
        render_text(
            "(APENAS 3 LETRAS)",
            fonte_pequena,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            450,
            centro=True,
        )

        # Caixa de input
        pygame.draw.rect(screen, (255, 255, 255), (LARGURA // 2 - 50, 500, 100, 40), 2)
        render_text(
            input_usuario,
            fonte_grande,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            520,
            centro=True,
        )

        pygame.display.update()
        clock.tick(FPS)


def tela_game_over():
    """
    Função responsável por exibir a tela de "Game Over".
    Salva a pontuação na leaderboard e aguarda interação do jogador para reiniciar o jogo.
    """
    global pontos, nome
    salva_leaderboard(nome, pontos)  # Salva os dados na leaderboard.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Detecta se o jogador fechou o jogo.
                pygame.quit()
                sys.exit()
        # Renderiza a tela de "Game Over".
        screen.fill((0, 0, 0))
        screen.blit(BG_IMAGE, (0, 0))
        render_text(
            "Game Over!",
            fonte_grande,
            (255, 0, 0),
            screen,
            LARGURA // 2,
            300,
            centro=True,
        )
        render_text(
            f"Pontuação: {pontos}",
            fonte_media,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            350,
            centro=True,
        )
        render_text(
            "Pressione Enter para reiniciar",
            fonte_pequena,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            400,
            centro=True,
        )
        pygame.display.update()

        # Verifica se a tecla Enter foi pressionada para reiniciar o jogo.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            main()


def tela_pause():
    """
    Função responsável por exibir a tela de pausa e gerenciar o retorno ao jogo.
    O jogador tem 3 segundos antes do jogo ser retomado.
    """
    global pause, p
    pause_menu = True
    while pause_menu:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
            ):  # Encerra o jogo caso o jogador feche a janela.
                pygame.quit()
                sys.exit()

            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_p
            ):  # Detecta a tecla 'p' para sair da pausa.
                time.sleep(3)  # Pausa de 3 segundos antes de retomar o jogo.
                pause_menu = False  # Sai do menu de pausa.
                pause = False  # Desativa o estado de pausa.
                p = 1  # Variável auxiliar usada para controle.

        # Renderiza a tela de pausa.
        screen.fill((0, 0, 0))
        render_text(
            "PAUSADO",
            fonte_grande,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            400,
            centro=True,
        )
        render_text(
            "PRESSIONE 'p' PARA CONTINUAR.\nVOCE TERA\n3 SEGUNDOS PARA\n     VOLTAR AO JOGO.",
            fonte_pequena,
            (255, 255, 255),
            screen,
            LARGURA // 2,
            450,
            centro=True,
        )
        pygame.display.update()
        clock.tick(FPS)


def main():
    """
    Função principal do jogo.
    Gerencia o loop do jogo, controle de eventos e lógica principal, como movimento e fixação de peças.
    """
    global delay, grid, pontos, run, pause, p, rodar, evento_limpar, primeira_execucao, nome, ja_executou
    # Variáveis de controle e inicialização.
    run = True
    pause = False
    p = 0
    rodar = False
    evento_limpar = False
    pontos = 0
    grid = [  # Matriz representando o tabuleiro do jogo.
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    ]
    shape = Formato()  # Peça atual.
    nshape = Formato()  # Próxima peça.
    primeira_execucao = True

    while run:
        for event in pygame.event.get():  # Verifica eventos, como teclas pressionadas.
            if event.type == pygame.QUIT:  # Fecha o jogo.
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    shape.move_esquerda(grid)  # Move peça para a esquerda.
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    shape.move_direita(grid)  # Move peça para a direita.
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    shape.rotaciona(grid)  # Rotaciona a peça.
                if event.key == pygame.K_p:
                    pause = True  # Ativa o modo de pausa.
                if event.key == pygame.K_x:  # Pula para a próxima peça.
                    nshape = Formato()
                if event.key == pygame.K_z:  # Diminui a velocidade de queda.
                    delay = 0.20
                if event.key == pygame.K_c:
                    # Limpa a penúltima linha e adiciona 100 pontos.
                    for x in range(len(grid[-2])):
                        grid[-2][x] = 0
                    pontos += 100

        if not pause:  # Continua o jogo se não estiver em pausa.
            if shape.y == 23 - shape.altura + 1 or not shape.pode_mover(grid):
                if (
                    shape.y == 0
                ):  # Verifica se a peça alcançou o topo, encerrando o jogo.
                    tela_game_over()
                else:
                    shape.fixa_formato(grid)  # Fixa a peça na posição final.
                    shape = nshape  # Gera nova peça.
                    nshape = Formato()
                    del_linha(grid)  # Remove linhas completas.
            if shape.pode_mover(grid):  # Move a peça para baixo se possível.
                shape.y += 1
            else:
                shape.fixa_formato(grid)
                shape = nshape
                nshape = Formato()
                del_linha(grid)
            pontos += 1  # Incrementa pontuação.
            desenha_grid_pygame(grid, shape, nshape)  # Atualiza a interface.
            pygame.display.update()
            time.sleep(delay)  # Atraso entre atualizações.
        else:
            pause = True
            tela_pause()
        clock.tick(FPS)


def start_game():
    """
    Função inicial que exibe o menu principal, registra o nome do jogador e inicia o jogo.
    """
    main_menu_screen()
    tela_registro_nome()
    main()


if __name__ == "__main__":
    start_game()
