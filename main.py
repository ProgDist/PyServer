from flask import Flask, request
from PeixeModel import Peixe, db

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
    return 'ok'

if __name__ == '__main__':
    app.run()
