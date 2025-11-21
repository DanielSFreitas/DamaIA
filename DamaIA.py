"""
Jogo de Damas com IA baseada em Árvore de Decisão
"""

import copy
import random

class JogoDamas:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(8)] for _ in range(8)]
        self.jogador_atual = 'O'
        self.modo_jogo = None
        self.simbolo_humano = None
        self.inicializar_tabuleiro()
    
    def inicializar_tabuleiro(self):
        """Inicializa o tabuleiro com as peças nas posições iniciais"""
        # Peças do jogador O (parte superior)
        for linha in range(3):
            for col in range(8):
                if (linha + col) % 2 == 1:
                    self.tabuleiro[linha][col] = 'O'
        
        # Peças do jogador X (parte inferior)
        for linha in range(5, 8):
            for col in range(8):
                if (linha + col) % 2 == 1:
                    self.tabuleiro[linha][col] = 'X'
    
    def imprimir_tabuleiro(self):
        """Imprime o tabuleiro de forma visual"""
        print("\n   0  1  2  3  4  5  6  7")
        print("  -------------------------")
        for i, linha in enumerate(self.tabuleiro):
            print(f"{i}|", end="")
            for celula in linha:
                print(f" {celula} ", end="")
            print("|")
        print("  -------------------------\n")
    
    def configurar_jogo(self):
        """Configura as opções do jogo"""
        print("=== JOGO DE DAMAS ===\n")
        
        # Escolher símbolo
        while True:
            simbolo = input("Escolha seu símbolo (O ou X): ").upper()
            if simbolo in ['O', 'X']:
                self.simbolo_humano = simbolo
                break
            print("Símbolo inválido! Escolha O ou X.")
        
        # Escolher modo
        while True:
            modo = input("Jogar contra IA? (S/N): ").upper()
            if modo in ['S', 'N']:
                self.modo_jogo = 'IA' if modo == 'S' else 'HUMANO'
                break
            print("Opção inválida! Digite S ou N.")
        
        print(f"\nVocê escolheu: {self.simbolo_humano}")
        print(f"Modo: {'Contra IA' if self.modo_jogo == 'IA' else 'Dois Jogadores'}\n")
    
    def movimento_valido(self, origem_l, origem_c, destino_l, destino_c):
        """Verifica se um movimento é válido"""
        # Verificar limites
        if not (0 <= destino_l < 8 and 0 <= destino_c < 8):
            return False
        
        # Verificar se origem tem peça do jogador atual
        if self.tabuleiro[origem_l][origem_c] != self.jogador_atual:
            return False
        
        # Verificar se destino está vazio
        if self.tabuleiro[destino_l][destino_c] != ' ':
            return False
        
        diff_l = destino_l - origem_l
        diff_c = abs(destino_c - origem_c)
        
        # Movimento simples diagonal
        if diff_c == 1:
            if self.jogador_atual == 'O' and diff_l == 1:
                return True
            if self.jogador_atual == 'X' and diff_l == -1:
                return True
        
        # Captura (pular sobre peça adversária)
        if diff_c == 2 and abs(diff_l) == 2:
            meio_l = (origem_l + destino_l) // 2
            meio_c = (origem_c + destino_c) // 2
            peca_meio = self.tabuleiro[meio_l][meio_c]
            
            adversario = 'X' if self.jogador_atual == 'O' else 'O'
            if peca_meio == adversario:
                return True
        
        return False
    
    def executar_movimento(self, origem_l, origem_c, destino_l, destino_c):
        """Executa um movimento no tabuleiro"""
        self.tabuleiro[destino_l][destino_c] = self.tabuleiro[origem_l][origem_c]
        self.tabuleiro[origem_l][origem_c] = ' '
        
        # Se foi captura, remove a peça capturada
        diff_c = abs(destino_c - origem_c)
        if diff_c == 2:
            meio_l = (origem_l + destino_l) // 2
            meio_c = (origem_c + destino_c) // 2
            self.tabuleiro[meio_l][meio_c] = ' '
    
    def obter_movimentos_possiveis(self, jogador):
        """Retorna lista de todos os movimentos possíveis para um jogador"""
        movimentos = []
        
        for l in range(8):
            for c in range(8):
                if self.tabuleiro[l][c] == jogador:
                    # Tentar todos os possíveis destinos
                    direcoes = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    
                    for dl, dc in direcoes:
                        # Movimento simples
                        destino_l, destino_c = l + dl, c + dc
                        if self.movimento_valido(l, c, destino_l, destino_c):
                            movimentos.append((l, c, destino_l, destino_c))
                        
                        # Captura
                        destino_l, destino_c = l + 2*dl, c + 2*dc
                        if self.movimento_valido(l, c, destino_l, destino_c):
                            movimentos.append((l, c, destino_l, destino_c))
        
        return movimentos
    
    def avaliar_tabuleiro(self, jogador):
        """Avalia o tabuleiro com base em heurísticas (Árvore de Decisão simplificada)"""
        adversario = 'X' if jogador == 'O' else 'O'
        pontuacao = 0
        
        # Decisão 1: Contar peças (mais importante)
        pecas_jogador = sum(linha.count(jogador) for linha in self.tabuleiro)
        pecas_adversario = sum(linha.count(adversario) for linha in self.tabuleiro)
        pontuacao += (pecas_jogador - pecas_adversario) * 100
        
        # Decisão 2: Posição das peças (peças avançadas valem mais)
        for l in range(8):
            for c in range(8):
                if self.tabuleiro[l][c] == jogador:
                    if jogador == 'O':
                        pontuacao += l * 10  # Quanto mais perto do fim, melhor
                    else:
                        pontuacao += (7 - l) * 10
        
        # Decisão 3: Controle do centro
        for l in range(3, 5):
            for c in range(3, 5):
                if self.tabuleiro[l][c] == jogador:
                    pontuacao += 20
        
        return pontuacao
    
    def ia_movimento(self):
        """IA faz um movimento baseado em árvore de decisão"""
        print("IA está pensando...")
        
        adversario = 'X' if self.jogador_atual == 'O' else 'O'
        movimentos = self.obter_movimentos_possiveis(self.jogador_atual)
        
        if not movimentos:
            return None
        
        melhor_movimento = None
        melhor_pontuacao = float('-inf')
        
        # Árvore de Decisão: avaliar cada movimento possível
        for movimento in movimentos:
            ol, oc, dl, dc = movimento
            
            # Simular movimento
            tabuleiro_temp = copy.deepcopy(self.tabuleiro)
            peca_original = self.tabuleiro[ol][oc]
            self.executar_movimento(ol, oc, dl, dc)
            
            # Avaliar posição resultante
            pontuacao = self.avaliar_tabuleiro(self.jogador_atual)
            
            # Desfazer movimento
            self.tabuleiro = tabuleiro_temp
            
            # Decisão: É uma captura? Priorizar!
            if abs(dc - oc) == 2:
                pontuacao += 150
            
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_movimento = movimento
        
        return melhor_movimento
    
    def verificar_vitoria(self):
        """Verifica se alguém venceu"""
        pecas_o = sum(linha.count('O') for linha in self.tabuleiro)
        pecas_x = sum(linha.count('X') for linha in self.tabuleiro)
        
        if pecas_o == 0:
            return 'X'
        if pecas_x == 0:
            return 'O'
        
        # Verificar se jogador atual tem movimentos
        if not self.obter_movimentos_possiveis(self.jogador_atual):
            return 'X' if self.jogador_atual == 'O' else 'O'
        
        return None
    
    def jogar(self):
        """Loop principal do jogo"""
        self.configurar_jogo()
        
        while True:
            self.imprimir_tabuleiro()
            
            vencedor = self.verificar_vitoria()
            if vencedor:
                print(f"\n🎉 Jogador {vencedor} venceu! 🎉")
                break
            
            print(f"Vez do jogador: {self.jogador_atual}")
            
            # Determinar quem joga
            if self.modo_jogo == 'IA' and self.jogador_atual != self.simbolo_humano:
                # IA joga
                movimento = self.ia_movimento()
                if movimento:
                    ol, oc, dl, dc = movimento
                    print(f"IA moveu de ({ol},{oc}) para ({dl},{dc})")
                    self.executar_movimento(ol, oc, dl, dc)
                else:
                    print("IA não tem movimentos válidos!")
                    break
            else:
                # Humano joga
                try:
                    entrada = input("Digite sua jogada (formato: linha_origem,col_origem,linha_destino,col_destino): ")
                    ol, oc, dl, dc = map(int, entrada.split(','))
                    
                    if self.movimento_valido(ol, oc, dl, dc):
                        self.executar_movimento(ol, oc, dl, dc)
                    else:
                        print("Movimento inválido! Tente novamente.")
                        continue
                except:
                    print("Entrada inválida! Use o formato: 2,1,3,2")
                    continue
            
            # Trocar jogador
            self.jogador_atual = 'X' if self.jogador_atual == 'O' else 'O'

# Executar o jogo
if __name__ == "__main__":
    jogo = JogoDamas()
    jogo.jogar()