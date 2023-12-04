from flask import Blueprint, jsonify, request
from services.EquipamentoService import EquipamentoService  # Apenas um exemplo, ajuste conforme sua estrutura

# Blueprint Flask: Rota de equipamentos.
blueprint_equipamentos = Blueprint('equipamentos', __name__)


@blueprint_equipamentos.route('/equipamentos', methods=['GET'])
def get_equipamentos():
    """
    Lista todos os equipamentos cadastrados com base na filial e no setor fornecidos.
    ---
    tags:
      - Equipamentos
    parameters:
      - name: filial
        in: query
        type: string
        required: true
        description: Filial do equipamento
      - name: setor
        in: query
        type: string
        required: true
        description: Setor do equipamento
    responses:
      200:
        description: Lista de equipamentos
        schema:
          id: Equipamentos
          properties:
            equipamento_id:
              type: integer
              description: ID do equipamento
            equipamento_filial:
              type: string
              description: Filial do equipamento
            equipamento_setor:
              type: string
              description: Setor do equipamento
            equipamento_nome:
              type: string
              description: Nome do equipamento
            equipamento_ccusto:
              type: string
              description: Centro de custo do equipamento
      400:
        description: Requisição inválida (parâmetros faltando)
        schema:
          id: Error
          properties:
            error:
              type: string
              description: Mensagem de erro
    """
    filial = request.args.get('filial', '').strip()
    setor = request.args.get('setor', '').strip()

    print(f"\n----> Requests Recebidos: {filial}, {setor} <----\n")

    if not filial or not setor:
        return jsonify(error="Os campos 'filial' e 'setor' são obrigatórios."), 400

    lista_equipamentos, error = EquipamentoService.fetch_equipamentos(filial_id=filial, setor_id=setor)
    print(f"\n----> __ ROTA EQUIPAMENTOS __: Equipamentos Retornados da Service <----\n"
          f"{lista_equipamentos}\n{'-' * 100}\n")
    if error:
        return jsonify(error="Erro ao buscar equipamentos no banco de dados.", details=error), 500
    return jsonify(resultado=lista_equipamentos)


@blueprint_equipamentos.route('/equipamentos_ss', methods=['GET'])
def get_equipamentos_ss():
    """
    Lista todos os equipamentos cadastrados com base na filial e no setor fornecidos,
    incluindo informação sobre se o equipamento possui solicitação de serviço (SS) aberta.
    ---
    tags:
      - Equipamentos
    parameters:
      - name: filial
        in: query
        type: string
        required: true
        description: Filial do equipamento
        default: '020101'
      - name: setor
        in: query
        type: string
        required: true
        description: Setor do equipamento
        default: 'GENERI'
    responses:
      200:
        description: Lista de equipamentos com status de SS
        schema:
          id: EquipamentosSS
          properties:
            equipamento_id:
              type: integer
              description: ID do equipamento
            equipamento_filial:
              type: string
              description: Filial do equipamento
            equipamento_setor:
              type: string
              description: Setor do equipamento
            equipamento_nome:
              type: string
              description: Nome do equipamento
            equipamento_ccusto:
              type: string
              description: Centro de custo do equipamento
            possui_ss_aberta:
              type: string
              description: Informa se o equipamento possui solicitação de serviço aberta ('true' ou 'false')
            prioridade_ss:
              type: string
              description: Prioridade da S.S. atual do equipamento.
      400:
        description: Requisição inválida (parâmetros faltando)
        schema:
          id: Error
          properties:
            error:
              type: string
              description: Mensagem de erro
    """
    filial = request.args.get('filial', '').strip()
    setor = request.args.get('setor', '').strip()

    print(f"\n----> Requests Recebidos para Equipamentos com Status de SS: {filial}, {setor} <----\n")

    if not filial or not setor:
        return jsonify(error="Os campos 'filial' e 'setor' são obrigatórios."), 400

    equipamentos_com_status, error = EquipamentoService.fetch_equipamentos_e_ss(filial_id=filial, setor_id=setor)
    print(f"\n----> __ ROTA EQUIPAMENTOS COM STATUS SS __: Equipamentos Retornados da Service <----\n"
          f"{equipamentos_com_status}\n{'-' * 100}\n")
    if error:
        return jsonify(error="Erro ao buscar equipamentos com status de SS no banco de dados.", details=error), 500

    return jsonify(resultado=equipamentos_com_status)

