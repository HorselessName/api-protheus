from flask import Flask, redirect, jsonify, request
from flasgger import Swagger
import db_context

# Routes - Precisa ser diferente de 'routes' para não conflitar com o módulo 'routes'.
from routing import initialize_routes

app = Flask(__name__)
swagger = Swagger(app)
db_context.init_app(app)
initialize_routes(app)


@app.route('/', methods=['GET'])
def documentacao():
    return redirect('/apidocs')


if __name__ == '__main__':
    app.run(debug=True)
