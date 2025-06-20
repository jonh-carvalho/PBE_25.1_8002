# Dashboard Streamlit para Visualização de Dados do Censo Demográfico
# Este script cria um dashboard interativo usando Streamlit para visualizar os dados coletados pelo c
# censo, com base no questionário do Censo 2022 do IBGE.
## Requisitos:
# - Streamlit   
# - Requests
# - Pandas
# - Matplotlib
# - Seaborn
# - Faker (para gerar dados fictícios, se necessário)
# - Django (para rodar a API que fornece os dados)
# - Django REST Framework (para a API)
# - Certifique-se de que sua API Django esteja rodando e acessível na URL configurada abaixo.

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configurações da Página e API ---
st.set_page_config(layout="wide", page_title="Dashboard Censo Demográfico")

API_BASE_URL_BASICO = "http://localhost:8000/api/"  # Ajuste se sua API rodar em outra URL/porta
# API_BASE_URL_CENSO = "http://localhost:8000/api/" # Adicione a URL base do seu app 'censo'

# --- Funções Auxiliares ---
@st.cache_data(ttl=600) # Cache para evitar requisições repetidas rapidamente
def fetch_data(endpoint_url):
    """Busca dados de um endpoint da API."""
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar à API ({endpoint_url}): {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        st.error(f"Erro ao decodificar JSON da API ({endpoint_url}). Resposta não é um JSON válido.")
        return None

def plot_countplot(df, column, title, xlabel, ylabel="Contagem", hue=None):
    """Cria um gráfico de contagem e o exibe no Streamlit."""
    if column not in df.columns or df[column].empty:
        st.warning(f"Coluna '{column}' não encontrada ou vazia para o gráfico '{title}'.")
        return

    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y=column, order=df[column].value_counts().index, hue=hue, palette="viridis")
    plt.title(title, fontsize=15)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf() # Limpa a figura para o próximo gráfico

