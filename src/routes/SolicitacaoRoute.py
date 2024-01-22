import re

from flask import Blueprint, jsonify, request
from services.ManutencaoService import ManutencaoService  # Ajuste conforme sua estrutura de imports
from services.SolicitacaoService import SolicitacaoService
from services.utils import validar_status, validar_data_between, validar_caracteres

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


# Rota pra trazer todas as solicitações de uma filial
# Lista todas as solicitações de uma filial com base no status fornecido.
@blueprint_manutencao.route('/manutencao/solicitacao/filial', methods=['GET'])
def get_solicitacoes_filial():
    """
    Lista todas as solicitações de uma filial com base no status fornecido.
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
      - name: status
        in: query
        type: string
        required: true
        description: Status da solicitação.
        default: 'A'
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
    status = request.args.get('status')

    if not validar_status(status):
        return jsonify({'erro': 'Formato de status inválido'}), 400

    print("Request Recebido para Ver se tem S.S. aberta para. Args: ", filial, status)

    if not filial or not status:
        return jsonify({'error': 'Os campos "filial" e "status" são obrigatórios.'}), 400

    try:
        # Precisa vir a quantia certa de argumentos, senão ele gera o erro "Not Enough Values to Unpack"
        sql, solicitacoes, mensagem_erro = ManutencaoService.buscar_solicitacoes_filial(
            filial=filial,
            status=status)

        if mensagem_erro:
            response_data = {'mensagem': mensagem_erro}
        else:
            response_data = {'sql': sql, 'solicitacoes': solicitacoes}

        print("Lista de Solicitacoes: ", response_data)

        return jsonify(response_data)

    except Exception as e:
        print(f"Erro ao processar as solicitações da Filial: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500


@blueprint_manutencao.route('/manutencao/solicitacao/listar', methods=['GET'])
def get_solicitacoes():
    """
    Lista todas as solicitações, usando os filtros informados.
    ---
    tags:
      - Solicitacoes
    parameters:
      - name: solicitacao_filial
        in: query
        type: string
        required: false
        description: Filial em que a S.S. está aberta.
        default: '*'
      - name: solicitacao_status
        in: query
        type: string
        required: false
        description: Status da Solicitação de Serviço (A,C,D,E).
        default: '*'
      - name: solicitacao_tipo
        in: query
        type: string
        required: false
        description: Tipo da Solicitação de Serviço (Correcao Eletrica, Mecanica, etc).
        default: '*'
      - name: solicitacao_equipamento
        in: query
        type: string
        required: false
        description: Equipamento da Solicitação de Serviço.
        default: '*'
      - name: data_between
        in: query
        type: string
        required: false
        description: Período de abertura das Solicitações (Ex. 20240131,20240230 ).
        default: '*'
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
            solicitacao_origin:
              type: string
              description: Origem da solicitação
            solicitacao_descricao:
              type: string
              description: Descrição da solicitação
            solicitacao_tipo:
              type: string
              description: Tipo da solicitação
            solicitacao_databer:
              type: string
              description: Data de abertura da solicitação
            solicitacao_datafec:
              type: string
              description: Data de fechamento da solicitação
            solicitacao_horaber:
              type: string
              description: Hora de abertura da solicitação
            solicitacao_horafec:
              type: string
              description: Hora de fechamento da solicitação
            solicitacao_tempo:
              type: string
              description: Tempo da solicitação
      400:
        description: Requisição inválida (parâmetros faltando)
        schema:
          id: Error
          properties:
            error:
              type: string
              description: Mensagem de erro
    """

    print(f"\n{'#' * 50} Tratamento de Dados da Lista de Solicitações {'#' * 50}")

    argumentos_esperados = {
        'solicitacao_filial': '*',
        'solicitacao_status': '*',
        'solicitacao_tipo': '*',
        'solicitacao_equipamento': '*',
        'data_between': '*'
    }

    print("# 1 - Argumentos Esperados: ", argumentos_esperados)

    argumentos_recebidos = request.args

    print("# 2 - Argumentos Recebidos: ", argumentos_recebidos)

    argumentos_validos = {}

    # Iterando sobre argumentos esperados e atualizando com valores recebidos, se aplicável
    for chave, valor_padrao in argumentos_esperados.items():
        valor_recebido = argumentos_recebidos.get(chave)
        if valor_recebido is not None and valor_recebido != '*':
            argumentos_validos[chave] = valor_recebido
        else:
            argumentos_validos[chave] = valor_padrao

    print("# 3 - Argumentos Válidos: ", argumentos_validos)

    # Validando os argumentos recebidos.

    print("# 4 - Validando os argumentos recebidos. ")

    for chave, valor in argumentos_validos.items():
        # Using RegEx because `if valor != '*'` doesn't work for some reason. DO NOT USE `!=` for this!
        if not re.match(r"^[*]?$", valor):
            valor_validado, msg_dados_invalidos = validar_caracteres(valor, chave)
            if not valor_validado:
                print("# 5 - Erro ao validar os argumentos recebidos: ", chave, valor)
                print(f"{'#' * 50} Fim do Tratamento de Dados da Lista de Solicitações (Com Erro) {'#' * 50}\n")
                return jsonify({'error': msg_dados_invalidos}), 400
            if chave == 'data_between':
                valor_validado, msg_validador_data = validar_data_between(valor)
                if not valor_validado:
                    print("# 5 - Erro ao validar a data: ", chave, valor)
                    print(f"{'#' * 50} Fim do Tratamento de Dados da Lista de Solicitações (Com Erro) {'#' * 50}\n")
                    return jsonify({'error': msg_validador_data}), 400
            if chave == 'solicitacao_status':
                if not validar_status(valor):
                    return jsonify({'erro': 'Formato de status inválido. Valores e Formato: A,D,E,C.'}), 400

    print("# 5 - Enviando os Argumentos Validados p/ a Service de Solicitacoes: ", argumentos_validos)

    try:
        print("\n-- Route: Chamando a Service de Solicitacoes")
        SolicitacaoService.get_all_solicitacoes(**argumentos_validos)

        return ""
    except Exception as e:
        print(f"Erro ao processar as solicitações na Get Solicitacoes: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

    pass
