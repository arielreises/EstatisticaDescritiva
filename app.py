# Autora: Lalla Fatima Azahra Rachid e Ariel Ladislau Reises
# Trabalho de Estatística do curso de Sistemas Embarcados da Fatec Jundiaí
# Este app analisa estatísticas descritivas de dados quantitativos contínuos
# com agrupamento em classes: média, mediana, moda bruta e de Czuber,
# variância, desvio padrão e coeficiente de variação.

import streamlit as st
import numpy as np
import pandas as pd

# Função que determina o tipo da moda a partir dos dados brutos (não agrupados)
def tipo_de_moda_dados_brutos(dados):
    from collections import Counter
    contagem = Counter(dados)
    frequencias = list(contagem.values())
    maior_freq = max(frequencias)
    qtd_modas = frequencias.count(maior_freq)

    if maior_freq == 1:
        return "🔵 Amodal"          # Todos valores aparecem 1 vez
    elif qtd_modas == 1:
        return "🟢 Unimodal"
    elif qtd_modas == 2:
        return "🟠 Bimodal"
    else:
        return "🔴 Multimodal"


# Função que realiza o agrupamento de dados e calcula estatísticas agrupadas
def analisar_agrupado(dados, k=None):
    dados = sorted(dados)
    n = len(dados)
    minimo, maximo = min(dados), max(dados)
    amplitude_total = maximo - minimo

    # Se o número de classes não for informado, usa a regra de Sturges
    if not k:
        k = int(1 + 3.322 * np.log10(n))
    
    # Ajusta k para que seja sempre ímpar
    if k % 2 == 0:
        k += 1

    # Define amplitude das classes e arredonda para cima
    h = np.ceil(amplitude_total / k)

    # Cria os limites das classes
    limites = [(minimo + i * h, minimo + (i + 1) * h) for i in range(k)]

    # Calcula a frequência (fi) de cada classe
    fi = [len([x for x in dados if lim[0] <= x < lim[1]]) for lim in limites]
    fi[-1] += dados.count(maximo)  # Garante que o valor máximo entre na última classe

    # Calcula os pontos médios de cada classe (xi)
    xi = [(lim[0] + lim[1]) / 2 for lim in limites]

    # Cálculo da média agrupada
    fixi = [f * x for f, x in zip(fi, xi)]
    media = sum(fixi) / n

    # Cálculo da variância agrupada
    fi_xi2 = [f * (x - media) ** 2 for f, x in zip(fi, xi)]
    variancia = sum(fi_xi2) / (n - 1)
    desvio_padrao = np.sqrt(variancia)
    coef_var = (desvio_padrao / media) * 100

    # Cálculo da mediana agrupada
    fac = np.cumsum(fi)
    n2 = n / 2
    for i, f_ac in enumerate(fac):
        if f_ac >= n2:
            li = limites[i][0]
            fi_median = fi[i]
            fac_ant = fac[i - 1] if i > 0 else 0
            mediana = li + ((n2 - fac_ant) / fi_median) * h
            break

    # Moda bruta (ponto médio da classe com maior frequência)
    i_moda = np.argmax(fi)
    moda_bruta = xi[i_moda]

    # Moda de Czuber (mais precisa para dados agrupados)
    try:
        d1 = fi[i_moda] - fi[i_moda - 1] if i_moda > 0 else fi[i_moda]
        d2 = fi[i_moda] - fi[i_moda + 1] if i_moda < k - 1 else fi[i_moda]
        li = limites[i_moda][0]
        czuber = li + (d1 / (d1 + d2)) * h
    except:
        czuber = "Não aplicável"

    # Determina o tipo da moda a partir dos dados originais
    tipo_moda = tipo_de_moda_dados_brutos(dados)

    # Retorna os resultados em formato de dicionário
    return {
        "classes": limites,
        "frequências": fi,
        "pontos_médios": xi,
        "média": media,
        "mediana": mediana,
        "moda_bruta": moda_bruta,
        "moda_czuber": czuber,
        "variância": variancia,
        "desvio_padrão": desvio_padrao,
        "coeficiente_variação": coef_var,
        "tipo_moda": tipo_moda
    }


# --------------------------- INÍCIO DA INTERFACE COM STREAMLIT --------------------------- #

