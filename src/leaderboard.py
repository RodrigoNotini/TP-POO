import json
import os

# Arquivo do leaderboard
LEADERBOARD_FILE = "./src/leaderboard.json"


class LeaderBoard:
    def __init__(self, nome):
        self.nome = nome

    def _inicializar_arquivo(self):
        """Cria o arquivo JSON se não existir, com dados iniciais."""
        if not os.path.exists(LEADERBOARD_FILE):
            data_inicial = [
                {"nome": "LAURA", "pontuacao": 100},
                {"nome": "JOAO", "pontuacao": 90},
                {"nome": "RODRI", "pontuacao": 80},
                {"nome": "DUDU", "pontuacao": 70},
                {"nome": "HENRI", "pontuacao": 60},
            ]
            with open(LEADERBOARD_FILE, "w") as f:
                json.dump(data_inicial, f, indent=4)

    def carregar_leaderboard(self):
        """Carrega o leaderboard do arquivo JSON."""
        self._inicializar_arquivo()
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def salvar_leaderboard(self, nome, pontuacao):
        """Salva uma nova pontuação no leaderboard."""
        leaderboard = self.carregar_leaderboard()
        leaderboard.append({"nome": nome, "pontuacao": pontuacao})
        # Ordena por pontuação, descendente, e mantém apenas os 5 melhores
        leaderboard = sorted(leaderboard, key=lambda x: x["pontuacao"], reverse=True)[:5]
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard, f, indent=4)

    def renderizar_texto(self, texto, fonte, cor, superficie, x, y, centro=False):
        """Renderiza texto na tela."""
        textobj = fonte.render(texto, True, cor)
        textrect = textobj.get_rect()
        if centro:
            textrect.center = (x, y)
        else:
            textrect.topleft = (x, y)
        superficie.blit(textobj, textrect)

    def exibir_leaderboard(self, fonte, cor, superficie, x, y):
        """Exibe o leaderboard na tela."""
        leaderboard = self.carregar_leaderboard()
        for idx, entry in enumerate(leaderboard):
            nome = entry["nome"]
            pontuacao = entry["pontuacao"]
            texto = f"{nome}: -------------------------- {pontuacao} pts"
            self.renderizar_texto(texto, fonte, cor, superficie, x, y + idx * 30)
