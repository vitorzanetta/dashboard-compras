
# 📊 Dashboard de Compras – Streamlit + Plotly

Dashboard interativo desenvolvido com **Streamlit** para análise de desempenho de fornecedores e pedidos de compra. Ideal para uso em aplicações reais de BI em Supply Chain.

## 🚀 Funcionalidades

- 📌 KPIs: Gasto total em USD e percentual de pedidos automáticos
- 🔍 Filtros interativos: por **Ano**, **Planta** e **Grupo de Compras**
- 📈 Gráficos:
  - Top 10 fornecedores por gasto
  - Pedidos no prazo x fora do prazo
  - Distribuição entre pedidos automáticos e manuais
  - Pie chart de status de entrega
- 📋 Tabela interativa com dados principais de cada pedido
- 🎨 Interface com estilo CSS customizado (modo claro ou escuro)

## 🗂️ Estrutura do projeto

```
📁 dashboard-compras/
├── Base BI.csv                # Base de dados (anonimizada ou fictícia)
├── py001_tabs_organizado.py  # Script principal com Streamlit
├── style.css                 # Estilo visual (claro)
├── style_dark.css            # Estilo visual alternativo (escuro)
└── README.md                 # Instruções e documentação do projeto
```

## ▶️ Como executar localmente

Pré-requisitos: Python 3.9+ com Streamlit e Plotly instalados.

```bash
pip install streamlit plotly pandas
streamlit run py001.py
```

## 📸 Exemplos de Tela

<img src="https://via.placeholder.com/700x400.png?text=Dashboard+Principal" alt="Dashboard Compras" />

## 💡 Sugestões de melhoria

- Autenticação de usuários
- Upload dinâmico da base .csv
- Exportação de gráficos em PDF
- Integração com banco de dados

## 👨‍💻 Autor

**Vitor Santos**  
[LinkedIn](https://www.linkedin.com/in/vitor-natã-zanetta-santos-2483a6141/) • [GitHub](https://github.com/vitorzanetta)

---

> Projeto desenvolvido como vitrine de competências em Análise de Dados, BI e visualização interativa com Streamlit.
