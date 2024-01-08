import tkinter as tk
import Pyro5.api

class JogoTabuleiroCliente:
    def __init__(self, uri_servidor):
        # Inicialização do cliente e configuração da interface gráfica
        self.jogo_remoto = Pyro5.api.Proxy(uri_servidor)
        self.janela = tk.Tk()
        self.janela.title("---=== Jogo de Tabuleiro +2-1 ===---")

        self.numero_casas = 20
        self.largura_casa = 30
        self.altura_casa = 30
        self.tamanho_grid = self.numero_casas * self.largura_casa

        self.canvas = tk.Canvas(self.janela, width=self.tamanho_grid, height=self.altura_casa)
        self.canvas.pack(pady=10)

        self.posicao_jogadores = [1, 1]
        self.pontos_jogadores = [0, 0]
        self.resultado_dado_jogador = [0, 0]

        self.label_info = tk.Label(self.janela, text="")
        self.label_info.pack(pady=10)

        self.botao_jogar_jogador1 = tk.Button(self.janela, text="Jogar dado para jogador Vermelho", command=lambda: self.jogar_dado(0))
        self.botao_jogar_jogador1.pack(pady=20)

        self.botao_jogar_jogador2 = tk.Button(self.janela, text="Jogar dado para jogador Azul", command=lambda: self.jogar_dado(1))
        self.botao_jogar_jogador2.pack(pady=20)

        self.desenhar_tabuleiro()

        self.atualizar_info()

    def desenhar_tabuleiro(self):
        # Desenha visualmente o tabuleiro na interface gráfica
        for i in range(self.numero_casas):
            x0 = i * self.largura_casa
            y0 = 0
            x1 = (i + 1) * self.largura_casa
            y1 = self.altura_casa

            self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightgray", outline="black")
            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(i + 1))

    def desenhar_jogadores(self):
        # Desenha visualmente os jogadores na interface gráfica
        self.canvas.delete("jogadores")
        for i, posicao in enumerate(self.posicao_jogadores):
            x = (posicao - 0.5) * self.largura_casa
            y = self.altura_casa // 2
            cor = "red" if i == 0 else "blue"  # Jogador 1 em vermelho, Jogador 2 em azul
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=cor, outline="black", tags="jogadores")

    def jogar_dado(self, jogador):
        # Permite que os jogadores joguem o dado clicando nos botões apropriados
        if not self.jogo_remoto.obter_estado_jogo()["jogador_atual"] == jogador:
            return

        resultado = self.jogo_remoto.jogar_dado_remoto(jogador)
        print(resultado) 
        estado_jogo = self.jogo_remoto.obter_estado_jogo()
        self.posicao_jogadores = estado_jogo["posicao_jogadores"]
        self.pontos_jogadores = estado_jogo["pontos_jogadores"]
        self.resultado_dado_jogador = resultado 

        self.atualizar_info()
        self.desenhar_jogadores()

    def atualizar_info(self):
        # Atualiza as informações sobre a posição, pontos e status dos jogadores na interface
        info_text = (f"{'Vermelho'.ljust(8)}:\t\t{'Azul'.ljust(8)}:\n"
                     f"Casa {self.posicao_jogadores[0]}\t\t\tCasa {self.posicao_jogadores[1]}\n"
                     f"Pontos {self.pontos_jogadores[0]}\t\t\tPontos {self.pontos_jogadores[1]}\n")
        self.label_info.config(text=info_text)

        vencedor = self.jogo_remoto.verificar_vencedor()
        if vencedor:
            self.label_info.config(text=vencedor)

            # Desabilita botões de jogar dados quando um jogador atinge 10 pontos
            self.botao_jogar_jogador1.config(state=tk.DISABLED)
            self.botao_jogar_jogador2.config(state=tk.DISABLED)

    def iniciar_interface(self):
        # Inicia a interface gráfica
        self.janela.mainloop()

if __name__ == "__main__":
    uri_servidor = "PYRONAME:jogo.tabuleiro"

    jogo_cliente = JogoTabuleiroCliente(uri_servidor)
    jogo_cliente.iniciar_interface()
