from flask import Blueprint, jsonify, request
from services.FilialService import FilialService  # Ajuste conforme sua estrutura de imports

blueprint_filial = Blueprint('filial', __name__)


@blueprint_filial.route('/filial/listar', methods=['GET'])
def get_filiais():
    """
    Lista todas as filiais cadastradas.
    ---
    tags:
      - Filiais
    responses:
      200:
        description: Lista de filiais
        schema:
          id: Filiais
          properties:
            filial_grupo:
              type: integer
              description: ID da grupo da filial
            filial_codigo:
              type: string
              description: Código da filial
            filial_nome:
              type: string
              description: Nome da filial
            filial_familia:
                type: string
                description: Nome da Família (Grupo) da filial
      400:
        description: Requisição inválida (parâmetros faltando)
        schema:
          id: Error
          properties:
            error:
              type: string
              description: Mensagem de erro
    """
    filiais, error = FilialService.buscar_todas_filiais()
    if error:
        return jsonify(error=error), 400
    return {'filiais': filiais}


from flask import request


@blueprint_filial.route('/filial/setores', methods=['GET'])
def get_setores():
    """
    Lista os Setores
    ---
    tags:
      - Setores
    summary: Recupera setores da filial.
    description: Esta rota é responsável por buscar e retornar os setores associados a uma filial. Ao clicar no botão, a query é executada automaticamente.
    parameters:
      - name: setor_param
        in: query
        type: string
        description: Parâmetro de setor.
      - name: grupo_condicional
        in: query
        type: string
        description: Grupo condicional.
      - name: grupo_default
        in: query
        type: string
        description: Grupo padrão.
      - name: filial_condicional
        in: query
        type: string
        description: Filial condicional.
      - name: setor_filial
        in: query
        type: string
        description: Parâmetro de filial para setor.
      - name: setor_grupo
        in: query
        type: string
        description: Parâmetro de grupo para setor.
    responses:
        200:
            description: Sucesso ao buscar os setores.
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            message:
                                type: string
                                example: "Botão Clicado"
    """
    setor_param = request.args.get('setor_param')
    grupo_condicional = request.args.get('grupo_condicional')
    grupo_default = request.args.get('grupo_default')
    filial_condicional = request.args.get('filial_condicional')
    setor_filial = request.args.get('setor_filial')
    setor_grupo = request.args.get('setor_grupo')

    return FilialService.buscar_setores(setor_param, grupo_condicional, grupo_default, filial_condicional, setor_filial, setor_grupo)
