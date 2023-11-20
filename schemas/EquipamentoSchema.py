from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Equipamento
from marshmallow import fields


class EquipamentoSchema(SQLAlchemyAutoSchema):
    # Definir o Campo Adicional, gerado com o Outer Join da Query de Equipamentos.
    possui_ss_aberta = fields.Str()

    class Meta:
        model = Equipamento
        load_instance = True
        exclude = ("D_E_L_E_T_", "T9_STATUS")
