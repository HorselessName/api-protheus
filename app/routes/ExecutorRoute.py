from flask import Blueprint, jsonify, request
from flasgger import swag_from
from services.ExecutorService import ExecutorService

blueprint_executores = Blueprint('executores', __name__)


@blueprint_executores.route('/manutencao/executores/listar', methods=['GET'])
@swag_from('./api_docs/ExecutoresDocs.yaml')
def get_executores_por_especialidade():
    # Pegar o Argumento por Query String
    especialidade_nome = request.args.get('especialidade_nome')
    return jsonify(ExecutorService.get_executores_por_especialidade(especialidade_nome)), 200


@blueprint_executores.route('/manutencao/executor/listar', methods=['GET'])
@swag_from('./api_docs/ExecutorDocs.yaml')
def get_executor_por_matricula():
    # Pegar o Argumento por Query String
    executor_matricula = request.args.get('executor_matricula')
    return jsonify(ExecutorService.get_executor_por_matricula(executor_matricula)), 200
