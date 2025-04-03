import streamlit as st  # Importa o Streamlit para criar aplicações web interativas
# pip install streamlit
# Para executar digite: streamlit run (Nome do projeto) - streamlit run app.py
# Acesse o Link: http://localhost:8501 no navegador
import pandas as pd  # Importa o Pandas para manipulação de dados
import plotly.express as px  # Importa o Plotly Express para criação de gráficos interativos
# pip install plotly

# Configura a página do Streamlit para ocupar toda a largura da tela
st.set_page_config(layout="wide")

# Lê os dados do arquivo CSV (separado por ponto e vírgula) e converte a coluna "Data" para o formato de data
df = pd.read_csv("vendas_supermercado.csv", sep=";", decimal=",")
df["Data"] = pd.to_datetime(df["Data"])  # Converte para formato de data
df = df.sort_values("Data")  # Ordena os dados pela data

# Cria uma nova coluna "Mês" no formato "ano-mês" (exemplo: 2025-03)
df["Mês"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Cria uma caixa de seleção (dropdown) no menu lateral para escolher o mês
mes = st.sidebar.selectbox("Selecione o Mês", df["Mês"].unique())

# Filtra os dados para exibir apenas as vendas do mês escolhido
df_filtrado = df[df["Mês"] == mes]

# Organiza os gráficos em diferentes colunas
col1, col2 = st.columns(2)  # Duas colunas
col3, col4, col5 = st.columns(3)  # Três colunas

# Gráfico 1: Faturamento por dia (barra) com cores diferentes por cidade
fig_data = px.bar(df_filtrado, x="Data", y="Total", color="Cidade", title="Faturamento por Dia")
col1.plotly_chart(fig_data, use_container_width=True)  # Exibe o gráfico na primeira coluna

# Gráfico 2: Faturamento por tipo de produto (horizontal)
fig_prod = px.bar(df_filtrado, x="Data", y="Linha de Produtos", color="Cidade", title="Faturamento por Tipo de Produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)  # Exibe o gráfico na segunda coluna

# Gráfico 3: Faturamento total por cidade (barra)
total_cidade = df_filtrado.groupby("Cidade")[["Total"]].sum().reset_index()  # Agrupa por cidade e soma o faturamento
fig_cidade = px.bar(total_cidade, x="Cidade", y="Total", title="Faturamento por Filial")
col3.plotly_chart(fig_cidade, use_container_width=True)  # Exibe o gráfico na terceira coluna

# Gráfico 4: Faturamento por tipo de pagamento (pizza)
fig_tipo_pagamento = px.pie(df_filtrado, values="Total", names="Pagamento", title="Faturamento por Tipo de Pagamento")
col4.plotly_chart(fig_tipo_pagamento, use_container_width=True)  # Exibe o gráfico na quarta coluna

# Gráfico 5: Avaliação média das filiais (barra)
total_cidade = df_filtrado.groupby("Cidade")[["Avaliacao"]].mean().reset_index()  # Agrupa por cidade e calcula a média da avaliação
fig_avaliacao = px.bar(total_cidade, y="Avaliacao", x="Cidade", title="Avaliação das Filiais")
col5.plotly_chart(fig_avaliacao, use_container_width=True)  # Exibe o gráfico na quinta coluna
