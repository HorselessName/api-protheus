from flask import Blueprint, jsonify
from flasgger import swag_from

from services.UsuarioService import UsuarioService

blueprint_usuarios = Blueprint('usuarios', __name__)


@blueprint_usuarios.route('/usuarios/informacoes', methods=['GET'])
@swag_from('./api_docs/InformacoesDoUsuarioDocs.yaml')
def informacoes_do_usuario():
    try:
        usuario = UsuarioService.informacoes_do_usuario("raul.chiarella")
        return jsonify(usuario), 200
    except Exception as erro:
        return jsonify({"erro": f"Erro ao processar a requisição: {erro}"}), 500
