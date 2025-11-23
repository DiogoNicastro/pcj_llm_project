Projeto PCJ - Análise Ambiental com LLM
Objetivo

Automatizar a extração de dados dos boletins PCJ e gerar análises comparando valores atuais e médias históricas de chuva e vazão com auxílio de um modelo de linguagem (LLM).

Estrutura do Projeto

extracao_media_historica.ipynb – extração e leitura dos boletins PDF.

normalizacao_e_merge.ipynb – limpeza e consolidação dos dados.

app_llm_pcj.py – aplicação Streamlit para visualização e geração de insights.

resultados/df_completo_normalizado.csv – dataset final processado.

Execução

Instale as dependências e execute a aplicação:

pip install -r requirements.txt
streamlit run app_llm_pcj.py

Dataset

Contém os campos:

mes_ano | rio | chuva | chuva_hist | vazao | vazao_hist | oxigenio

LLM

Modelo GPT-5 (OpenAI), usado para gerar análises automáticas sobre o comportamento hidrológico mensal com base nos dados históricos e observados.

Ética e Viabilidade

Dados públicos, sem informações pessoais.
Uso pontual de LLM, com custo reduzido e finalidade interpretativa.

Equipe

Caua Ricci
Diogo Nicastro
Henry Demetrio
Rodrigo Andrino