from flask import Flask, redirect, jsonify
from flasgger import Swagger
import db_context

# Services
from services.EquipamentoService import EquipamentoService

app = Flask(__name__)
swagger = Swagger(app)
db_context.init_app(app)


@app.route('/', methods=['GET'])
def documentacao():
    return redirect('/apidocs')


@app.route('/equipamentos', methods=['GET'])
def get_equipamentos():
    """
    Lista todos os equipamentos cadastrados.
    ---
    tags:
      - Equipamentos
    responses:
      200:
        description: Lista de equipamentos
        schema:
          id: Equipamentos
          properties:
            equipamento_id:
              type: integer
              description: ID do equipamento
              default: 1
            equipamento_filial:
              type: string
              description: Filial do equipamento
              default: 01
            equipamento_setor:
              type: string
              description: Setor do equipamento
              default: 01
            equipamento_nome:
              type: string
              description: Nome do equipamento
              default: Equipamento 01
            equipamento_ccusto:
              type: string
              description: Centro de custo do equipamento
              default: 01
    """
    equipamentos, error = EquipamentoService.fetch_equipamentos()
    if error:
        return jsonify(error="Erro ao buscar equipamentos no banco de dados.", details=error), 500
    return {'equipamentos': equipamentos}


if __name__ == '__main__':
    app.run(debug=True)
