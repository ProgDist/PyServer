from flask import Flask, request
from PeixeModel import Peixe
from EmailModel import Email
from google.appengine.api import mail
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/dados', methods=['GET', 'POST'])
def dados():
    if request.method == 'POST':
        p = Peixe(
            temperatura = int(request.form.get('temperatura')),
            ph = int(request.form.get('ph')),
            dureza = int(request.form.get('dureza')),
            alcalinidade = int(request.form.get('alcalinidade')),
            nivelo2 = int(request.form.get('nivelo2')),
            transparencia = int(request.form.get('transparencia')),
        )
        p.put()
        if (p.temperatura > 28 or p.temperatura < 22) or (p.ph > 7 or p.ph < 6) or (p.dureza < 65 or p.dureza > 80) or (p.alcalinidade < 80 or p.alcalinidade > 100) or (p.nivelo2 < 6 or p.nivelo2 > 10) or (p.transparencia < 30 or p.transparencia > 40):
            string_email = 'Leitura dos Sensores!'
            string_email = string_email + '\nTemperatura: ' + request.form.get('temperatura')
            string_email = string_email + '\nPh: ' + request.form.get('ph')
            string_email = string_email + '\nDureza: ' + request.form.get('dureza')
            string_email = string_email + '\nAlcalinidade: ' + request.form.get('alcalinidade')
            string_email = string_email + '\nNivelO2: ' + request.form.get('nivelo2')
            string_email = string_email + '\nTransparencia: ' + request.form.get('transparencia')
            email_query = Email.all()
            for e in email_query:
                mail.send_mail("Peixe@premium-valor-94418.appspotmail.com",
                           e.email,
                          "Alerta - Niveis anormais nos sensores!",
                            string_email)
    if request.method == 'GET':
        p = Peixe(
            temperatura = int(request.args.get('temperatura')),
            ph = int(request.args.get('ph')),
            dureza = int(request.args.get('dureza')),
            alcalinidade = int(request.args.get('alcalinidade')),
            nivelo2 = int(request.args.get('nivelo2')),
            transparencia = int(request.args.get('transparencia')),
        )
        p.put()
        if (p.temperatura > 28 or p.temperatura < 22) or (p.ph > 7 or p.ph < 6) or (p.dureza < 65 or p.dureza > 80) or (p.alcalinidade < 80 or p.alcalinidade > 100) or (p.nivelo2 < 6 or p.nivelo2 > 10) or (p.transparencia < 30 or p.transparencia > 40):
            string_email = 'Leitura dos Sensores!'
            string_email = string_email + '\nTemperatura: ' + request.args.get('temperatura')
            string_email = string_email + '\nPh: ' + request.args.get('ph')
            string_email = string_email + '\nDureza: ' + request.args.get('dureza')
            string_email = string_email + '\nAlcalinidade: ' + request.args.get('alcalinidade')
            string_email = string_email + '\nNivelO2: ' + request.args.get('nivelo2')
            string_email = string_email + '\nTransparencia: ' + request.args.get('transparencia')
            email_query = Email.all()
            for e in email_query:
                mail.send_mail("Peixe@premium-valor-94418.appspotmail.com",
                           e.email,
                           "Alerta - Niveis anormais nos sensores!",
                            string_email)
    return 'ok'

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():

    if request.method == 'POST':
        e = Email(
            email = request.form.get('email'),
        )
        email_query = Email.all()
        for ema in email_query:
            if ema.email == e.email:
                return 'Email '+ema.email+' ja cadastrado!'
        e.put()
        em = request.form.get('email')
    if request.method == 'GET':
        e = Email(
            email = request.args.get('email'),
        )
        email_query = Email.all()
        for ema in email_query:
            if ema.email == e.email:
                return 'Email '+ema.email+' ja cadastrado!'
        e.put()
        em = request.args.get('email')
    return 'Email '+em+' cadastrado!'

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    if request.method == 'POST':
        e = Email(
            email = request.form.get('email'),
        )
        email_query = Email.all()
        for ema in email_query:
            if ema.email == e.email:
                ema.delete()
                return 'Email '+ema.email+' removido!'
        em = request.form.get('email')
    if request.method == 'GET':
        e = Email(
            email = request.args.get('email'),
        )
        email_query = Email.all()
        for ema in email_query:
            if ema.email == e.email:
                ema.delete()
                return 'Email '+ema.email+' removido!'
        em = request.args.get('email')
    return 'Email '+em+' nao encontrado!'

