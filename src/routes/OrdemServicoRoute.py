from flask import Blueprint, request, jsonify
from services.OrdemServicoService import OrdemServicoService
from services.utils import validar_caracteres
from flasgger import swag_from

"""
    Ordem de Serviço
    Blueprint para as rotas da Ordem de Serviço, para serem registradas
    no Flask pelo `Routing.py`. 
"""
blueprint_ordem_servico = Blueprint('ordens_servico', __name__)


@blueprint_ordem_servico.route('/ordens_servico/listar', methods=['GET'])
@swag_from('./api_docs/OrdemServicoDocs.yaml')
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
