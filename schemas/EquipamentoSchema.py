from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Equipamento


class EquipamentoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Equipamento
        load_instance = True
        exclude = ("D_E_L_E_T_", "T9_STATUS")
