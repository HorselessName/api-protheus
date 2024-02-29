from flask import Blueprint, jsonify, request
from flasgger import swag_from

from services.UsuarioService import UsuarioService

blueprint_usuarios = Blueprint('usuarios', __name__)


@blueprint_usuarios.route('/usuarios/informacoes/<usuario_login>', methods=['GET'])
@swag_from('./api_docs/InformacoesDoUsuarioDocs.yaml')
def informacoes_do_usuario(usuario_login):
    try:
        print(f"Verificando Permissões do Usuário {usuario_login}")
        usuario = UsuarioService.informacoes_do_usuario(usuario_login)

        if usuario:
            return jsonify(usuario), 200

        raise Exception  # Exception sem detalhes p/ não expor informações sensíveis.
    except Exception as erro:
        return jsonify({"erro": f"Erro ao processar a requisição: {erro}"}), 500
