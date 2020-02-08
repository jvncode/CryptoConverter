from crypto import app
from flask import render_template, request, redirect, url_for
from crypto.forms import PurchaseForm
import datetime
import sqlite3
import json
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

BBDD = './data/CryptoData.db'
API_KEY=app.config['API_KEY']

cryptos = ("BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")
dt = datetime.datetime.now()

def api(cryptoFrom, cryptoTo):

    url= "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={}&convert={}&CMC_PRO_API_KEY='70b558a8-8ad0-4d2b-8e9f-559cc06fdcd3'".format(cryptoTo, cryptoFrom)

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return data['data']['quote'][cryptoFrom]['price']


def dataQuery(consulta):

    conex = sqlite3.connect(BBDD)
    cursor = conex.cursor()

    movs = cursor.execute(consulta).fetchall()

    if len(movs) == 1:
        movs = movs[0]
    elif len(movs) == 0:
        movs = None

    conex.commit()
    conex.close()

    return movs

@app.route("/")
def index():

    registros = dataQuery("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVEMENTS;")

    return render_template("index.html", registros = registros)


@app.route("/purchase", methods=['GET', 'POST'])
def purchase():

    form = PurchaseForm(request.form)
    slctFrom=request.values.get("slct_from")
    slctTo=request.values.get("slct_to")
    units=request.values.get("inputCantidad")
    quant = 0
    pu = 0

    if request.method == 'GET':

        return render_template("purchase.html", form=form , data=[quant,pu])


    if request.values.get("submitCalcular"):

        dataQuant = api(slctFrom, slctTo)
        quant = float(dataQuant)*float(units)
        pu = dataQuant

        return render_template("purchase.html", form=form, data=[quant, pu, slctFrom])

    if request.values.get("submitCompra"):

        #Calculo de saldo de la moneda con la que se quiere comprar

        saldoStr = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%{}%";'.format(slctFrom))
        saldo = saldoStr[0]

        if slctFrom == 'EUR' or saldo != None:

            conex = sqlite3.connect(BBDD)
            cursor = conex.cursor()
            mov = "INSERT INTO MOVEMENTS(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?);"

            dataQuant = api(slctFrom, slctTo)
            quant = float(dataQuant)*float(units)
            fecha=dt.strftime("%d/%m/%Y")
            hora=dt.strftime("%H:%M:%S")

            try:
                cursor.execute(mov, (fecha, hora, slctFrom, float(quant), slctTo, float(units)))
            except sqlite3.Error:
                quant = 0
                pu = 0
                errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
                return render_template("purchase.html", form=form , errorDB=errorDB, data=[quant,pu])

            conex.commit()
            registros = dataQuery("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVEMENTS;")
            conex.close()

            # (OJO!) Falta restar unidades de crytos que se gastan (excepto EUR)

            return render_template("index.html", form=form, registros=registros)
        else:
            quant = 0
            pu = 0
            alert = "NO EXISTE SALDO DE COMPRA EN LA CRYPTOMONEDA {}".format(slctFrom)
            return render_template("purchase.html", form=form, data=[quant, pu, slctFrom], alert=alert)


@app.route("/status")
def inverter():

    # Calculo Inversion

    movOrNot = dataQuery("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVEMENTS;")

    if movOrNot == None:
        return render_template("status.html", movOrNot=True)

    InverFrom= dataQuery('SELECT SUM(from_quantity) FROM MOVEMENTS WHERE from_currency LIKE "%EUR%";')
    InverTo= dataQuery('SELECT SUM(from_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%EUR%";')

    for x in InverFrom:
        totalInverFrom = x

    if None in InverTo:
        totalInverTo = 0
    else:
        for y in InverTo:
            totalInverTo = y

    totalInver = totalInverFrom + totalInverTo

    # Calculo saldo de Cryptomonedas

    balanceBTC = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%BTC%";')
    balanceETH = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%ETH%";')
    balanceXRP = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%XRP%";')
    balanceLTC = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%LTC%";')
    balanceBCH = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%BCH%";')
    balanceBNB = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%BNB%";')
    balanceUSDT = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%USDT%";')
    balanceEOS = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%EOS%";')
    balanceBSV = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%BSV%";')
    balanceXLM = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%XLM%";')
    balanceADA = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%ADA%";')
    balanceTRX = dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%TRX%";')

    cryptoBalance = [balanceBTC[0], balanceETH[0],balanceXRP[0], balanceLTC[0],balanceBCH[0], balanceBNB[0], balanceUSDT[0],balanceEOS[0], balanceBSV[0], balanceXLM[0], balanceADA[0], balanceTRX[0]]

    # Cambia None por 0 para listado de saldo de Cryptos
    for x in range(len(cryptoBalance)):
        if cryptoBalance[x] == None:
            cryptoBalance[x]=0

    # Calculo Valor Actual de todas las cryptomonedas en Euros y totalizarlas en Status
    xi = 0
    cryptoValorActual = {}
    valorAct = 0
    for coin in cryptos:
        cryptoValorActual[coin] = api('EUR',coin) * cryptoBalance[xi]
        valorAct += cryptoValorActual[coin]
        xi += 1

    return render_template("status.html", totalInver=totalInver, cryptoBalance=cryptoBalance, valorAct=valorAct)
