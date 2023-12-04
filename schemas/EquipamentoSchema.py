from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Equipamento
from marshmallow import fields


class EquipamentoSchema(SQLAlchemyAutoSchema):
    # Definir o Campo Adicional, gerado com o Outer Join da Query de Equipamentos.
    possui_ss_aberta = fields.Str()
    prioridade_ss = fields.Str()

    class Meta:
        model = Equipamento
        load_instance = True
        exclude = ("D_E_L_E_T_", "T9_STATUS")

    @staticmethod
    def get_prioridade_ss(obj):
        # Verificar se possui_ss_aberta é 'true'
        if obj.possui_ss_aberta == 'true':
            # Se houver uma S.S. aberta, retornar a prioridade dela
            return obj.prioridade_ss
        else:
            # Se não houver S.S. aberta, retornar '0'
            return '0'

