import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Combina todas as tabelas em uma só. Mudei o nome da tabela fornecida de 2019 manualmente, pois ela não seguia o formato das outras.
casamentos_homens_ano = []
casamentos_mulheres_ano = []
for ano in range(2015, 2022):
    tabela_homens = pd.read_csv(f"dados_Tabela 4.1.3.xls_{ano}.csv")
    tabela_mulheres = pd.read_csv(f"dados_Tabela 4.1.4.xls_{ano}.csv")
    casamentos_homens_ano.append(tabela_homens)
    casamentos_mulheres_ano.append(tabela_mulheres)
todos_casamentos_ano = casamentos_homens_ano + casamentos_mulheres_ano
tabela_completa = pd.concat(todos_casamentos_ano, ignore_index=True)

# Mapeamento dos meses para valor númerico
mapa_meses = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12,
}
tabela_completa["mes"] = tabela_completa["mes"].map(mapa_meses)

# Agrupamentos para futuras analises e criação de tabelas
casamentos_por_ano = tabela_completa.groupby("ano")["numero"].sum()
casamentos_por_estado = tabela_completa.groupby("uf")["numero"].sum()
casamentos_por_genero = tabela_completa.groupby("genero")["numero"].sum()
casamentos_por_mes = tabela_completa.groupby("mes")["numero"].sum()

print("Número de Casamentos por Ano:")
print(casamentos_por_ano)

print("Número de Casamentos por Estado:")
print(casamentos_por_estado)

print("Número de Casamentos por Gênero:")
print(casamentos_por_genero)

print("Número de Casamentos por Mês:")
print(casamentos_por_mes)

# Exporta as tabelas para arquivos CSV
casamentos_por_ano.to_csv("casamentos_por_ano.csv")
casamentos_por_estado.to_csv("casamentos_por_estado.csv")
casamentos_por_genero.to_csv("casamentos_por_genero.csv")
casamentos_por_mes.to_csv("casamentos_por_mes.csv")


# Plota em um gráfico em forma de linha o número de casamentos homoafetivos para homens e mulheres em linhas separadas.
def grafico_casamento_por_ano(tabela_completa):
    dados_ano_genero = (
        tabela_completa.groupby(["ano", "genero"])["numero"].sum().unstack()
    )
    plt.figure(figsize=(10, 6))
    plt.plot(
        dados_ano_genero.index,
        dados_ano_genero["Masculino"],
        label="Casamentos Masculinos",
        color="blue",
    )
    plt.plot(
        dados_ano_genero.index,
        dados_ano_genero["Feminino"],
        label="Casamentos Femininos",
        color="deeppink",
    )
    plt.xlabel("Ano")
    plt.ylabel("Número de Casamentos")
    plt.grid(True)
    plt.title("Número de Casamentos por Ano")
    plt.legend()
    plt.show()


grafico_casamento_por_ano(tabela_completa)


