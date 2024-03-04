from flask import Blueprint, jsonify, request
from flasgger import swag_from
from services import Utils
from services.ProdutoService import ProdutoService

blueprint_produtos = Blueprint('produtos', __name__)


@blueprint_produtos.route('/produtos/listar', methods=['GET'])
@swag_from('./api_docs/GetProdutosDocs.yaml')
def get_produtos():
    try:
        tipos_de_produto = Utils.valores_por_virgula(request.args.get('tipos_de_produto'))

        # Verificar se é um único tipo de produto sem vírgula
        if tipos_de_produto is None:
            tipos_de_produto = [request.args.get('tipos_de_produto')]
            if not Utils.dois_caracteres_uppercase(tipos_de_produto):
                return jsonify({"erro": "Tipo de produto inválido"}), 400
        elif not Utils.dois_caracteres_uppercase(tipos_de_produto):
            return jsonify({"erro": "Tipos de produto inválidos"}), 400

        # Obter parâmetros de paginação da query string
        pagina = int(request.args.get('pagina', 1))
        itens_por_pagina = int(request.args.get('itens_por_pagina', 5000))

        # Buscar os produtos com paginação
        produtos = ProdutoService.trazer_produtos(tipos_de_produto, pagina, itens_por_pagina)

        print("#" * 50)
        print(f"# Produtos obtidos com sucesso. Lista de Produtos: {produtos}")

        # Retornar os produtos serializados como JSON
        return jsonify({"produtos": produtos}), 200

    except Exception as erro:
        return jsonify({"erro": f"Erro ao processar a requisição: {erro}"}), 500
