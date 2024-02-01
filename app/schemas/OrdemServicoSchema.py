from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import OrdemServico, OrdemServicoInsumo


class OrdemServicoInsumoSchema(SQLAlchemyAutoSchema):
    """
    Schema do Marshmallow para Desserialização, com relacionamento Many to One com a O.S..
    Representa os Insumos da Ordem de Serviço.
    """

    executor_nome = fields.Method("get_executor_nome")

    @staticmethod
    def get_executor_nome(obj):
        """
        Método para definir o Executor da O.S. de acordo com o tipo do Insumo.
        Depende das Models também possuírem o Executor, caso contrário, retornará None.
        """
        if obj.insumo_tipo == "M":
            return obj.executor.executor_nome if obj.executor else None
        return None

    class Meta:
        model = OrdemServicoInsumo
        load_instance = True
        include_fk = True
        exclude = ("insumo_ordem_id", )
        ordered = True


class OrdemServicoSchema(SQLAlchemyAutoSchema):
    """
    Schema do Marshmallow para Desserialização, com relacionamento One to Many com os Insumos da O.S.
    """

    ordem_insumos = fields.Nested(OrdemServicoInsumoSchema(many=True,))
    ordem_prioridade = fields.Method("get_ordem_prioridade")
    ordem_equipamento_nome = fields.Method("get_ordem_equipamento_nome")

    @staticmethod
    def get_ordem_prioridade(obj):
        """
        Método para ver a prioridade definida pela @Hybrid Property da Model da OrdemServico.
        """
        return obj.ordem_prioridade if obj.ordem_prioridade else None

    @staticmethod
    def get_ordem_equipamento_nome(obj):
        """
        Método para ver o nome do Equipamento da Ordem de Serviço.
        """
        return obj.ordem_equipamento_nome if obj.ordem_equipamento_nome else None

    class Meta:
        model = OrdemServico
        load_instance = True
        include_fk = True
        exclude = ("ordem_excluida",)
        ordered = True
