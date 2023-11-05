from flask import Blueprint, request, jsonify
from services.FilialService import FilialService

blueprint_filial = Blueprint('filial', __name__)


@blueprint_filial.route('/filial/setores', methods=['GET'])
def get_setores():
    """
    Retorna a lista dos setores para os grupos e filiais informados.
    ---
    tags:
      - Setores
    parameters:
      - name: setor_codigo_opcional
        in: query
        type: string
        required: false
        description: Código opcional do setor para aplicar a lógica de teste condicional.
      - name: grupo_condicional
        in: query
        type: string
        required: false
        description: Modificador de grupo, aplicado se usado junto com o código do setor.
      - name: filial_condicional
        in: query
        type: string
        required: false
        description: Modificador de Filial, aplicado se usado junto com o código do setor.
      - name: grupo_padrao
        in: query
        type: string
        required: true
        description: Nome do grupo padrão a ser aplicado nos setores.
      - name: filial_padrao
        in: query
        type: string
        required: true
        description: Nome da filial padrão a ser aplicado nos setores.
    responses:
      200:
        description: Retorna a Lista de Setores.
      400:
        description: Erro de validação dos parâmetros de entrada. Verifique os valores informados.
        examples:
          application/json: { "Erro": "Descrição detalhada do erro de validação" }
      500:
        description: Erro ao executar a consulta na base de dados. Pode ser devido a problemas de conexão ou erros internos do servidor.
        examples:
          application/json: { "Erro": "Erro interno do servidor. Tente novamente mais tarde ou contate o suporte técnico." }
    """
    try:
        # Parse dos parâmetros da query string
        parametros = {
            "setor_codigo_opcional": request.args.get('setor_codigo_opcional'),
            "grupo_condicional": request.args.get('grupo_condicional'),
            "filial_condicional": request.args.get('filial_condicional'),
            "grupo_padrao": request.args.get('grupo_padrao'),
            "filial_padrao": request.args.get('filial_padrao')
        }

        # Faz a validação dos parâmetros obrigatórios aqui
        if not parametros["grupo_padrao"] or not parametros["filial_padrao"]:
            return jsonify(message="O 'grupo_padrao' e 'Filial_padrao' são parâmetros obrigatórios."), 400

        # Executa a função de serviço e retorna a resposta
        resultado = FilialService.executar_e_serializar_query(**parametros)
        return jsonify(message="Consulta executada com sucesso!", resultado=resultado)

    except ValueError as e:
        # Isso captura as exceções de validação
        return jsonify(message=str(e)), 400
    except Exception as e:
        # Qualquer outro erro que possa ocorrer
        return jsonify(message="Erro ao executar a consulta", erro=str(e)), 500


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
