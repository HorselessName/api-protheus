from flask import jsonify, request
from services import EquipamentoService


def equipamentos_routes(app):
    @app.route('/equipamentos', methods=['GET'])
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
        filial = request.args.get('filial')
        setor = request.args.get('setor')

        if not filial or not setor:
            return jsonify(error="Os campos 'filial' e 'setor' são obrigatórios."), 400

        equipamentos, error = EquipamentoService.fetch_equipamentos(filial_id=filial, setor_id=setor)
        if error:
            return jsonify(error="Erro ao buscar equipamentos no banco de dados.", details=error), 500
        return {'equipamentos': equipamentos}
