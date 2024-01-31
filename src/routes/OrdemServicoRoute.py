from flask import Blueprint, request, jsonify
from services.OrdemServicoService import OrdemServicoService
from services.utils import validar_caracteres, validar_numeros
from flasgger import swag_from

"""
    Ordem de Serviço
    Blueprint para as rotas da Ordem de Serviço, para serem registradas
    no Flask pelo `Routing.py`. 
"""
blueprint_ordem_servico = Blueprint('ordens_servico', __name__)


@blueprint_ordem_servico.route('/ordens_servico/listar', methods=['GET'])
@swag_from('./api_docs/OrdemServicoPorSsDocs.yaml')
def get_ordens():
    validacao_codsolicitacao, message = validar_caracteres(request.args.get('ordem_codsolicitacao'))
    if validacao_codsolicitacao is True:
        ordem_cod_solicitacao = request.args.get('ordem_codsolicitacao')
        ordens_json, query_str = OrdemServicoService.get_ordens_por_solicitacao(ordem_cod_solicitacao)
        return jsonify(ordens_json), 200
    return jsonify(message), 400


@blueprint_ordem_servico.route('/ordens_servico/todas', methods=['GET'])
@swag_from('./api_docs/OrdensServicoDocs.yaml')
def get_todas_ordens():
    ordens_json, query_str = OrdemServicoService.get_todas_ordens_servico()
    return jsonify(ordens_de_servico=ordens_json, SQL=query_str), 200


@blueprint_ordem_servico.route('/ordens_servico/<ordem_id>', methods=['GET'])
@swag_from('./api_docs/OrdemServicoPorIdDocs.yaml')
def get_ordem(ordem_id):
    """
    Os argumentos da API, passados via URL, sempre devem ter o nome igual aos parâmetros da função e também
    dos campos da URL (ex: /ordens_servico/<ordem_id>), para que o Flask consiga fazer o mapeamento correto.
    """

    ordem_filial = request.args.get('ordem_filial')
    ordem_id_valida, mensagem = validar_numeros(ordem_id)
    ordem_filial_valida, mensagem = validar_numeros(request.args.get('ordem_filial'))

    if (not ordem_id_valida) or (not ordem_filial_valida):
        return jsonify({"erro": mensagem}), 400

    ordem_json, query_str = OrdemServicoService.get_ordem_servico(ordem_id, ordem_filial)

    print("-" * 30)
    print("Trazendo a O.S. por ID:", ordem_id, "e Filial:", ordem_filial)

    return jsonify(ordem_de_servico=ordem_json, SQL=query_str), 200
