import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json
import plotly.graph_objects as go


def get_fund_data(fund_name):
    index = array_funds.index(fund_name)
    list_positions = eval(df['posicoes'][index])[0]['Posicoes']
    array_tickers = [i['Ticker'] for i in list_positions]
    array_pl = [float(i['% Pl'].replace(",", ".")) for i in list_positions]
    fig = go.Figure(go.Bar(
            x = array_pl,
            y = array_tickers,
            orientation='h',
            marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1))))
    fig.update_layout(
        width=800,
        height=700,
    )
    st.plotly_chart(fig)
    st.title("Histórico quantidade de papéis")
    with st.expander("O que é o histórico da quantidade de papéis?"):
        st.write("""
            O histórico da quantidade de papéis mostra a quantidade de papéis que o fundo possui ao longo dos últimos meses.

            E qual a sua utilidade?
            Ele permite que você acompanhe se o fundo está aumentando ou diminuindo sua posição em um ativo específico.
        """)
    selected_ticker = st.selectbox("Selecione o Ticker", array_tickers)
    if selected_ticker:
        get_fund_qtd(selected_ticker, fund_name)


def get_fund_qtd(ticker, fund_name):
    index = array_funds.index(fund_name)
    list_positions_brute = eval(df['posicoes'][index])
    array_data = []
    array_qtd = []
    for i in list_positions_brute:
        for v in i['Posicoes']:
            if v['Ticker'] == ticker:
                array_data.insert(0, i['Mes'])
                array_qtd.insert(0, int(v['Quantidade'].replace(".", "")))
    st.metric(label="Quantidade Atual", value="10M", delta="-0.9M")
    fig2 = px.line(x = array_data, y = array_qtd, markers = True, color_discrete_sequence = ['#32AB60'] )
    fig2.update_layout(xaxis_title = "Mês", yaxis_title = "Quantidade")
    st.plotly_chart(fig2)


def get_fund_byticker(ticker):
    fund_that_has = []
    for index in range(len(array_funds)):
        list_positions = [i['Ticker'] for i in eval(df['posicoes'][index])[0]['Posicoes']]
        if ticker in list_positions:
            fund_that_has.append(array_funds[index])

    st.table(data = fund_that_has)


def gerador_match(lista_tickers):
    carteira_final = []

    for ind in range(len(lista_tickers)):
        if ind == 0:
            index1 = array_funds.index(lista_tickers[ind])
            list_positions1 = eval(df['posicoes'][index1])[0]['Posicoes']
            array_tickers1 = [i['Ticker'] for i in list_positions1]

            index2 = array_funds.index(lista_tickers[ind+1])
            list_positions2 = eval(df['posicoes'][index1])[0]['Posicoes']
            array_tickers2 = [i['Ticker'] for i in list_positions2]

            carteira_final = set(array_tickers1) & set(array_tickers2)
        if ind == 1:
            continue 
        else: 
            index1 = array_funds.index(lista_tickers[ind])
            list_positions1 = eval(df['posicoes'][index1])[0]['Posicoes']
            array_tickers1 = [i['Ticker'] for i in list_positions1]
            carteira_final = set(array_tickers1) & set(carteira_final)
    st.dataframe(data = carteira_final)


def get_initial_final_position(datafram):
    for i in range(len(datafram['posicoes'])):
        posInicial = eval(datafram['posicoes'][i])[-1]
        posFinal = eval(datafram['posicoes'][i])[0]
        datafram.loc[i, 'init_final_position'] = str([posInicial, posFinal])
    return datafram


def get_notices(x):
    notices = []
    for a in eval(x)[0]['Posicoes']:
        for b in eval(x)[-1]['Posicoes']:
            if a['Ticker'] == b['Ticker']:
                if int(a['Quantidade'].replace(".", "")) > int(b['Quantidade'].replace(".", "")):
                    notices.append(" comprou " + str(int(a['Quantidade'].replace(".", "")) - int(b['Quantidade'].replace(".", ""))) + " quantidades de " + a['Ticker'])
                else:
                    notices.append(" vendeu " + str(int(b['Quantidade'].replace(".", "")) - int(a['Quantidade'].replace(".", ""))) + " quantidades de " + a['Ticker'])
    return notices

def get_final_notice(datafram):
    df['news'] = df['init_final_position'].apply(get_notices)
    absolute_notice = []
    for i in datafram['Fundo']:
        nomeFundo = ' '.join(i.split()[:2])
        array_newFinal = []
        for a in datafram['news'].loc[datafram['Fundo'] == i]:
            for b in a:
                new_final = nomeFundo + b
                array_newFinal.append(new_final)
                absolute_notice.append(new_final)
        datafram.loc[datafram['Fundo'] == i, 'news_final'] = str(array_newFinal)
    return absolute_notice
            








df = pd.read_csv('./MVP-Pront.csv')
array_funds = df['Fundo'].tolist()
list_positions = eval(df['posicoes'][0])[0]['Posicoes']
all_tickers = [eval(df['posicoes'][index])[0]['Posicoes'][i]['Ticker'] for index in range(len(array_funds)) for i in range(len(list_positions))]


                                #------# COMPONENTES DA PÁGINA  #-------#

st.title("Movimentações para ficar de olho")
get_initial_final_position(df)
with st.expander("Como funciona o algoritmo de movimentação?"):
    st.write("""
        O campo de **Insigths** apresenta as principais movimentações dos fundos nos útimos meses, ou seja, 
        as compras e vendas de ativos que mais impactaram a carteira do fundo.

        E qual a sua utilidade?
    """)
st.table(data = get_final_notice(df))


st.title("Busca de Fundos pelo Ticker")
with st.expander("O que é a busca de fundos pelo Ticker?"):
    st.write("""
        A busca de fundos pelo ticker fornece uma lista de fundos que possuem o ativo selecionado em sua carteira.

        E qual a sua utilidade?
    """)
selected_ticker_search = st.selectbox("Selecione o ticker", all_tickers)
if selected_ticker_search:
    get_fund_byticker(selected_ticker_search)


st.title("Carteira Fundo")
with st.expander("O que é a carteira do fundo?"):
    st.write("""
        O campo de carteira do fundo mostra todos os tickers que compõem a carteira do fundo selecionado,
        além de apresentar também o percentual de participação de cada ativo na carteira do fundo.
    """)
selected_fund = st.selectbox("Selecione o Fundo", array_funds)
if selected_fund:
    get_fund_data(selected_fund)


st.title("Gerador de Carteira ")
with st.expander("Como funciona o algoritmo do gerador de carteiras?"):
    st.write("""
        O campo de carteira do fundo mostra todos os tickers que compõem a carteira do fundo selecionado,
        além de apresentar também o percentual de participação de cada ativo na carteira do fundo.
    """)
options = st.multiselect(
'Selecione seus fundos favoritos',
array_funds)

if st.button('Gerar Carteira '):
    gerador_match(options)


# Define a função a ser executada quando o botão for clicado
def button_clicked():
    st.write("Botão clicado!")

# Adiciona o botão na barra lateral
st.sidebar.title("Menu")
if st.sidebar.button("Movimentações para ficar de olho"):
    button_clicked()
if st.sidebar.button("Busca de fundos pelo ticker"):
    button_clicked()
if st.sidebar.button("Carteira Fundo"):
    button_clicked()
if st.sidebar.button("Gerador de Match"):
    button_clicked()