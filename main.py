import pandas as pd
from flask import Flask
from flask import jsonify
import pandas_datareader.data as web
from pandas_datareader import data as pdr
import datetime
import investpy as inv
from flask_cors import CORS
# import yfinance as yf




app = Flask(__name__)

CORS(app)

@app.route('/funds')
def fundspage():
  df = pd.read_csv("cad_fi.csv", encoding="ISO-8859-1", sep = ';')
  df_ = df[["DENOM_SOCIAL", "CNPJ_FUNDO", "SIT" ]]

  nomes = []
  cnpj = []
  situacao = []
  
  for nome in df["DENOM_SOCIAL"]:
    nomes.append(nome)
  for cnp in df["CNPJ_FUNDO"]:
    cnpj.append(cnp)
  for sit in df["SIT"]:
    situacao.append(sit)

  dict_list = []

  for i in range(len(nomes)):
      dict = {}
      dict['Nome'] = nomes[i]
      dict['CNPJ'] = cnpj[i]
      dict['Situação'] = situacao[i]
      dict_list.append(dict)
  
  return jsonify(dict_list)


@app.route('/companies')
def companiespage():
    df = pd.read_csv("cad_cia_aberta.csv", encoding="ISO-8859-1", sep = ';')
    df_ = df[["DENOM_SOCIAL", "CNPJ_CIA", "DT_CONST", "SIT", "UF_RESP" ]]

    nomes = []
    cnpj = []
    dt_const = []
    situacao = []   
    uf = []

    for nome in df["DENOM_SOCIAL"]:
        nomes.append(nome)
    for cnp in df["CNPJ_CIA"]:
        cnpj.append(cnp)
    for const in df["DT_CONST"]:
        dt_const.append(const)
    for sit in df["SIT"]:
        situacao.append(sit)
    for uff in df["UF_RESP"]:
        uf.append(uff)
            
    dict_list = []

    for i in range(len(nomes)):
        dict = {}
        dict['NOME'] = nomes[i]
        dict['CNPJ'] = cnpj[i]
        dict['DATA CONST'] = dt_const[i]
        dict['SIT'] = situacao[i]
        dict['UF RESP'] = uf[i]
        dict_list.append(dict)

    return jsonify(dict_list)

# @app.route('/companies/<ticker>')
# def pricespage(ticker):
#   #df = inv.get_stock_recent_data(stock=str(ticker), country='brazil')
#   yf.pdr_override()
#   df = pdr.get_data_yahoo(str(ticker) + '.SA')

#   datas = []
#   open_ = []
#   high = []
#   low = []
#   close = []
#   volume = []

#   for uff in df['Open'].to_frame().transpose():
#       datas.append(uff)
#   for nome in df["Open"]:
#       open_.append(nome)
#   for cnp in df["High"]:
#       high.append(cnp)
#   for const in df["Low"]:
#       low.append(const)
#   for sit in df["Close"]:
#       close.append(sit)
#   for sit in df["Volume"]:
#       volume.append(sit)

        
#   dict_list = []

#   for i in range(len(df)):
#       dict = {}
#       dict['DATE'] = datas[i].strftime("%d/%m/%Y")
#       dict['OPEN'] = open_[i]
#       dict['HIGH'] = high[i]
#       dict['LOW'] = low[i]
#       dict['CLOSE'] = close[i]
#       dict['VOLUME'] = volume[i]

#       dict_list.append(dict)
        
#   return jsonify(dict_list)


# @app.route('/currencies/<ticker>')
# def pricescurrencypage(ticker):
#     df = inv.currency_crosses.get_currency_cross_recent_data(ticker+'/BRL', as_json=False, order='descending', interval='Daily')

#     date = []
#     open_ = []
#     high = []
#     low = []
#     close = []

#     for dat in df['Open'].to_frame().transpose():
#         date.append(dat)
#     for i in df["Open"]:
#         open_.append(i)
#     for cnp in df["High"]:
#         high.append(cnp)
#     for const in df["Low"]:
#         low.append(const)
#     for clos in df["Close"]:
#         close.append(clos)
        
#     dict_list = []

