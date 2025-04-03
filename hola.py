print('Bienvenido al sistema de lavanderia de la UAB')
print('soy elia')
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola, Flask está funcionando!"

if __name__ == '__main__':
    app.run(debug=True)
