from services.Utils import horario_atual
from flask import Blueprint, jsonify
from flasgger import swag_from

blueprint_utils = Blueprint('utils', __name__)


@blueprint_utils.route('/utils/horario', methods=['GET'])
@swag_from('./api_docs/UtilsHorarioDocs.yaml')
def get_horario_atual():
    horario = horario_atual()
    return jsonify({'horario': horario})
