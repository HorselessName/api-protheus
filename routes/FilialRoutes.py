from flask import jsonify, request
from services import FilialService


def filial_routes(app):
    @app.route('/filial/listar', methods=['GET'])
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
