from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import Solicitacao


class SolicitacaoSchema(SQLAlchemyAutoSchema):
    solicitacao_prioridade = fields.Method("get_prioridade", dump_only=True)

    class Meta:
        model = Solicitacao
        load_instance = True
        exclude = ("D_E_L_E_T_",)

    @staticmethod
    def get_prioridade(obj):
        # Verificar se o campo está vazio ou contém apenas espaços
        if obj.solicitacao_prioridade.strip():
            # Retornar o valor atual, removendo espaços desnecessários
            return obj.solicitacao_prioridade.strip()
        else:
            # Caso contrário, aplicar o valor padrão "1"
            return "1"
