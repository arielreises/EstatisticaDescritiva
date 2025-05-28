# 📊 Analisador Estatístico com Classes

Este aplicativo, desenvolvido em Python com **Streamlit**, permite analisar **dados quantitativos contínuos agrupados em classes**, gerando automaticamente estatísticas descritivas como:

- Média agrupada  
- Mediana agrupada  
- Moda bruta e Moda de Czuber  
- Variância  
- Desvio padrão  
- Coeficiente de variação  
- Tipo de moda (unimodal, bimodal etc.)

## 🧠 Sobre o projeto

Este trabalho foi desenvolvido por **Lalla Fatima Azahra Rachid** e **Denis Queiroz Soutello**, como parte da disciplina de Estatística do curso de **Sistemas Embarcados da Fatec Jundiaí**.

O projeto possui interface amigável com Streamlit e recebe dados colados diretamente do usuário, permitindo análise estatística em tempo real com agrupamento em classes.

---

## ✅ Funcionalidades

- Inserção de dados numéricos manualmente (um por linha)
- Definição automática ou manual do número de classes (3, 5, 7 ou 9)
- Tabela com:
  - Limites das classes
  - Frequências absolutas e relativas
  - Frequências acumuladas
  - Pontos médios
  - Produto fi·xi
- Cálculo automático de:
  - Média, mediana e modas
  - Variância e desvio padrão
  - Coeficiente de variação
- Indicação visual do tipo de moda com emojis

---

## ▶️ Como usar

1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/analisador-estatistico-classes.git
   cd analisador-estatistico-classes
   ```

2. Instale as dependências:

    ```
    pip install -r requirements.txt
    ```

3. Execute a aplicação:

    ```
    streamlit run app.py
    ```

4. Requisitos
Python 3.8 ou superior

- Bibliotecas:

    - streamlit
    - numpy
    - pandas

- Você pode instalar com:

    ```
    pip install streamlit numpy pandas
    ```

- Exemplo de entrada

    Basta colar os dados assim, um número por linha:

    ```
        10  
        12  
        15  
        18  
        20  
        25  
        25  
        30  
        32  
        35
    ```
## ✍️ Autores
- Lalla Fatima Azahra Rachid
- Denis Queiroz Soutello

Este projeto foi idealizado para fins didáticos e apresentado na disciplina de Estatística da Fatec Jundiaí.