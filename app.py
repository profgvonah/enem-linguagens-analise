import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Análise ENEM Linguagens", layout="wide")
st.title("📊 Painel de Análise das Questões de Linguagens - ENEM")

try:
    df = pd.read_csv("banco_enem_linguagens.csv")
except FileNotFoundError:
    st.error("❌ Arquivo 'banco_enem_linguagens.csv' não encontrado. Coloque-o na mesma pasta do app.py.")
    st.stop()

colunas_necessarias = ["Ano", "Tipo_ENEM", "Área", "Assunto", "Competência", "Habilidade"]
for c in colunas_necessarias:
    if c not in df.columns:
        st.error(f"❌ A coluna '{c}' está faltando no CSV.")
        st.stop()

st.sidebar.header("🔍 Filtros")
anos = st.sidebar.multiselect("Ano:", sorted(df["Ano"].unique()), default=sorted(df["Ano"].unique()))
assuntos = st.sidebar.multiselect("Assunto:", sorted(df["Assunto"].unique()), default=sorted(df["Assunto"].unique()))
tipos = st.sidebar.multiselect("Tipo de ENEM:", sorted(df["Tipo_ENEM"].unique()), default=sorted(df["Tipo_ENEM"].unique()))

df_filtrado = df[df["Ano"].isin(anos) & df["Assunto"].isin(assuntos) & df["Tipo_ENEM"].isin(tipos)]

col1, col2, col3 = st.columns(3)
col1.metric("Total de Questões", len(df_filtrado))
col2.metric("Assuntos diferentes", df_filtrado["Assunto"].nunique())
col3.metric("Anos analisados", df_filtrado["Ano"].nunique())

st.markdown("---")

st.subheader("📈 Distribuições e Tendências")

graf1, graf2 = st.columns(2)

with graf1:
    fig1 = px.histogram(df_filtrado, x="Ano", title="Questões por Ano", color="Assunto")
    st.plotly_chart(fig1, use_container_width=True)

with graf2:
    fig2 = px.pie(df_filtrado, names="Assunto", title="Distribuição por Assunto", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.subheader("📋 Base de Questões Filtradas")
st.dataframe(df_filtrado, use_container_width=True)

st.download_button(
    label="⬇️ Baixar dados filtrados (CSV)",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="questoes_filtradas.csv",
    mime="text/csv",
)
