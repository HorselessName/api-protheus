from models import Usuario
from schemas import UsuarioSchema


class UsuarioService:
    @staticmethod
    def informacoes_do_usuario(usuario: str) -> Usuario:
        usuario = Usuario.query.filter_by(usuario_login=usuario).first()
        usuario_schema = UsuarioSchema()
        usuario_json = usuario_schema.dump(usuario)  # O Dump permite que o objeto seja serializado para JSON
        return usuario_json
