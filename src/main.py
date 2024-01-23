from flask import Flask, redirect
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)

# Agora, inicializamos o contexto do banco de dados
import db_context

db_context.init_app(app)  # Isso inicializa o SQLAlchemy

# E agora inicializamos o Marshmallow
ma = Marshmallow(app)

from routing import initialize_routes
initialize_routes(app)


@app.route('/', methods=['GET'])
def documentacao():
    return redirect('/apidocs')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