#     for i in range(len(df['Open'])):
#         dict = {}
#         dict['DATE'] = date[i].strftime("%d/%m/%Y")
#         dict['OPEN'] = open_[i]
#         dict['HIGH'] = high[i]
#         dict['LOW'] = low[i]
#         dict['CLOSE'] = close[i]

#         dict_list.append(dict)
        
#     return jsonify(dict_list)


@app.route('/fed/tax')
def tax_fed():
    start = datetime.datetime(1900, 1, 1)
    rate_ = web.DataReader('DFEDTARU', 'fred', start)
    taxa = []
    data = []
    for date in rate_.transpose():
        data.append(date)
    for tax in rate_['DFEDTARU']:
        taxa.append(tax)                
    dict_list = []
    for i in range(len(rate_)):
        dict = {}
        dict['DATA'] = data[i].strftime("%d/%m/%Y")
        dict['TAXA'] = taxa[i]

        dict_list.append(dict)

    return jsonify(dict_list)


@app.route('/getPosition/<fund_name>')
def get_fund_data(fund_name):
    df = pd.read_csv('./ATLAS PROJECT/MVP-Pront.csv')
    array_funds = df['Fundo'].tolist()
    index = array_funds.index(fund_name)
    list_positions = eval(df['posicoes'][index])[0]['Posicoes']
    array_tickers = [i['Ticker'] for i in list_positions]
    array_pl = [float(i['% Pl'].replace(",", ".")) for i in list_positions]

    return jsonify(array_tickers, array_pl)


@app.route('/searchFundByTicker/<ticker>')
def get_fund_byticker(ticker):
    ticker = ticker.upper()
    df = pd.read_csv('./ATLAS PROJECT/MVP-Pront.csv')
    array_funds = df['Fundo'].tolist()
    fund_that_has = []
    for index in range(len(array_funds)):
        list_positions = [i['Ticker'] for i in eval(df['posicoes'][index])[0]['Posicoes']]
        if ticker in list_positions:
            fund_that_has.append(array_funds[index])

    return jsonify(fund_that_has)



@app.route('/getallfunds')
def get_all_funds():
    df = pd.read_csv('./ATLAS PROJECT/MVP-Pront.csv')
    array_funds = df['Fundo'].tolist()
    return jsonify(array_funds)


@app.route('/updates')
def get_updates():
    df = pd.read_csv('./ATLAS PROJECT/MVP-Pront.csv')

    def get_initial_final_position(datafram):
        for i in range(len(datafram['posicoes'])):
            posInicial = eval(datafram['posicoes'][i])[-1]
            posFinal = eval(datafram['posicoes'][i])[0]
            datafram.loc[i, 'init_final_position'] = str([posInicial, posFinal])
        return datafram
    get_initial_final_position(df)
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
    
    df['news'] = df['init_final_position'].apply(get_notices)
    absolute_notice = []
    for i in df['Fundo']:
        nomeFundo = ' '.join(i.split()[:2])
        array_newFinal = []
        for a in df['news'].loc[df['Fundo'] == i]:
            for b in a:
                new_final = nomeFundo + b
                array_newFinal.append(new_final)
                absolute_notice.append(new_final)
        df.loc[df['Fundo'] == i, 'news_final'] = str(array_newFinal)
    return jsonify(absolute_notice)

@app.route('/alltickers')
def get_alltickers():
    df = pd.read_csv('./ATLAS PROJECT/MVP-Pront.csv')
    array_funds = df['Fundo'].tolist()
    list_positions = eval(df['posicoes'][0])[0]['Posicoes']
    all_tickers = list(set([eval(df['posicoes'][index])[0]['Posicoes'][i]['Ticker'] for index in range(len(array_funds)) for i in range(len(list_positions))]))
    return jsonify(all_tickers)


@app.route('/generator/<funds>')
def gerador_match(funds):
    lista_tickers = funds.split('%20', ' ')
    df = pd.read_csv('./ATLAS PROJECT/MVP-Pront.csv')
    array_funds = df['Fundo'].tolist()
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
    return carteira_final

if __name__ == "__main__":
  app.run(debug=True)
