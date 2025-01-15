class Tabuleiro:
    def __init__(self, largura=14, altura=21):
        """
        Inicializa o tabuleiro com a matriz (grid) e dimensões.
        """
        self.largura = largura
        self.altura = altura
        self.grid = self._criar_grid()

    def _criar_grid(self):
        """
        Cria um grid inicial, com bordas indestrutíveis.
        """
        grid = [[8] + [0] * (self.largura - 2) + [8] for _ in range(self.altura - 1)]
        grid.append([8] * self.largura)  # Linha inferior indestrutível
        return grid

    def remover_linhas_completas(self):
        """
        Remove linhas completas do grid e adiciona novas no topo.
        """
        linhas_removidas = 0
        for y in range(len(self.grid) - 1):  # Ignora a linha inferior indestrutível
            if all(celula != 0 and celula != 8 for celula in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [8] + [0] * (self.largura - 2) + [8])
                linhas_removidas += 1
        return linhas_removidas

    def adicionar_peca(self, peca):
        """
        Adiciona a peça fixa ao grid.
        """
        peca.fixa_formato(self.grid)

    def desenhar(self, superficie, desenho_func):
        """
        Renderiza o grid na tela usando a função de desenho.
        """
        desenho_func(self.grid, superficie)