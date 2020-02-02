from crypto import app
from flask import render_template, request, redirect, url_for
from crypto.forms import PurchaseForm

cryptos = {"EUR":1, "BTC":3.5, "ETH":4.8, "XRP":3.76, "LTC":6.4, "BCH":1.5, "BNB":76.4, "USDT":2.6, "EOS":4.3, "BSV":1.41, "XLM":2.43, "ADA":3.6, "TRX":6.8}

@app.route("/")
def index():
    slctFrom=None
    slctTo=None
    units=0
    quant = 0
    pu = 0
    return render_template("index.html", data=[quant, pu, units, slctFrom, slctTo])


@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    form = PurchaseForm(request.form)
    slctFrom=request.values.get("slct_from")
    slctTo=request.values.get("slct_to")
    units=request.values.get("inputCantidad")
    quant = 0
    pu = 0
    if slctFrom and slctTo != '':
        quant=(float(units) * float(cryptos[slctTo])) / float(cryptos[slctFrom])
        pu = float(cryptos[slctTo]) / float(cryptos[slctFrom])


    if request.method == 'GET':

        return render_template("purchase.html", form=form, data=[quant,pu])

    if request.values.get("submitCalcular"):

        return render_template("purchase.html", form=form, data=[quant,pu, slctFrom])

    if request.values.get("submitCompra"):

        return render_template("index.html", form=form, data=[quant, pu, int(units), slctFrom, slctTo])


@app.route("/status")
def inverter():
    return render_template("status.html")
