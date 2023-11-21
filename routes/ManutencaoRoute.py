import json

from flask import Blueprint, jsonify, request
from services.ManutencaoService import ManutencaoService  # Ajuste conforme sua estrutura de imports

blueprint_manutencao = Blueprint('manutencao', __name__)


@blueprint_manutencao.route('/manutencao/solicitacao', methods=['GET'])
def get_solicitacao():
    """
    Lista as solicitações abertas para o Equipamento e Filial informada.
    ---
    tags:
      - Solicitacoes
    parameters:
      - name: filial
        in: query
        type: string
        required: true
        description: Filial em que a S.S. está aberta.
        default: '020101'
      - name: equipamento
        in: query
        type: string
        required: true
        description: Identificação do bem qual deseja ver as solicitacoes.
        default: 'DOC'
    responses:
      200:
        description: Lista de solicitações
        schema:
          id: Solicitacoes
          properties:
            solicitacao_id:
              type: integer
              description: ID da solicitação
            solicitacao_filial:
                type: string
                description: Filial da solicitação
            solicitacao_equipamento:
                type: string
                description: Equipamento da solicitação
            solicitacao_prioridade:
                type: string
                description: Prioridade da solicitação
            solicitacao_status:
                type: string
                description: Status da solicitação
      400:
        description: Requisição inválida (parâmetros faltando)
        schema:
          id: Error
          properties:
            error:
              type: string
              description: Mensagem de erro
    """

    filial = request.args.get('filial')
    equipamento = request.args.get('equipamento')

    print("Request Recebido para Ver se tem S.S. aberta para. Args: ", filial, equipamento)

    if not filial or not equipamento:
        return jsonify({'error': 'Os campos "filial" e "equipamento" são obrigatórios.'}), 400

    try:
        sql, solicitacoes, possui_ss_aberta, mensagem_erro = ManutencaoService.buscar_solicitacoes_abertas(
            filial=filial,
            equipamento=equipamento)

        if mensagem_erro:
            response_data = {'possui_ss_aberta': False, 'mensagem': mensagem_erro}
        else:
            response_data = {'possui_ss_aberta': possui_ss_aberta, 'sql': sql}
            if possui_ss_aberta:
                response_data['solicitacoes'] = solicitacoes
            else:
                response_data['mensagem'] = 'O equipamento não possui nenhuma S.S. aberta'

        print("Lista de Solicitacoes: ", response_data)

        return jsonify(response_data)

    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
