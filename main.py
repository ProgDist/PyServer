from flask import Flask, request
from PeixeModel import Peixe
from EmailModel import Email
from google.appengine.api import mail
from google.appengine.ext import db

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


if __name__ == '__main__':
    app.run()
