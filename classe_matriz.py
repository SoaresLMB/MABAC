import numpy as np
import pandas as pd

class Matriz:

    def __init__(self,qtd_alternativas,qtd_criterios):
        self.qtd_alternativas = qtd_alternativas
        self.qtd_criterios = qtd_criterios
        self.lista_alternativas = []
        self.criterios_max = []
        self.criterios_min = []
        self.lista_criterios = []
        self.lista_pesos = []

    def metodo_mabac(self):

        self.inserindo_alternativas()
        self.inserindo_criterios()
        self.inserindo_pesos()
        matriz_inicial = self.matriz_decisao()
        matriz_normalizada = self.normalizacao_da_matriz(matriz_inicial)
        matriz_ponderada = self.ponderacao_matriz(matriz_normalizada)
        area_aproximada = self.area_aproximada_da_fronteira(matriz_ponderada)
        matriz_de_distancias = self.distancia_alternativa_para_area_aproximada_da_fronteira(matriz_ponderada,area_aproximada)
        valor_absoluto_alternativas = self.valor_absoluto_das_alternativas(matriz_de_distancias)
        self.classificacao_das_alternativas(valor_absoluto_alternativas)
        self.visualizacao_dos_resultados(matriz_inicial,matriz_normalizada,matriz_ponderada,area_aproximada,matriz_de_distancias)

    def metodo_critic(self):
        pass

    def inserindo_alternativas(self):
        n = 0

        while n < self.qtd_alternativas:

            alternativa = input("digite o nome da alternativa")
            self.lista_alternativas.append(alternativa)

            n += 1

    def inserindo_criterios(self):
        n = 0

        while n < self.qtd_criterios:
            criterio = input("digite o nome do critério")
            tipo_de_criterio = input("Tipo do critério: (MAX) para maximização ou (MIN) para minimização").upper()

            if tipo_de_criterio == "MAX":
                self.criterios_max.append(criterio)
            else:
                self.criterios_min.append(criterio)

            n += 1

        for cmax in self.criterios_max:
            self.lista_criterios.append(cmax)

        for cmin in self.criterios_min:
            self.lista_criterios.append(cmin)

    def inserindo_pesos(self):

        for criterio in range(self.qtd_criterios):
            peso = float(input(f"Digite o peso para o critério {self.lista_criterios[criterio]}"))
            self.lista_pesos.append(peso)

    def matriz_decisao(self):
        matriz_decisao_inicial = np.zeros((self.qtd_alternativas, self.qtd_criterios))

        for a in range(self.qtd_alternativas):
            for c in range(self.qtd_criterios):
                matriz_decisao_inicial[a][c] = float(input(f"Digite o valor do critério {self.lista_criterios[c]} da alternativa {self.lista_alternativas[a]}:"))

        return matriz_decisao_inicial

    def normalizacao_da_matriz(self,matriz_decisao_inicial):

        matriz_normalizada = np.zeros((self.qtd_alternativas, self.qtd_criterios))

        ri_menos = matriz_decisao_inicial.min(axis=0)
        ri_mais = matriz_decisao_inicial.max(axis=0)
        range_1 = len(self.criterios_max)
        range_2 = (len(self.lista_criterios) - range_1)

        for a in range(self.qtd_alternativas):
            for c in range(range_1):
                matriz_normalizada[a][c] = (matriz_decisao_inicial[a][c] - ri_menos[c]) / (ri_mais[c] - ri_menos[c])
            for c in range(range_2):
                matriz_normalizada[a][c + range_1] = ((matriz_decisao_inicial[a][c + range_1] - ri_mais[c + range_1]) / (ri_menos[c + range_1] - ri_mais[c + range_1]))

        return matriz_normalizada

    def ponderacao_matriz(self,matriz_normalizada):

        matriz_ponderada = np.zeros((self.qtd_alternativas, self.qtd_criterios))

        for a in range(self.qtd_alternativas):
            for c in range(self.qtd_criterios):
                matriz_ponderada[a][c] = self.lista_pesos[c] + (self.lista_pesos[c] * matriz_normalizada[a][c])

        return matriz_ponderada

    def area_aproximada_da_fronteira(self,matriz_ponderada):
        area_aproximada_fronteira = []

        produto_colunas_matriz_ponderada = np.prod(matriz_ponderada, axis=0)

        for c in range(self.qtd_criterios):
            valor = (produto_colunas_matriz_ponderada[c]) ** (1 / self.qtd_alternativas)
            area_aproximada_fronteira.append(valor)

        return area_aproximada_fronteira

    def distancia_alternativa_para_area_aproximada_da_fronteira(self,matriz_ponderada,area_aproximada_fronteira):
        matriz_de_distancias = np.subtract(matriz_ponderada, area_aproximada_fronteira)

        return matriz_de_distancias

    def valor_absoluto_das_alternativas(self,matriz_de_distancias):
        valor_absoluto_alternativas = np.sum(matriz_de_distancias, axis=1)

        return valor_absoluto_alternativas

    def classificacao_das_alternativas(self,valor_absoluto_alternativas):

        nome_linhas = np.array(self.lista_alternativas)

        df_valor_absoluto = pd.DataFrame(valor_absoluto_alternativas)
        df_valor_absoluto.index = nome_linhas
        df_valor_absoluto.columns = ["Valor absoluto"]

        clasificacao_alternativas = df_valor_absoluto.sort_values(by=["Valor absoluto"], ascending=False)

        return clasificacao_alternativas

    def visualizacao_dos_resultados(self,matriz_decisao_inicial,matriz_normalizada,matriz_ponderada,area_aproximada_fronteira,matriz_de_distancias):

        nome_colunas = np.array(self.lista_criterios)
        nome_linhas = np.array(self.lista_alternativas)

        matriz_de_decisao = pd.DataFrame(matriz_decisao_inicial)
        matriz_de_decisao.columns = nome_colunas
        matriz_de_decisao.index = nome_linhas
        print(matriz_de_decisao)
        print("\n")

        matriz_normalizada = pd.DataFrame(matriz_normalizada)
        matriz_normalizada.index = nome_linhas
        print(matriz_normalizada)
        print("\n")

        matriz_ponderada = pd.DataFrame(matriz_ponderada)
        matriz_ponderada.index = nome_linhas
        print(matriz_ponderada)
        print("\n")

        area_fronteira = np.array(area_aproximada_fronteira)
        print(area_fronteira)
        print("\n")

        matriz_de_distancias = pd.DataFrame(matriz_de_distancias)
        matriz_de_distancias.index = nome_linhas
        print(matriz_de_distancias)
        print("\n")





