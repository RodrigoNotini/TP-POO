import pygame
import sys
from telas import Detalhes, Creditos, GameOver, Pause
from utils.constantes import LARGURA, ALTURA
from menu import Menu
from leaderboard import LeaderBoard


def carregar_imagens():
    """Carrega e redimensiona as imagens necessárias."""
    try:
        menu_bg = pygame.image.load("./src/images/menu_bg.jpg")
        menu_bg = pygame.transform.scale(menu_bg, (LARGURA, ALTURA))
        game_bg = pygame.image.load("./src/images/game_bg.png")
        game_bg = pygame.transform.scale(game_bg, (LARGURA, ALTURA))
        return {"menu_bg": menu_bg, "game_bg": game_bg}
    except pygame.error as e:
        print(f"Erro ao carregar imagens: {e}")
        sys.exit()


def carregar_fontes():
    """Inicializa e retorna as fontes usadas no jogo."""
    try:
        pygame.font.init()
        return {
            "titulo": pygame.font.SysFont("fixedsys", 44),
            "grande": pygame.font.SysFont("fixedsys", 32),
            "media": pygame.font.SysFont("fixedsys", 24),
            "pequena": pygame.font.SysFont("fixedsys", 18),
        }
    except pygame.error as e:
        print(f"Erro ao carregar fontes: {e}")
        sys.exit()


def inicializar():
    """Inicializa o Pygame e carrega recursos essenciais."""
    pygame.init()

    imagens = carregar_imagens()
    fontes = carregar_fontes()

    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("TETRIS")
    clock = pygame.time.Clock()

    return {"screen": screen, "clock": clock, "imagens": imagens, "fontes": fontes}


def main():
    # Inicializa recursos
    recursos = inicializar()
    screen = recursos["screen"]
    imagens = recursos["imagens"]
    fontes = recursos["fontes"]

    # Instancia o LeaderBoard
    leaderboard = LeaderBoard("Leaderboard do Tetris")

    # Instancia as telas
    menu = Menu(screen, fontes, imagens, leaderboard)
    detalhes = Detalhes(screen, fontes, imagens)
    creditos = Creditos(screen, fontes, imagens)
    pause = Pause(screen, fontes, imagens)
    game_over = GameOver(screen, fontes, imagens, leaderboard)

    # Estado inicial
    jogando = False
    pontuacao = 0

    # Exibe o menu principal
    menu.exibir_menu(detalhes, creditos)

    while True:
        # Inicia o jogo (lógica do loop do jogo será integrada aqui futuramente)
        jogando = True
        nome_jogador = "PLAYER"  # Exemplo de nome para o jogador (adicionar registro no futuro)

        while jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:
                        pause.exibir(lambda: None)  # Lógica para continuar será integrada aqui futuramente

            # Simulação de lógica do jogo
            pontuacao += 1
            if pontuacao > 500:  # Exemplo de fim de jogo
                leaderboard.salvar_leaderboard(nome_jogador, pontuacao)  # Salva a pontuação
                game_over.exibir(pontuacao, main)  # Reinicia o jogo ao clicar em "Reiniciar"
                jogando = False

            # Atualiza a tela (placeholder)
            screen.fill((0, 0, 0))
            pygame.display.update()


if __name__ == "__main__":
    main()
