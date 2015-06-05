from flask import Flask, request
from PeixeModel import Peixe, db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/dados', methods=['GET', 'POST'])
def dados():
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
