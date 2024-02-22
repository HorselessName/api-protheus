from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Usuario


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
