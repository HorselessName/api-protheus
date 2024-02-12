from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Produto


class ProdutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Produto
        load_instance = True
        exclude = ['D_E_L_E_T_']
