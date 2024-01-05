from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Filial


class FilialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Filial
        load_instance = True
        exclude = ("D_E_L_E_T_",)