@app.route('/relatorio', methods=['GET', 'POST'])
def relatorio():
    peixe = Peixe.all()
    string_p_bad = 0
    string_p_good = 0

    for p in peixe:
        if (p.temperatura > 28 or p.temperatura < 22) or (p.ph > 7 or p.ph < 6) or (p.dureza < 65 or p.dureza > 80) or (p.alcalinidade < 80 or p.alcalinidade > 100) or (p.nivelo2 < 6 or p.nivelo2 > 10) or (p.transparencia < 30 or p.transparencia > 40):
            string_p_bad += 1
        elif (p.temperatura < 28 and p.temperatura > 22) and (p.ph < 7 and p.ph > 6) and (p.dureza > 65 and p.dureza < 80) and (p.alcalinidade > 80 and p.alcalinidade < 100) and (p.nivelo2 > 6 and p.nivelo2 < 10) and (p.transparencia > 30 and p.transparencia < 40):
            string_p_good += 1
    return 'Leituras Boas: ' + str(string_p_good) + "\n / " + 'Leituras Ruins: ' + str(string_p_bad)

@app.route('/relatorio/<dia>/<mes>/<ano>', methods=['GET', 'POST'])
def relatoriodata(dia, mes, ano):
    data = datetime.datetime(int(ano),int(mes),int(dia),0,0,0)
    peixe = Peixe.all()
    peixe.filter('data >=', data)
    data += datetime.timedelta(days=1)
    peixe.filter('data <', data)
    string_p_bad = 0
    string_p_good = 0

    for p in peixe:
        if (p.temperatura > 28 or p.temperatura < 22) or (p.ph > 7 or p.ph < 6) or (p.dureza < 65 or p.dureza > 80) or (p.alcalinidade < 80 or p.alcalinidade > 100) or (p.nivelo2 < 6 or p.nivelo2 > 10) or (p.transparencia < 30 or p.transparencia > 40):
            string_p_bad += 1
        elif (p.temperatura < 28 and p.temperatura > 22) and (p.ph < 7 and p.ph > 6) and (p.dureza > 65 and p.dureza < 80) and (p.alcalinidade > 80 and p.alcalinidade < 100) and (p.nivelo2 > 6 and p.nivelo2 < 10) and (p.transparencia > 30 and p.transparencia < 40):
            string_p_good += 1
    return 'Leituras Boas: ' + str(string_p_good) + "\n / " + 'Leituras Ruins: ' + str(string_p_bad)

@app.route('/relatoriobd', methods=['GET', 'POST'])
def relatoriobd():
    peixe = Peixe.all()
    string_p = ""
    for p in peixe:
        string_p = string_p + " / " + "Data: " + str(p.data) + " / Temperatura: " + str(p.temperatura) + " / Ph: " + str(p.ph) + " / Dureza: " + str(p.dureza) + " / Alcalinidade: " + str(p.alcalinidade) + " / NivelO2: " + str(p.nivelo2) + " / Transparencia: " + str(p.transparencia) + "\r\n"
    return string_p

@app.route('/relatoriobd/<dia>/<mes>/<ano>', methods=['GET', 'POST'])
def relatoriobddata(dia, mes, ano):
    data = datetime.datetime(int(ano),int(mes),int(dia),0,0,0)
    peixe = Peixe.all()
    peixe.filter('data >=', data)
    data += datetime.timedelta(days=1)
    peixe.filter('data <', data)
    string_p = ""
    for p in peixe:
        string_p = string_p + " / " + "Data: " + str(p.data) + " / Temperatura: " + str(p.temperatura) + " / Ph: " + str(p.ph) + " / Dureza: " + str(p.dureza) + " / Alcalinidade: " + str(p.alcalinidade) + " / NivelO2: " + str(p.nivelo2) + " / Transparencia: " + str(p.transparencia) + "\r\n"
    return string_p

if __name__ == '__main__':
    app.run()
