from flask import Flask, jsonify
import socket

app = Flask(__name__)
contador = 0

@app.route('/')
def hello():
    """Endpoint principal que mostra o nome do pod e um contador"""
    global contador
    contador += 1
    return jsonify({
        'mensagem': 'Olá! Este é um exemplo simples de Kubernetes',
        'pod': socket.gethostname(),
        'contador': contador
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 