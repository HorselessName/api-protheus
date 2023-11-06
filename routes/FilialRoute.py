from flask import Blueprint, request, jsonify
from services.FilialService import FilialService, SetorLogic

blueprint_filial = Blueprint('filial', __name__)


@blueprint_filial.route('/filial/testes', methods=['GET'])
def fazer_testes():
    """
    Rota para Testes
    ---
    tags:
      - Testes
    responses:
      200:
        description: Teste Ok.
    """
    # Retorna a consulta SQL como parte da resposta da API.
    return jsonify(message="Teste Ok!")


@blueprint_filial.route('/filial/setores', methods=['GET'])
def get_setores():
    """
    Retorna a lista dos setores para os grupos e filiais informados, com a possibilidade de aplicar filtros condicionais e padrões.
    ---
    tags:
      - Setores
    parameters:
      - name: setor_no_request
        in: query
        type: string
        required: false
        description: Nome do setor a ser usado para o join interno na consulta.
      - name: filial_no_request
        in: query
        type: string
        required: false
        description: Nome da filial condicional para aplicar o filtro na consulta.
      - name: grupo_no_request
        in: query
        type: string
        required: false
        description: Nome do grupo condicional para aplicar o filtro na consulta.
      - name: grupo_padrao
        in: query
        type: string
        required: false
        description: Nome do grupo padrão a ser aplicado na consulta, se desejado.
      - name: setor_filial_filtro
        in: query
        type: string
        required: true
        description: Filtro obrigatório para ser aplicado especificamente à filial do setor.
      - name: setor_grupo_filtro
        in: query
        type: string
        required: true
        description: Filtro obrigatório para ser aplicado especificamente ao grupo do setor.
    responses:
      200:
        description: Retorna a Lista de Setores com a consulta SQL e os dados serializados em JSON.
      400:
        description: Erro de validação dos parâmetros de entrada. Verifique os valores informados.
        examples:
          application/json: { "Erro": "Descrição detalhada do erro de validação" }
      500:
        description: Erro ao executar a consulta na base de dados.
        examples:
          application/json: { "Erro": "Erro. Tente novamente mais tarde ou contate o suporte técnico." }
    """
    try:
        print(request.args)
        # Parse dos parâmetros da query string
        setor_no_request = request.args.get('setor_no_request')
        filial_no_request = request.args.get('filial_no_request')
        grupo_no_request = request.args.get('grupo_no_request')
        grupo_padrao = request.args.get('grupo_padrao')

        # Captura e validação dos parâmetros obrigatórios setor_filial_filtro e setor_grupo_filtro
        setor_filial_filtro = request.args.get('setor_filial_filtro')
        setor_grupo_filtro = request.args.get('setor_grupo_filtro')

        if not setor_filial_filtro or not setor_grupo_filtro:
            return jsonify(
                {"Erro": "Os parâmetros 'setor_filial_filtro' e 'setor_grupo_filtro' são obrigatórios."}), 400

        # Executa a função de serviço e retorna a resposta.
        resultado = SetorLogic.listar_setores(
            setor_recebido=setor_no_request,
            filial_condicional=filial_no_request,
            grupo_condicional=grupo_no_request,
            grupo_padrao=grupo_padrao,
            setor_filial_filtro=setor_filial_filtro,
            setor_grupo_filtro=setor_grupo_filtro
        )
        return jsonify({"message": "Consulta executada com sucesso!", "resultado": resultado}), 200

    except ValueError as e:
        # Isso captura as exceções de validação
        return jsonify({"Erro": str(e)}), 400
    except Exception as e:
        # Qualquer outro erro que possa ocorrer
        return jsonify({"Erro": "Erro ao executar a consulta", "erro": str(e)}), 500


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