# Faz um heatmap do número de casamentos para cada mes cruzado com cada ano
def grafico_casamentos_mes_ano(tabela_completa):
    dados_grafico_heatmap = tabela_completa.pivot_table(
        values="numero", index="mes", columns="ano", aggfunc="sum"
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(dados_grafico_heatmap, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Número de Casamentos por Mês e Ano")
    plt.xlabel("Ano")
    plt.ylabel("Mês")
    plt.show()


grafico_casamentos_mes_ano(tabela_completa)

# DataFrame para calcular casamentos per capita para cada estado (fonte: IBGE 2022)
dados_populacao = pd.DataFrame(
    {
        "uf": [
            "São Paulo",
            "Minas Gerais",
            "Rio de Janeiro",
            "Bahia",
            "Paraná",
            "Rio Grande do Sul",
            "Pernambuco",
            "Ceará",
            "Pará",
            "Santa Catarina",
            "Goiás",
            "Maranhão",
            "Paraíba",
            "Amazonas",
            "Espírito Santo",
            "Mato Grosso",
            "Rio Grande do Norte",
            "Piauí",
            "Alagoas",
            "Distrito Federal",
            "Mato Grosso do Sul",
            "Sergipe",
            "Rondônia",
            "Tocantins",
            "Acre",
            "Amapá",
            "Roraima",
        ],
        "populacao": [
            44411238,
            20538718,
            16054524,
            14141626,
            11444380,
            10882965,
            9058931,
            8794957,
            8121025,
            7610361,
            7056495,
            6775805,
            3974687,
            3941613,
            3833712,
            3658649,
            3302729,
            3271199,
            3127683,
            2817381,
            2757013,
            2209558,
            1581196,
            1511460,
            830018,
            733759,
            636707,
        ],
    }
)


# Faz um gráfico de bararas que demonstra o número de casamentos a cada 10000 habitantes em cada estado do país, utilizando o DataFrame acima
def grafico_casamentos_por_estado_per_capita(tabela_completa):
    casamentos_estado = casamentos_por_estado.reset_index()
    dados_estado = pd.merge(casamentos_estado, dados_populacao, on="uf", how="left")
    dados_estado["casamentos_per_capita"] = (
        dados_estado["numero"] * 10000 / dados_estado["populacao"]
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dados_estado, x="uf", y="casamentos_per_capita")
    plt.title("Casamentos Homoafetivos per Capita por Estado")
    plt.xlabel("Estado")
    plt.ylabel("Casamentos por 10000 pessoas")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


grafico_casamentos_por_estado_per_capita(tabela_completa)

# Relaciona cada estada a sua região
mapa_estado_para_regiao = {
    "São Paulo": "Sudeste",
    "Rio de Janeiro": "Sudeste",
    "Minas Gerais": "Sudeste",
    "Espírito Santo": "Sudeste",
    "Rio Grande do Sul": "Sul",
    "Santa Catarina": "Sul",
    "Paraná": "Sul",
    "Bahia": "Nordeste",
    "Sergipe": "Nordeste",
    "Alagoas": "Nordeste",
    "Pernambuco": "Nordeste",
    "Paraíba": "Nordeste",
    "Rio Grande do Norte": "Nordeste",
    "Ceará": "Nordeste",
    "Piauí": "Nordeste",
    "Maranhão": "Nordeste",
    "Pará": "Norte",
    "Amazonas": "Norte",
    "Acre": "Norte",
    "Rondônia": "Norte",
    "Roraima": "Norte",
    "Amapá": "Norte",
    "Tocantins": "Norte",
    "Mato Grosso": "Centro-Oeste",
    "Mato Grosso do Sul": "Centro-Oeste",
    "Goiás": "Centro-Oeste",
    "Distrito Federal": "Centro-Oeste",
}


# Faz um gráfico de bararas que demonstra o número de casamentos a cada 10000 habitantes para cada região do país
def casamentos_per_capita_por_regiao(tabela_completa):
    casamentos_estado = tabela_completa.groupby("uf")["numero"].sum().reset_index()
    dados_estado = pd.merge(casamentos_estado, dados_populacao, on="uf", how="left")
    dados_estado["regiao"] = dados_estado["uf"].map(mapa_estado_para_regiao)
    dados_regiao = dados_estado.groupby("regiao").sum().reset_index()
    dados_regiao["casamentos_per_capita"] = (
        dados_regiao["numero"] * 10000 / dados_regiao["populacao"]
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dados_regiao, x="regiao", y="casamentos_per_capita")
    plt.title("Casamentos Homoafetivos per Capita por Região")
    plt.xlabel("Região")
    plt.ylabel("Casamentos por 10000 pessoas")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


casamentos_per_capita_por_regiao(tabela_completa)


# Mede a correlação entre a população de um estado e o número de casamentos homoafetivos.
def correlacao_casamentos_populacao(dados_populacao):
    casamentos_estado = casamentos_por_estado.reset_index()
    dados_estado = pd.merge(casamentos_estado, dados_populacao, on="uf", how="left")
    correlacao = dados_estado["numero"].corr(
        dados_estado["populacao"], method="pearson"
    )
    print(f"\nCoeficiente de Pearson: {correlacao}")
    plt.figure(figsize=(10, 6))
    plt.scatter(
        dados_estado["populacao"],
        dados_estado["numero"],
        label="Dados por Estado",
        color="blue",
    )
    plt.plot(
        np.unique(dados_estado["populacao"]),
        np.poly1d(np.polyfit(dados_estado["populacao"], dados_estado["numero"], 1))(
            np.unique(dados_estado["populacao"])
        ),
        color="red",
        label="Linha de Regressão",
    )
    plt.xlabel("População")
    plt.ylabel("Número de Casamentos")
    plt.title(
        "Correlação (Pearson) entre População e Número de Casamentos Homoafetivos"
    )
    plt.legend()
    plt.grid(True)
    plt.show()


correlacao_casamentos_populacao(dados_populacao)


# Faz a previsão de número de casamentos para um determinado estado, para os próximos 2 anos, 2024 e 2025.
def previsao_casamentos(dados_estado, nome_estado):
    X = dados_estado[["ano"]]
    y = dados_estado["numero"]
    modelo = LinearRegression()
    modelo.fit(X, y)
    anos_futuros = pd.DataFrame({"ano": [2024, 2025]})
    previsoes = modelo.predict(anos_futuros)
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color="blue", label="Dados Reais")
    plt.plot(X, modelo.predict(X), color="black", label="Modelo")
    plt.scatter(anos_futuros, previsoes, color="red", label="Previsões")
    plt.xlabel("Ano")
    plt.ylabel("Número de Casamentos")
    plt.title(f"Previsão de Casamentos Homoafetivos em {nome_estado}")
    plt.legend()
    plt.grid(True)
    plt.show()
    return previsoes


# Seleciona os dados dos 3 estados com o maior número de casamentos homoafetivos
estados_top3 = ["Rio de Janeiro", "Minas Gerais", "São Paulo"]
dados_filtrados_top3 = tabela_completa[tabela_completa["uf"].isin(estados_top3)]
dados_agrupados = (
    dados_filtrados_top3.groupby(["ano", "uf"])["numero"].sum().reset_index()
)

# Roda a função de previsao_casamentos para os estados com maior número de casamentos homoafetivos, armazena os resultados e os printa.
resultados_previsoes = {}
for estado in estados_top3:
    dados_estado = dados_agrupados[dados_agrupados["uf"] == estado]
    resultados_previsoes[estado] = previsao_casamentos(dados_estado, estado)
for estado in estados_top3:
    print(f"Previsões - {estado}:")
    print(f"2024: {resultados_previsoes[estado][0]}")
    print(f"2025: {resultados_previsoes[estado][1]}")
