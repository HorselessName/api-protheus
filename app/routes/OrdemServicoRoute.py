from flask import Blueprint, request, jsonify
from services.OrdemServicoService import OrdemServicoService
from services.Utils import validar_caracteres, validar_numeros, validar_estrutura_json, remover_espacos_do_json
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
        ordem_filial = request.args.get('ordem_filial')
        ordens_json, query_str = OrdemServicoService.get_ordens_por_solicitacao(ordem_cod_solicitacao, ordem_filial)
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


@blueprint_ordem_servico.route('/ordens_servico/<ordem_id>/insumos', methods=['GET'])
@swag_from('./api_docs/InsumosPorOrdemDocs.yaml')
def get_ordem_insumos(ordem_id):
    """
    Os argumentos da API, passados via URL, sempre devem ter o nome igual aos parâmetros da função e também
    dos campos da URL (ex: /ordens_servico/<ordem_id>), para que o Flask consiga fazer o mapeamento correto.
    """

    ordem_filial = request.args.get('ordem_filial')
    ordem_id_valida, mensagem = validar_numeros(ordem_id)
    ordem_filial_valida, mensagem = validar_numeros(request.args.get('ordem_filial'))

    if (not ordem_id_valida) or (not ordem_filial_valida):
        return jsonify({"erro": mensagem}), 400

    insumos_json, query_str = OrdemServicoService.get_insumos_por_ordem(ordem_id, ordem_filial)

    print("-" * 30)
    print("Trazendo os insumos da O.S. por ID:", ordem_id, "e Filial:", ordem_filial)

    return jsonify(insumos=insumos_json, SQL=query_str), 200


@blueprint_ordem_servico.route('/ordens_servico/<ordem_id>/insumos/incluir', methods=['POST'])
@swag_from('./api_docs/IncluirInsumoDocs.yaml')
def incluir_ordem_insumo(ordem_id):
    insumo_json_bruto = request.get_json()
    insumo_json = remover_espacos_do_json(insumo_json_bruto)

    if not validar_estrutura_json(insumo_json):
        return jsonify({"erro": "Estrutura JSON inválida"}), 400

    campos_esperados_json = {"insumo_codigo", "insumo_quantidade", "insumo_tipo",
                             "insumo_unidade", "insumo_local", "ordem_filial"}

    # Verifica se a estrutura do JSON contém todos os campos esperados e não contém campos extras
    if set(insumo_json.keys()) != campos_esperados_json:
        campos_faltando = campos_esperados_json - set(insumo_json.keys())
        campos_extras = set(insumo_json.keys()) - campos_esperados_json
        mensagem_erro = "JSON deve conter exatamente os campos: " + ", ".join(sorted(campos_esperados_json)) + "."
        if campos_faltando:
            mensagem_erro += " Faltando: " + ", ".join(sorted(campos_faltando)) + "."
        if campos_extras:
            mensagem_erro += " Campos extras não permitidos: " + ", ".join(sorted(campos_extras)) + "."
        return jsonify({"erro": mensagem_erro}), 400

    sucesso, mensagem_insumo = OrdemServicoService.incluir_insumo_na_ordem(
        ordem_id,
        insumo_json["ordem_filial"],
        insumo_json
    )

    if sucesso:
        resposta = {
            "mensagem": mensagem_insumo,
            "ordem_id": ordem_id,
            "detalhes_insumo": insumo_json
        }
        return jsonify(resposta), 200
    else:
        return jsonify({"erro": mensagem_insumo}), 500


@blueprint_ordem_servico.route('/ordens_servico/<ordem_id>/comentarios/listar', methods=['GET'])
@swag_from('./api_docs/ComentariosPorOrdemDocs.yaml')
def get_ordem_comentarios(ordem_id):
    # Argumentos esperados
    argumentos_esperados = {'ordem_filial'}
    argumentos_recebidos = set(request.args.keys())

    # Verifica se há argumentos desconhecidos
    argumentos_desconhecidos = argumentos_recebidos - argumentos_esperados
    if argumentos_desconhecidos:
        return jsonify({"erro": f"Argumentos desconhecidos recebidos: {', '.join(argumentos_desconhecidos)}"}), 400

    # Continua a execução normal se todos os argumentos forem conhecidos
    ordem_filial = request.args.get('ordem_filial')

    print("Ordem Filial:", ordem_filial)
    print("Ordem ID:", ordem_id)

    ordem_id_valida, mensagem = validar_numeros(ordem_id)
    ordem_filial_valida, mensagem = validar_numeros(ordem_filial)

    if not ordem_id_valida or not ordem_filial_valida:
        return jsonify({"erro": mensagem}), 400

    comentarios_json, query_str = OrdemServicoService.get_comentarios_da_os(ordem_id, ordem_filial)

    print("-" * 30)
    print("Trazendo os comentários da O.S. por ID:", ordem_id, "e Filial:", ordem_filial)

    return jsonify(comentarios=comentarios_json, SQL=query_str), 200


@swag_from('./api_docs/IncluirComentarioDocs.yaml')
@blueprint_ordem_servico.route('/ordens_servico/<ordem_id>/comentarios/incluir', methods=['POST'])
def incluir_comentarios_na_os(ordem_id):
    ordem_filial = request.args.get('filial')
    texto_comentario = request.json.get('texto_comentario')

    ordem_id_valida, mensagem = validar_numeros(ordem_id)
    ordem_filial_valida, mensagem_filial = validar_numeros(ordem_filial)

    if not (ordem_id_valida and ordem_filial_valida):
        mensagem_erro = mensagem if not ordem_id_valida else mensagem_filial
        return jsonify({"erro": mensagem_erro}), 400

    # Chama a service para adicionar o comentário
    resultado = OrdemServicoService.adicionar_comentario_na_os(ordem_id, ordem_filial, texto_comentario)

    if isinstance(resultado, str) and resultado.startswith("Erro"):
        return jsonify({"erro": resultado}), 500
    else:
        return jsonify(resultado), 200