def plot_histplot(df, column, title, xlabel, ylabel="Frequência", bins=10):
    """Cria um histograma e o exibe no Streamlit."""
    if column not in df.columns or df[column].empty:
        st.warning(f"Coluna '{column}' não encontrada ou vazia para o gráfico '{title}'.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(df[column].dropna(), bins=bins, kde=True)
    plt.title(title, fontsize=15)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()

# --- Título Principal do Dashboard ---
st.title("📊 Dashboard Censo Demográfico")
st.markdown("Visualização dos dados coletados pelo censo, com base no questionário do Censo 2022 do IBGE.")

# --- Abas para Organização ---
tab_basico, tab_censo_geral, tab_observacoes = st.tabs(["Informações Básicas (App Básico)", "Análises do Censo (App Censo)", "Observações"])

with tab_basico:
    st.header("Análises do App `basico`")

    # --- Domicílios ---
    st.subheader("🏠 Domicílios")
    domicilios_data = fetch_data(f"{API_BASE_URL_BASICO}domicilios/")
    if domicilios_data:
        df_domicilios = pd.DataFrame(domicilios_data)
        if not df_domicilios.empty:
            st.markdown(f"**Total de Domicílios Registrados:** {len(df_domicilios)}")

            col1, col2 = st.columns(2)
            with col1:
                plot_countplot(df_domicilios, 'especie', 'Distribuição por Espécie de Domicílio', 'Contagem', 'Espécie')
            with col2:
                plot_countplot(df_domicilios, 'tipo', 'Distribuição por Tipo de Construção', 'Contagem', 'Tipo')

            # Adicione mais gráficos para abastecimento_agua, banheiros, destino_esgoto, coleta_lixo
            # Exemplo:
            # plot_countplot(df_domicilios, 'abastecimento_agua', 'Abastecimento de Água', 'Contagem', 'Forma de Abastecimento')
            # st.dataframe(df_domicilios.head()) # Para visualização tabular
        else:
            st.info("Não há dados de domicílios para exibir.")
    else:
        st.warning("Não foi possível carregar os dados de domicílios.")

    # --- Moradores ---
    st.subheader("👥 Moradores")
    moradores_data = fetch_data(f"{API_BASE_URL_BASICO}moradores/")
    if moradores_data:
        df_moradores = pd.DataFrame(moradores_data)
        if not df_moradores.empty:
            st.markdown(f"**Total de Moradores Registrados:** {len(df_moradores)}")

            col1, col2 = st.columns(2)
            with col1:
                plot_countplot(df_moradores, 'sexo', 'Distribuição por Sexo', 'Contagem', 'Sexo')
            with col2:
                plot_countplot(df_moradores, 'raca_cor', 'Distribuição por Raça/Cor', 'Contagem', 'Raça/Cor')

            plot_histplot(df_moradores, 'idade', 'Distribuição de Idade dos Moradores', 'Idade', 'Frequência', bins=20)
            # Adicione mais gráficos para alfabetizado, etc.
            # st.dataframe(df_moradores.head())
        else:
            st.info("Não há dados de moradores para exibir.")
    else:
        st.warning("Não foi possível carregar os dados de moradores.")

    # --- Responsáveis ---
    st.subheader("👤 Responsáveis pelo Domicílio")
    responsaveis_data = fetch_data(f"{API_BASE_URL_BASICO}responsaveis/")
    if responsaveis_data:
        df_responsaveis = pd.DataFrame(responsaveis_data)
        if not df_responsaveis.empty:
            st.markdown(f"**Total de Responsáveis Registrados:** {len(df_responsaveis)}")
            # Converter renda_mensal para numérico, tratando erros
            df_responsaveis['renda_mensal'] = pd.to_numeric(df_responsaveis['renda_mensal'], errors='coerce')

            plot_histplot(df_responsaveis, 'renda_mensal', 'Distribuição de Renda Mensal dos Responsáveis', 'Renda Mensal (R$)', 'Frequência', bins=15)
            plot_countplot(df_responsaveis, 'faixa_rendimento', 'Distribuição por Faixa de Rendimento', 'Contagem', 'Faixa de Rendimento')
            # st.dataframe(df_responsaveis.head())
        else:
            st.info("Não há dados de responsáveis para exibir.")
    else:
        st.warning("Não foi possível carregar os dados de responsáveis.")

    # --- Falecidos ---
    st.subheader("🖤 Falecidos no Domicílio")
    falecidos_data = fetch_data(f"{API_BASE_URL_BASICO}falecidos/")
    if falecidos_data:
        df_falecidos = pd.DataFrame(falecidos_data)
        if not df_falecidos.empty:
            st.markdown(f"**Total de Falecidos Registrados:** {len(df_falecidos)}")
            plot_histplot(df_falecidos, 'idade_falecimento', 'Distribuição de Idade ao Falecer', 'Idade ao Falecer', 'Frequência', bins=15)
            # st.dataframe(df_falecidos.head())
        else:
            st.info("Não há dados de falecidos para exibir.")
    else:
        st.warning("Não foi possível carregar os dados de falecidos.")


with tab_censo_geral:
    st.header("Análises Gerais do Censo (App `censo`)")
    st.markdown("Esta seção será dedicada a visualizações mais complexas e agregadas provenientes do seu app `censo`.")
    st.info("Lembre-se de que, para análises demográficas ricas (pirâmides etárias, mapas de densidade, etc.), "
            "é ideal que sua API Django no app `censo` já forneça endpoints com dados pré-agregados.")

    # Exemplo de como você poderia consumir um endpoint agregado do app 'censo'
    # populacao_por_idade_sexo_data = fetch_data(f"{API_BASE_URL_CENSO}populacao/por-idade-sexo/")
    # if populacao_por_idade_sexo_data:
    #     # Supondo que a API retorne algo como:
    #     # {
    #     #   "labels": ["0-10 M", "0-10 F", "11-20 M", "11-20 F", ...],
    #     #   "values": [150, 140, 220, 210, ...]
    #     # }
    #     # Ou um formato adequado para um DataFrame que você possa usar para plotar uma pirâmide etária
    #     df_pop_idade_sexo = pd.DataFrame(populacao_por_idade_sexo_data) # Ajuste conforme a estrutura do seu JSON
    #     st.subheader("Pirâmide Etária (Exemplo)")
    #     if not df_pop_idade_sexo.empty:
    #         # Aqui você implementaria a lógica para plotar a pirâmide etária
    #         # Ex: usando matplotlib ou plotly
    #         st.bar_chart(df_pop_idade_sexo.set_index('labels')) # Exemplo simples, pirâmide requer mais manipulação
    #         st.write("Implementação da pirâmide etária aqui.")
    #     else:
    #         st.info("Não há dados para a pirâmide etária.")
    # else:
    #     st.warning("Não foi possível carregar dados de população por idade e sexo do app 'censo'.")

    st.markdown("Outras análises possíveis para o app `censo`:")
    st.markdown("""
    - Distribuição da população por nível de escolaridade e sexo.
    - Mapas de densidade populacional por UF/Município (se os dados tiverem geolocalização).
    - Análise de migração (se houver dados sobre local de nascimento e residência anterior).
    - Características dos domicílios por área urbana/rural.
    """)

with tab_observacoes:
    st.header("Observações e Próximos Passos")
    st.markdown("""
    - **Completar `TipoConstrucao`**: O enum `TipoConstrucao` no arquivo `basico/models.py` (campo `tipo` do modelo `Domicilio`) precisa ser preenchido com todas as opções do questionário do IBGE (item 1.12) para que a análise de tipo de domicílio seja completa e precisa. Atualmente, ele está assim:
      ```python
      class TipoConstrucao(models.TextChoices):
          CASA = '011', 'Casa'
          APARTAMENTO = '013', 'Apartamento'
          # ... (adicionar todos os outros tipos do questionário 1.12)
      ```
    - **Endpoints Agregados na API (App `censo`)**: Para melhor performance e dashboards mais ricos (como pirâmides etárias, mapas, etc.), é **altamente recomendável** que sua API Django, especialmente no app `censo`, forneça endpoints com dados já agregados. Processar grandes volumes de dados brutos no Streamlit pode ser lento.
        - Exemplo: Um endpoint `/api/censo/populacao/distribuicao-idade-sexo/` que retorne contagens por faixas etárias e sexo, em vez de todos os registros de moradores.
    - **Filtros Interativos**: Adicione filtros na sidebar do Streamlit (`st.sidebar`) para permitir que o usuário explore os dados de forma mais dinâmica (ex: filtrar por UF, município, faixa etária, sexo).
    - **Detalhes e Cruzamentos**: Explore cruzamentos de dados mais complexos (ex: renda por nível de escolaridade, tipo de domicílio por faixa de renda do responsável).
    - **Estilização e Cores**: Utilize paletas de cores consistentes e melhore a apresentação visual dos gráficos. Bibliotecas como Plotly Express ou Altair podem oferecer mais interatividade nativa.
    - **Tratamento de Erros e Feedback**: Aprimore o tratamento de erros e forneça feedback claro ao usuário caso os dados não possam ser carregados ou se não houver dados para exibir.
    - **Segurança da API**: Se sua API Django requer autenticação, você precisará implementar a lógica para enviar tokens de autenticação nas requisições `requests`.
    """)

# Para rodar o dashboard:
# 1. Salve este código como dashboard_streamlit.py
# 2. Abra o terminal na pasta onde salvou o arquivo
# 3. Execute: streamlit run dashboard_streamlit.py
