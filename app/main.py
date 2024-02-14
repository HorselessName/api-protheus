import os

from flask import Flask, redirect
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flasgger import Swagger

# Antes de tudo, carregar as variáveis de ambiente do arquivo .env, para o Flask e SQLAlchemy.
# Ref: https://github.com/pallets/flask/blob/0c0b31a789f8bfeadcbcf49d1fb38a00624b3065/src/flask/app.py#L925
from dotenv import load_dotenv
load_dotenv(".env")  # Uso o `load_dotenv` pois o Flask por padrão usa o `load_dotenv`.

print("SQL_SERVER_HOST: ", os.getenv('SQL_SERVER_HOST', 'Valor de SQL_SERVER_HOST não carregado'))

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)

# Agora, inicializamos o contexto do banco de dados
import db_context

# Configurar SQLAlchemy no objeto app do Flask.
app.config['SQLALCHEMY_DATABASE_URI'] = db_context.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recomendado para desabilitar sinalizações de modificação

db_context.init_app(app)  # Isso inicializa o SQLAlchemy

# E agora inicializamos o Marshmallow
ma = Marshmallow(app)

from routing import initialize_routes
initialize_routes(app)


@app.route('/', methods=['GET'])
def documentacao():
    return redirect('/apidocs')


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 9000
    app.run(host=host, port=port, debug=True)
