from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Setor


class SetorSchema(SQLAlchemyAutoSchema):
    setor_grupo = fields.Str()  # Campo adicional que não existe na model Setor e nem na tabela.

    class Meta:
        model = Setor
        load_instance = True
        exclude = ("D_E_L_E_T_",)
