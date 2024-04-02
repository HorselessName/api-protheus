from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Produto, ProdutoSaldo


class ProdutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Produto
        load_instance = True
        exclude = ['D_E_L_E_T_']


class ProdutoSaldoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProdutoSaldo
        load_instance = True
