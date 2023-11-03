from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Solicitacao


class SolicitacaoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Solicitacao
        load_instance = True
        exclude = ("D_E_L_E_T_",)
