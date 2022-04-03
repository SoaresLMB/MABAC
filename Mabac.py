import numpy as np
import pandas as pd

# 1 - Inserindo as alternativas,critérios e pesos.

# 1.1 - Declarando as váriaveis.

parar = False
parar_2 = False

lista_alternativas = []
criterios_max = []
criterios_min = []
lista_criterios = []
lista_pesos = []

# 1.2 - Inserindo as alternativas.

while not parar:

    alternativa = input("digite o nome da alternativa")
    lista_alternativas.append(alternativa)

    escolha = int(input("Digite (1) para nova alternativa e (2) para encerrar"))

    if escolha == 1:
        parar = False
    else:
        parar = True

# 1.3 -  Inserindo os critérios.

while not parar_2:

    criterio = input("digite o nome do critério")
    tipo_de_criterio = input("Tipo do critério: (MAX) para maximização ou (MIN) para minimização").upper()

    if tipo_de_criterio == "MAX":
        criterios_max.append(criterio)
    else:
        criterios_min.append(criterio)

    escolha = int(input("Digite (1) para novo critério e (2) para encerrar"))

    if escolha == 1:
        parar_2 = False
    else:
        parar_2 = True

for cmax in criterios_max:
    lista_criterios.append(cmax)

for cmin in criterios_min:
    lista_criterios.append(cmin)

# 1.4 - Inserindo os Pesos.

qtd_de_criterios = len(lista_criterios)
qtd_de_alternativas = len(lista_alternativas)

for criterio in range(qtd_de_criterios):
    peso = float(input(f"Digite o peso para o critério {lista_criterios[criterio]}"))
    lista_pesos.append(peso)

#Inserir que o peso não pode ser maior que 1

#2 - Matriz de Decisão Inicial.

matriz_decisao_inicial = np.zeros((qtd_de_alternativas,qtd_de_criterios))

for a in range(qtd_de_alternativas):
    for c in range(qtd_de_criterios):
        matriz_decisao_inicial[a][c] = float(input(f"Digite o valor do critério {lista_criterios[c]} da alternativa {lista_alternativas[a]}:"))

# 3 - Normalização da Matriz de Decisão Inicial.

matriz_normalizada = np.zeros((qtd_de_alternativas,qtd_de_criterios))

ri_menos = matriz_decisao_inicial.min(axis=0)
ri_mais = matriz_decisao_inicial.max(axis=0)

range_1 = len(criterios_max)
range_2 = (len(lista_criterios) - range_1)

for a in range(qtd_de_alternativas):
    for c in range(range_1):
        matriz_normalizada[a][c] = (matriz_decisao_inicial[a][c] - ri_menos[c]) / (ri_mais[c] - ri_menos[c])
    for c in range(range_2):
        matriz_normalizada[a][c + range_1] = ((matriz_decisao_inicial[a][c + range_1] - ri_mais[c + range_1]) / (ri_menos[c + range_1] - ri_mais[c + range_1]))

# 4 - Ponderação da Matriz Normalizada.

matriz_ponderada = np.zeros((qtd_de_alternativas,qtd_de_criterios))

for a in range(qtd_de_alternativas):
    for c in range(qtd_de_criterios):
        matriz_ponderada [a][c] = lista_pesos[c] + (lista_pesos[c]*matriz_normalizada[a][c])

# 5 - Determinação da Área Aproximada da Fronteira).

area_aproximada_fronteira = []

produto_colunas_matriz_ponderada = np.prod(matriz_ponderada,axis=0)

for c in range(qtd_de_criterios):
    valor = (produto_colunas_matriz_ponderada[c]) ** (1/qtd_de_alternativas)
    area_aproximada_fronteira.append(valor)

# 6 - Cálculo da distância de cada alternativa até a Área Aproximada da Fronteira.

matriz_de_distancias = np.subtract(matriz_ponderada,area_aproximada_fronteira)

# 7 - Valor absoluto das alternativas:

valor_absoluto_alternativas = np.sum(matriz_de_distancias,axis=1)

# 8 - Classificação das alternativas:

nome_linhas = np.array(lista_alternativas)

df_valor_absoluto = pd.DataFrame(valor_absoluto_alternativas)
df_valor_absoluto.index = nome_linhas
df_valor_absoluto.columns = ["Valor absoluto"]

clasificacao_alternativas = df_valor_absoluto.sort_values(by=["Valor absoluto"],ascending=False)

# 9 - Visualização de resultados:

nome_colunas = np.array(lista_criterios)

matriz_de_decisao = pd.DataFrame(matriz_decisao_inicial)
matriz_de_decisao.columns = nome_colunas
matriz_de_decisao.index = nome_linhas

matriz_normalizada = pd.DataFrame(matriz_normalizada)
matriz_normalizada.index = nome_linhas

matriz_ponderada = pd.DataFrame(matriz_ponderada)
matriz_ponderada.index = nome_linhas

area_aproximada_fronteira = np.array(area_aproximada_fronteira)

matriz_de_distancias = pd.DataFrame(matriz_de_distancias)
matriz_de_distancias.index = nome_linhas

print("Matriz de Decisão Inicial")
print(matriz_de_decisao)
print("\n")
print("Matriz Normalizada")
print(matriz_normalizada)
print("\n")
print("Matriz Ponderada")
print(matriz_ponderada)
print("\n")
print("Área aproximada da Fronteira")
print(area_aproximada_fronteira)
print("\n")
print("Matriz de Distâncias")
print(matriz_de_distancias)
print("\n")
print("Classificação das alternativas (Da melhor alternativa para a pior)")
print(clasificacao_alternativas)



























