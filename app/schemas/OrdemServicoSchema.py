from models import OrdemServico, OrdemServicoInsumo
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import OrdemServicoInsumo


class OrdemServicoInsumoSchema(SQLAlchemyAutoSchema):
    """
    Schema do Marshmallow para Desserialização dos Insumos da Ordem de Serviço.
    """

    detalhes_insumo = fields.Method("get_detalhes_insumo")

    @staticmethod
    def get_detalhes_insumo(obj):
        """
        Retorna detalhes do insumo com base no seu tipo.
        """
        detalhes = {
            "insumo_tipo": obj.insumo_tipo,
            "insumo_codigo": obj.insumo_codigo,
            "insumo_quantidade": obj.insumo_quantidade,
            "insumo_unidade": obj.insumo_unidade,
            "insumo_data_inicio": obj.insumo_data_inicio,
            "insumo_hora_inicio": obj.insumo_hora_inicio
        }
        if obj.insumo_tipo == "M":
            detalhes["executor_nome"] = obj.executor.executor_nome if obj.executor else None
        return detalhes

    class Meta:
        model = OrdemServicoInsumo
        load_instance = True
        include_fk = True
        fields = ("detalhes_insumo",)
        ordered = True


class OrdemServicoSchema(SQLAlchemyAutoSchema):
    """
    Schema do Marshmallow para Desserialização, com relacionamento One to Many com os Insumos da O.S.
    """

    ordem_insumos = fields.Nested(OrdemServicoInsumoSchema(many=True, ))
    ordem_prioridade = fields.Method("get_ordem_prioridade")
    ordem_equipamento_nome = fields.Method("get_ordem_equipamento_nome")
    ordem_observacao = fields.Method("get_ordem_observacao")

    @staticmethod
    def get_ordem_observacao(obj):
        """
        Método para ver a observação da Ordem de Serviço.
        """
        return obj.ordem_observacao if obj.ordem_observacao else None

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
        exclude = ("ordem_excluida", "ordem_observacao_binario",)
        ordered = True


class OrdemServicoComentarioSchema(SQLAlchemyAutoSchema):
    """
    Schema do Marshmallow para Desserialização dos Comentários da Ordem de Serviço.
    """

    class Meta:
        model = OrdemServico
        load_instance = True
        ordered = True
