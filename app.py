
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Dashboard de Compras", layout="wide")
with open("style_dark.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.title("📊 Dashboard de Compras")

# Carregar base
try:
    df = pd.read_csv("Base BI.csv")
    st.success(f"✅ Base carregada com sucesso! {df.shape[0]} linhas.")
except Exception as e:
    st.error(f"Erro ao carregar a base: {e}")
    st.stop()

# Verificação de colunas
colunas_necessarias = [
    'Data do pedido', 'Data Entrada NF', 'Data de Remessa', 'Valor total. USD',
    'Planta', 'Automação', 'Nome do fornecedor', 'Pedido', 'Item do pedido', 'Grupo de compras'
]
colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]
if colunas_faltando:
    st.error(f"As seguintes colunas estão faltando: {colunas_faltando}")
    st.stop()

# Conversão de datas e cálculos
df['Data do pedido'] = pd.to_datetime(df['Data do pedido'], errors='coerce')
df['Data Entrada NF'] = pd.to_datetime(df['Data Entrada NF'], errors='coerce')
df['Data de Remessa'] = pd.to_datetime(df['Data de Remessa'], errors='coerce')
df['Lead Time Pedido-Remessa'] = (df['Data de Remessa'] - df['Data do pedido']).dt.days
df['Tempo Remessa-NF'] = (df['Data Entrada NF'] - df['Data de Remessa']).dt.days
df['Status de Entrega'] = df['Tempo Remessa-NF'].apply(lambda x: 'No prazo' if x > 0 else 'Fora do prazo')
df.rename(columns={'Valor total. USD': 'Valor Total USD'}, inplace=True)

# Filtros
st.sidebar.header("Filtros")
anos = df['Data do pedido'].dt.year.dropna().unique()
if len(anos) > 0:
    ano_sel = st.sidebar.selectbox("Ano", sorted(anos, reverse=True))
    df = df[df['Data do pedido'].dt.year == ano_sel]

planta_sel = st.sidebar.multiselect("Planta", options=df['Planta'].dropna().unique(), default=df['Planta'].dropna().unique())
df = df[df['Planta'].isin(planta_sel)]

usar_todos = st.sidebar.checkbox("Selecionar todos os grupos", value=True)
if usar_todos:
    grupo_sel = df['Grupo de compras'].dropna().unique()
else:
    grupo_sel = st.sidebar.multiselect("Grupo de Compras", options=sorted(df['Grupo de compras'].dropna().unique()))
df = df[df['Grupo de compras'].isin(grupo_sel)]

# Indicadores principais
col1, col2 = st.columns(2)
col1.metric("💰 Gasto Total (USD)", f"${df['Valor Total USD'].sum():,.2f}")
pct_auto = df['Automação'].value_counts(normalize=True).get('A', 0) * 100
col2.metric("⚙️ % Pedidos Automáticos", f"{pct_auto:.1f}%")

# Tabs organizadas
tab1, tab2, tab3 = st.tabs(["💸 Gasto e Automação", "📦 Status de Entrega", "📋 Tabela de Pedidos"])

with tab1:
    st.subheader("💸 Top 10 Fornecedores por Gasto")
    top_fornecedores = df.groupby('Nome do fornecedor')['Valor Total USD'].sum().sort_values(ascending=True).tail(10)
    fig_gasto = go.Figure(go.Bar(
        x=top_fornecedores.values,
        y=top_fornecedores.index,
        orientation='h',
        marker_color='royalblue'
    ))
    fig_gasto.update_layout(xaxis_title='USD', yaxis_title='', title='Top 10 Fornecedores por Gasto')
    st.plotly_chart(fig_gasto, use_container_width=True)

    st.subheader("🔄 Distribuição de Pedidos: Automáticos vs Manuais")
    automacao_counts = df['Automação'].value_counts()
    labels = ['Automático' if k == 'A' else 'Manual' for k in automacao_counts.index]
    values = automacao_counts.values
    fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
    fig_donut.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)

with tab2:
    st.subheader("🏅 Top 10 Fornecedores com Mais Pedidos no Prazo")
    top_pontuais = (
        df[df['Status de Entrega'] == 'No prazo']
        .groupby('Nome do fornecedor')
        .size()
        .sort_values(ascending=True)
        .tail(10)
    )
    fig_pontual = go.Figure(go.Bar(
        x=top_pontuais.values,
        y=top_pontuais.index,
        orientation='h',
        marker_color='mediumseagreen'
    ))
    fig_pontual.update_layout(
        xaxis_title='Qtd. de Pedidos no Prazo',
        yaxis_title='',
        title='Top 10 Fornecedores com Entregas no Prazo'
    )
    st.plotly_chart(fig_pontual, use_container_width=True)

    st.subheader("🚨 Top 10 Fornecedores com Mais Pedidos Fora do Prazo")
    top_atrasados = (
        df[df['Status de Entrega'] == 'Fora do prazo']
        .groupby('Nome do fornecedor')
        .size()
        .sort_values(ascending=True)
        .tail(10)
    )
    fig_atrasado = go.Figure(go.Bar(
        x=top_atrasados.values,
        y=top_atrasados.index,
        orientation='h',
        marker_color='crimson'
    ))
    fig_atrasado.update_layout(
        xaxis_title='Qtd. de Pedidos Fora do Prazo',
        yaxis_title='',
        title='Top 10 Fornecedores com Entregas Fora do Prazo'
    )
    st.plotly_chart(fig_atrasado, use_container_width=True)

    st.subheader("📦 Status de Entrega")
    status_counts = df['Status de Entrega'].value_counts()
    fig_status = px.pie(
        names=status_counts.index,
        values=status_counts.values,
        title="Distribuição de Entregas no Prazo vs Fora do Prazo",
        hole=0.4
    )
    st.plotly_chart(fig_status, use_container_width=True)

with tab3:
    st.subheader("📋 Tabela de Pedidos")
    st.dataframe(df[['Pedido','Item do pedido','Data do pedido', 'Nome do fornecedor', 'Planta', 'Valor Total USD']])
