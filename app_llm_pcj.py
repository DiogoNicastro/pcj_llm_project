# ============================================
# 💧 ANÁLISE AMBIENTAL PCJ COM LLM
# ============================================
import os
import streamlit as st
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "resultados", "df_completo_normalizado.csv")

df = pd.read_csv(DATA_PATH, sep=';')

st.set_page_config(page_title="Análise PCJ com LLM", layout="centered")
st.title("💧 Análise Ambiental das Bacias PCJ com LLM")
st.caption("Selecione um rio e um mês para gerar automaticamente um insight interpretativo com base nos dados monitorados.")

rios = sorted(df['rio'].unique())
meses = sorted(df['mes_ano'].unique())

rio = st.selectbox("🌊 Selecione o Rio", rios)
mes = st.selectbox("🗓️ Selecione o Mês", meses)

dados = df[(df['rio'] == rio) & (df['mes_ano'] == mes)]

if not dados.empty:
    st.subheader("📊 Dados Observados")
    st.dataframe(
        dados[['mes_ano', 'rio', 'chuva', 'chuva_hist', 'vazao', 'vazao_hist', 'oxigenio']],
        hide_index=True
    )
else:
    st.warning("⚠️ Nenhum dado encontrado para essa combinação.")

st.divider()
st.subheader("🤖 Geração Automática de Insight")

api_key = st.text_input("🔑 Cole sua chave da OpenAI API:", type="password")

if st.button("Gerar Insight com LLM"):
    if not api_key:
        st.error("❌ Por favor, insira sua chave da OpenAI API.")
    elif dados.empty:
        st.warning("⚠️ Nenhum dado disponível para gerar insight.")
    else:
        client = OpenAI(api_key=api_key)
        row = dados.iloc[0]

        prompt = f"""
        Gere uma análise técnica e breve sobre as condições do {row['rio']} no mês {row['mes_ano']}.

        Dados observados:
        - Precipitação atual: {row['chuva']:.2f} mm
        - Média histórica: {row['chuva_hist']:.2f} mm
        - Vazão atual: {row['vazao']:.2f} m³/s
        - Média histórica: {row['vazao_hist']:.2f} m³/s
        - Oxigênio dissolvido: {row['oxigenio']:.2f}%

        Compare os valores atuais com as médias históricas e descreva:
        1. Se o período teve chuva acima, abaixo ou próxima da média.
        2. Se a vazão indica aumento ou redução.
        3. O impacto provável no oxigênio e na qualidade da água.
        4. Uma conclusão geral sobre as condições ambientais.
        """

        with st.spinner("Gerando insight..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # usa modelo mais leve e barato
                messages=[
                    {"role": "system", "content": "Você é um especialista em recursos hídricos e análise ambiental."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )

        insight = response.choices[0].message.content
        st.success("✅ Insight gerado com sucesso!")
        st.markdown(insight)

if not dados.empty:
    chuva = [dados['chuva'].values[0], dados['chuva_hist'].values[0]]
    vazao = [dados['vazao'].values[0], dados['vazao_hist'].values[0]]

    fig, ax = plt.subplots(1, 2, figsize=(8, 3))
    ax[0].bar(['Atual', 'Histórica'], chuva)
    ax[0].set_title('Precipitação (mm)')
    ax[1].bar(['Atual', 'Histórica'], vazao, color='teal')
    ax[1].set_title('Vazão (m³/s)')
    st.pyplot(fig)
