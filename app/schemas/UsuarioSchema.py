from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import Usuario, UsuarioFilial
from marshmallow import fields


class UsuarioFilialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioFilial
        load_instance = True

        # Certifique-se de que exclude é uma lista de nomes de campos a serem excluídos
        exclude = ('usuario_acesso',)  # Nota: isso é uma tupla, mas você também pode usar uma lista ['usuario_acesso']

    # Campos personalizados mantidos
    usuario_filial = auto_field()
    usuario_filial_grupo = auto_field()


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_fk = True

    # When a class needs to be instanced, use `Class()` instead of `Class`
    filiais = fields.Nested(UsuarioFilialSchema(), many=True)