st.set_page_config(page_title="Analisador Estatístico", layout="wide")
st.title("📊 Analisador Estatístico com Classes")
st.markdown("**Autora: Lalla Fatima Azahra Rachid e Denis Queiroz Soutello**")
st.markdown("_Trabalho de Estatística do curso de Sistemas Embarcados da Fatec Jundiaí_")
st.markdown("Tema: Agrupamento em Classes (média, mediana, moda bruta e de Czuber, variância, desvio padrão e coeficiente de variação) ")

# Exemplo de como o usuário deve inserir os dados
st.text("Insira um número por linha (exemplo abaixo):")
st.code("10\n12\n15\n18\n20\n25\n25\n30\n32\n35", language="text")

# Campo de entrada dos dados numéricos
entrada = st.text_area("Cole os dados aqui:", height=200)

# Seleção do padrão de classes com filtro para ímpares
opcoes_classes = ['auto', 3, 5, 7, 9]  # todos ímpares (auto será tratado na função)
selecao = st.selectbox("Defina o padrão de número de classes:", opcoes_classes)

botao = st.button("Analisar")

if botao and entrada:
    try:
        # Converte cada linha em um número decimal (float)
        dados = [float(x.strip()) for x in entrada.splitlines() if x.strip()]

        if len(dados) < 5:
            st.warning("Insira ao menos 5 dados para uma análise significativa.")
        else:
            # Se selecionou 'auto', envia None para análise, senão passa o número
            k = None if selecao == 'auto' else selecao

            # Garante que k seja ímpar (caso a regra mude no futuro)
            if k is not None and k % 2 == 0:
                k += 1

            # Chama a função de análise
            resultados = analisar_agrupado(dados, k=k)

            # Frequências e cálculos para tabela completa
            fi = resultados["frequências"]
            n = len(dados)
            fac = np.cumsum(fi)
            fri = [f / n for f in fi]
            frac = np.cumsum(fri)

            # Exibe tabela de classes detalhada
            st.subheader("📌 Tabela de Classes Completa")
            tabela = pd.DataFrame({
                "Limite Inferior": [f"{lim[0]:.2f}" for lim in resultados["classes"]],
                "Limite Superior": [f"{lim[1]:.2f}" for lim in resultados["classes"]],
                "Frequência (fi)": fi,
                "Frequência Acumulada (Fac)": fac,
                "Ponto Médio (xi)": [f"{pm:.2f}" for pm in resultados["pontos_médios"]],
                "fi * xi": [f"{f * x:.2f}" for f, x in zip(fi, resultados["pontos_médios"])],
                "Frequência Relativa (fri)": [f"{frel*100:.2f}%" for frel in fri],
                "Frequência Relativa Acumulada (frac)": [f"{frac_i*100:.2f}%" for frac_i in frac]
            })
            st.dataframe(tabela)

            # Exibe os resultados estatísticos de forma mais detalhada
            st.subheader("📈 Resultados Estatísticos")
            st.markdown(f"""
            - **Média Agrupada**: {resultados["média"]:.2f} (valor médio ponderado pelas frequências)
            - **Mediana Agrupada**: {resultados["mediana"]:.2f} (posição central estimada)
            - **Moda Bruta**: {resultados["moda_bruta"]:.2f} (classe mais frequente)
            - **Moda de Czuber**: {resultados["moda_czuber"] if isinstance(resultados["moda_czuber"], str) else f"{resultados['moda_czuber']:.2f}"} (estimativa mais precisa da moda)
            - **Variância**: {resultados["variância"]:.2f} (dispersão dos dados)
            - **Desvio Padrão**: {resultados["desvio_padrão"]:.2f} (raiz quadrada da variância)
            - **Coeficiente de Variação**: {resultados["coeficiente_variação"]:.2f}% (medida relativa da dispersão)
            - **Tipo de Moda**: {resultados['tipo_moda']}
            """)
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")

# --------------------------- RODAPÉ --------------------------- #
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.9em;'>"
    "Feito por <strong>Lalla Rachid</strong><br>"
    "<a href='https://www.linkedin.com/in/lalla-rachid/' target='_blank'>LinkedIn</a>"
    "</div>",
    unsafe_allow_html=True
)