import tkinter as tk
from random import randint
import Pyro5.api


#python -m Pyro5.nameserver
@Pyro5.api.expose
class JogoTabuleiroRemoto:
    def __init__(self):
        # Inicialização do estado do jogo
        self.posicao_jogadores = [1, 1]
        self.pontos_jogadores = [0, 0]
        self.resultado_dado_jogador = [0, 0]
        self.jogador_atual = 0

    def jogar_dado_remoto(self, jogador):
        """
        Permite que um jogador jogue o dado remotamente.
        Atualiza a posição do jogador e os pontos com base no resultado do dado.
        Retorna uma mensagem indicando a ação do jogador.
        """
        if jogador == self.jogador_atual:
            self.resultado_dado_jogador[jogador] = randint(1, 6)
            self.posicao_jogadores[jogador] += self.resultado_dado_jogador[jogador]

            if self.posicao_jogadores[jogador] > 20:
                self.posicao_jogadores[jogador] %= 20

            self.atualizar_pontos()

            self.jogador_atual = 1 - jogador  # Alternar entre os jogadores

            cor_jogador = "Vermelho" if jogador == 0 else "Azul"
            return f"Jogador {cor_jogador} jogou o dado e obteve {self.resultado_dado_jogador[jogador]}."

    def atualizar_pontos(self):
        """
        Atualiza os pontos do jogador com base na posição atual.
        """
        casa_atual = self.posicao_jogadores[self.jogador_atual]
        if casa_atual % 2 == 0:
            self.pontos_jogadores[self.jogador_atual] += 2
        else:
            self.pontos_jogadores[self.jogador_atual] = max(0, self.pontos_jogadores[self.jogador_atual] - 1)

    def obter_estado_jogo(self):
        """
        Retorna um dicionário com o estado atual do jogo.
        """
        return {
            "posicao_jogadores": self.posicao_jogadores,
            "pontos_jogadores": self.pontos_jogadores,
            "jogador_atual": self.jogador_atual
        }

    def verificar_vencedor(self):
        """
        Verifica se algum jogador atingiu 10 pontos ou mais.
        Retorna uma mensagem indicando o vencedor, se houver.
        """
        if max(self.pontos_jogadores) >= 10:
            vencedor = 1 if self.pontos_jogadores[0] > self.pontos_jogadores[1] else 2
            cor_vencedor = "Vermelho" if vencedor == 1 else "Azul"
            return f"Jogo finalizado! {cor_vencedor} venceu com {max(self.pontos_jogadores)} pontos."

if __name__ == "__main__":
    jogo_remoto = JogoTabuleiroRemoto()

    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()

    uri = daemon.register(jogo_remoto)
    ns.register("jogo.tabuleiro", uri)

    print(f"URI do objeto remoto: {uri}")

    daemon.requestLoop()
