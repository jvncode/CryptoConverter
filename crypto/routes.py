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

    if len(movs) == 0:
        movs = None

    conex.commit()
    conex.close()

    return movs

def cryptoSaldo():

    balanceBTC = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "BTC"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "BTC"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')

    balanceETH = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "ETH"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "ETH"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceXRP = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "XRP"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "XRP"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceLTC = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "LTC"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "LTC"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceBCH = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "BCH"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "BCH"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceBNB = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "BNB"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "BNB"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceUSDT = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "USDT"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "USDT"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceEOS = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "EOS"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "EOS"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceBSV = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "BSV"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "BSV"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceXLM = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "XLM"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "XLM"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceADA = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "ADA"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "ADA"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')
    balanceTRX = dataQuery('''
                            WITH BALANCE
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE to_currency LIKE "TRX"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVEMENTS
                            WHERE from_currency LIKE "TRX"
                            )
                            SELECT SUM(saldo)
                            FROM BALANCE
                            ''')

    cryptoBalance = [balanceBTC[0], balanceETH[0], balanceXRP[0], balanceLTC[0], balanceBCH[0], balanceBNB[0], balanceUSDT[0], balanceEOS[0], balanceBSV[0], balanceXLM[0], balanceADA[0], balanceTRX[0]]

    for x in range(len(cryptoBalance)):
        if cryptoBalance[x] == (None,):
            cryptoBalance[x]=0
        else:
            cryptoBalance[x]=cryptoBalance[x][0]

    return cryptoBalance

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
        if not form.validate():
            quant = 0
            pu = 0
            validError = "OPERACIÓN INCORRECTA - LA CANTIDAD DEBE SER NUMÉRICA Y SUPERIOR A 0"
            return render_template("purchase.html", form=form , validError=validError, data=[quant,pu])

        # Validacion de monedas distintas

        if slctFrom == slctTo:
            quant = 0
            pu = 0
            cryptoError = "OPERACIÓN INCORRECTA - DEBE ELEGIR DOS MONEDAS DISTINTAS"
            return render_template("purchase.html", form=form , cryptoError=cryptoError, data=[quant,pu])
        
        # Validacion de compatibilidad de calculo entre criptomendas

        if slctFrom == 'EUR' and slctTo != 'BTC':
            quant = 0
            pu = 0
            cryptoIncompatible = "OPERACIÓN INCORRECTA - NO PUEDE COMPRAR {} CON EUROS".format(slctTo)
            return render_template("purchase.html", form=form , cryptoIncompatible=cryptoIncompatible, data=[quant,pu])

        if slctTo == 'EUR'and slctFrom != "BTC":
            quant = 0
            pu = 0
            cryptoIncompatible = "OPERACIÓN INCORRECTA - NO PUEDE COMPRAR EUROS CON {}".format(slctFrom)
            return render_template("purchase.html", form=form , cryptoIncompatible=cryptoIncompatible, data=[quant,pu])


        dataQuant = api(slctFrom, slctTo)
        quant = float(dataQuant)*float(units)
        pu = dataQuant

        return render_template("purchase.html", form=form, data=[quant, pu, slctFrom])

    if request.values.get("submitCompra"):

        # Validacion de monedas distintas

        if slctFrom == slctTo:
            quant = 0
            pu = 0
            cryptoError = "OPERACIÓN INCORRECTA - DEBE ELEGIR DOS MONEDAS DISTINTAS"
            return render_template("purchase.html", form=form , cryptoError=cryptoError, data=[quant,pu])

        # Validacion de compatibilidad de compra entre criptomendas

        if slctFrom == 'EUR' and slctTo != 'BTC':
            quant = 0
            pu = 0
            cryptoIncompatible = "OPERACIÓN INCORRECTA - NO PUEDE COMPRAR {} CON EUROS".format(slctTo)
            return render_template("purchase.html", form=form , cryptoIncompatible=cryptoIncompatible, data=[quant,pu])

        if slctTo == 'EUR'and slctFrom != "BTC":
            quant = 0
            pu = 0
            cryptoIncompatible = "OPERACIÓN INCORRECTA - NO PUEDE COMPRAR EUROS CON {}".format(slctFrom)
            return render_template("purchase.html", form=form , cryptoIncompatible=cryptoIncompatible, data=[quant,pu])


        #Calculo de saldo de la moneda con la que se quiere comprar
        if slctFrom == 'EUR':
            saldo = 9999999999
        else:
            saldoStr = dataQuery('''
                        WITH BALANCE
                        AS
                        (
                        SELECT SUM(to_quantity) AS saldo
                        FROM MOVEMENTS
                        WHERE to_currency LIKE "%{}%"
                        UNION ALL
                        SELECT -SUM(from_quantity) AS saldo
                        FROM MOVEMENTS
                        WHERE from_currency LIKE "%{}%"
                        )
                        SELECT SUM(saldo)
                        FROM BALANCE;
                        '''.format(slctFrom, slctFrom))
            if saldoStr[0] == (None,):
                saldo = 0
            else:
                saldo = saldoStr[0][0]

        if slctFrom == 'EUR' or saldo != 0:

            fecha=dt.strftime("%d/%m/%Y")
            hora=dt.strftime("%H:%M:%S")
            dataQuant = api(slctFrom, slctTo)
            quant = float(dataQuant)*float(units)

            # Comprobación de saldo suficiente con la crypto que se quiere comprar

            if saldo >= quant or slctFrom == 'EUR':

                conex = sqlite3.connect(BBDD)
                cursor = conex.cursor()
                mov = "INSERT INTO MOVEMENTS(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?);"

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

                return render_template("index.html", form=form, registros=registros)
            else:
                pu = dataQuant
                sinSaldo = "NO TIENE SALDO SUFICIENTE EN {} PARA REALIZAR ESTA OPERACIÓN".format(slctFrom)
                return render_template("purchase.html", form=form , sinSaldo=sinSaldo, data=[quant,pu])
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
    totalInverFrom = 0
    totalInverTo = 0
    for x in range(len(InverFrom)):
        if InverFrom[x] == (None,):
            totalInverFrom += 0
        else:
            InverFromInt = InverFrom[x][0]
            totalInverFrom += InverFromInt

    for x in range(len(InverTo)):
        if InverTo[x] == (None,):
            totalInverTo += 0
        else:
            InverToInt = InverTo[x][0]
            totalInverTo += InverToInt

    totalInver = totalInverFrom + totalInverTo

    # Calculo saldo de Cryptomonedas

    cryptoSaldo()

    # Calculo Valor Actual de todas las cryptomonedas en Euros y totalizarlas en Status
    xi = 0
    cryptoValorActual = {}
    valorAct = 0
    for coin in cryptos:
        cotizacion = api('EUR',coin)
        saldoCoin = cryptoSaldo()[xi]
        cryptoValorActual[coin] = cotizacion * saldoCoin
        valorAct += cryptoValorActual[coin]
        xi += 1

    return render_template("status.html", totalInver=totalInver, cryptoBalance=cryptoSaldo(), valorAct=valorAct)
