from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Solicitacao


class SolicitacaoDescricaoSchema(SQLAlchemyAutoSchema):
    """
    This Schema represents a SolicitacaoDescricao.

    In order to map relationships in Marshmallow, we need to create a Schema for each related entity.
    This allows Marshmallow to understand how to serialize and deserialize the related data.

    In the case of Solicitacao, the `solicitacao_descricao` relationship is a one-to-one relationship.
    This means that each Solicitacao has a single SolicitacaoDescricao.

    To represent this relationship, we need to create a Schema for the `SolicitacaoDescricao` class.
    This Schema should define the fields that we want to serialize and deserialize from the SolicitacaoDescricao.

    In this example, the Schema only defines the `descricao_texto` field,
    which is the required field of the SolicitacaoDescricao.
    """
    descricao_texto = fields.String(required=True)

    class Meta:
        ordered = True


class SolicitacaoSchema(SQLAlchemyAutoSchema):
    solicitacao_prioridade = fields.Method("get_prioridade", dump_only=True)

    # Nested: https://marshmallow.readthedocs.io/en/stable/nesting.html
    # Use `SolicitacaoDescricaoSchema()` para instanciar o Schema e evitar o erro "Expected type 'SchemaABC'".
    solicitacao_descricao = fields.Pluck(SolicitacaoDescricaoSchema, "descricao_texto", dump_only=True)

    class Meta:
        model = Solicitacao
        load_instance = True
        exclude = ("D_E_L_E_T_", "solicitacao_descricao_id")

    @staticmethod
    def get_prioridade(obj):
        if obj.solicitacao_prioridade.strip():
            return obj.solicitacao_prioridade.strip()
        else:
            return "1"
