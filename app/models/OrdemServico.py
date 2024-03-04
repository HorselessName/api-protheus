from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from db_context import db_sql
from typing import List
from models import Executor, Equipamento


@dataclass
class OrdemServico(db_sql.Model):
    __tablename__ = 'STJ010'

    # Mapeamento conforme os campos fornecidos na query SQL
    ordem_id: Mapped[str] = mapped_column('TJ_ORDEM', db_sql.String, primary_key=True)
    ordem_filial: Mapped[str] = mapped_column('TJ_FILIAL', db_sql.String, primary_key=True)

    ordem_equipamento: Mapped[str] = mapped_column('TJ_CODBEM', db_sql.String)

    ordem_cod_servico: Mapped[str] = mapped_column('TJ_SERVICO', db_sql.String)
    ordem_data_ultima_manutencao: Mapped[str] = mapped_column('TJ_DTULTMA', db_sql.String)

    # Valores Não Usados - Para Futuras Implementações de Agendamento.
    ordem_data_prevista: Mapped[str] = mapped_column('TJ_DTPPINI', db_sql.String)
    ordem_hora_prevista: Mapped[str] = mapped_column('TJ_HOPPINI', db_sql.String)

    # Valores Preenchidos quando o executor iniciar o atendimento.
    ordem_data_inicio_atendimento: Mapped[str] = mapped_column('TJ_DTPRINI', db_sql.String)
    ordem_hora_inicio_atendimento: Mapped[str] = mapped_column('TJ_HOPRINI', db_sql.String)

    # Valores Preenchidos quando o executor finalizar o atendimento.
    ordem_data_fim_atendimento: Mapped[str] = mapped_column('TJ_DTPRFIM', db_sql.String)
    ordem_hora_fim_atendimento: Mapped[str] = mapped_column('TJ_HOPRFIM', db_sql.String)

    # Valores de data e hora previstos e reais para início e fim de manutenção (ajustes conforme SQL).
    ordem_data_previsto_inicio_manutencao: Mapped[str] = mapped_column('TJ_DTMPINI', db_sql.String)
    ordem_hora_previsto_inicio_manutencao: Mapped[str] = mapped_column('TJ_HOMPINI', db_sql.String)
    ordem_data_previsto_fim_manutencao: Mapped[str] = mapped_column('TJ_DTMPFIM', db_sql.String)
    ordem_hora_previsto_fim_manutencao: Mapped[str] = mapped_column('TJ_HOMPFIM', db_sql.String)
    ordem_data_real_inicio_manutencao: Mapped[str] = mapped_column('TJ_DTMRINI', db_sql.String)
    ordem_hora_real_inicio_manutencao: Mapped[str] = mapped_column('TJ_HOMRINI', db_sql.String)
    ordem_data_real_fim_manutencao: Mapped[str] = mapped_column('TJ_DTMRFIM', db_sql.String)
    ordem_hora_real_fim_manutencao: Mapped[str] = mapped_column('TJ_HOMRFIM', db_sql.String)

    # Colunas para Filtro de O.S. abertas pelo APP.
    ordem_horaco2: Mapped[str] = mapped_column('TJ_HORACO2', db_sql.String)
    ordem_horaco1: Mapped[str] = mapped_column('TJ_HORACO1', db_sql.String)

    ordem_ultima_alteracao: Mapped[str] = mapped_column('TJ_USUARIO', db_sql.String)
    ordem_codsetor: Mapped[str] = mapped_column('TJ_CENTRAB', db_sql.String)
    ordem_observacao: Mapped[str] = mapped_column('TJ_OBSERVA', db_sql.String)
    ordem_codsolicitacao: Mapped[str] = mapped_column('TJ_SOLICI', db_sql.String)
    ordem_situacao: Mapped[str] = mapped_column('TJ_SITUACA', db_sql.String)

    @hybrid_property
    def ordem_prioridade(self):
        prioridade = self.solicitacao_vinculada.solicitacao_prioridade if self.solicitacao_vinculada else None
        if prioridade in ["", " ", None] or prioridade not in ["1", "2", "3"]:
            return "1"
        return prioridade

    def to_dict(self):
        return {
            "ordem_id": self.ordem_id,
            "ordem_filial": self.ordem_filial,
            "ordem_prioridade": self.ordem_prioridade if self.ordem_prioridade in ["1", "2", "3"] else "1",
            # Inclua outras propriedades conforme necessário
        }

    solicitacao_vinculada = relationship(
        "Solicitacao",
        primaryjoin="foreign(OrdemServico.ordem_codsolicitacao) == Solicitacao.solicitacao_id",
        lazy="joined"
    )

    ordem_excluida: Mapped[str] = mapped_column('D_E_L_E_T_', db_sql.String, nullable=True)

    # ----- Relacionamentos -----
    # Back Populates: Nome da Variável da outra Model, e vice - versa.
    ordem_insumos: Mapped[List["OrdemServicoInsumo"]] = relationship(back_populates="ordem_vinculada", lazy="joined")

    # Relacionamento com o Equipamento, pra trazer o nome (Usa a Filial da Ordem e o ID do Equipamento da Ordem)
    equipamento_da_ordem: Mapped["Equipamento"] = relationship(
        "Equipamento",
        primaryjoin="and_("
                    "foreign(OrdemServico.ordem_equipamento) == remote(Equipamento.equipamento_id), "
                    "foreign(OrdemServico.ordem_filial) == remote(Equipamento.equipamento_filial)"
                    ")",
        lazy="joined")

    @hybrid_property
    def ordem_equipamento_nome(self):
        return self.equipamento_da_ordem.equipamento_nome if self.equipamento_da_ordem else None


@dataclass
class OrdemServicoInsumo(db_sql.Model):
    __tablename__ = 'STL010'

    # Campos da tabela, definidos de acordo com as colunas no banco...
    # REF: https://docs.sqlalchemy.org/en/20/core/type_basics.html#sql-standard-and-multiple-vendor-uppercase-types

    insumo_ordem_id: Mapped[str] = mapped_column('TL_ORDEM', db_sql.VARCHAR, ForeignKey(OrdemServico.ordem_id))

    insumo_quantidade: Mapped[float] = mapped_column("TL_QUANTID", db_sql.Float)

    insumo_unidade: Mapped[str] = mapped_column("TL_UNIDADE", db_sql.VARCHAR)

    insumo_data_inicio: Mapped[str] = mapped_column("TL_DTINICI", db_sql.VARCHAR)
    insumo_hora_inicio: Mapped[str] = mapped_column("TL_HOINICI", db_sql.VARCHAR)
    insumo_data_fim: Mapped[str] = mapped_column("TL_DTFIM", db_sql.VARCHAR)
    insumo_hora_fim: Mapped[str] = mapped_column("TL_HOFIM", db_sql.VARCHAR)

    insumo_codigo: Mapped[str] = mapped_column('TL_CODIGO', db_sql.VARCHAR,
                                               ForeignKey(Executor.executor_matricula), primary_key=True)

    insumo_tipo: Mapped[str] = mapped_column('TL_TIPOREG', db_sql.VARCHAR)
    insumo_filial: Mapped[str] = mapped_column('TL_FILIAL', db_sql.VARCHAR)

    # ID do Insumo (Não pode ser 0)
    R_E_C_N_O_: Mapped[str] = mapped_column('R_E_C_N_O_', db_sql.BIGINT)

    @hybrid_property
    def executor_nome(self):
        if self.insumo_tipo == "M":
            return self.executor.executor_nome
        return None

    @hybrid_property
    def executor_codigo(self):
        if self.insumo_tipo == "M":
            return self.executor.executor_usuario

    ordem_vinculada: Mapped["OrdemServico"] = relationship(back_populates="ordem_insumos")
    executor: Mapped["Executor"] = relationship(
        "Executor",
        primaryjoin="Executor.executor_matricula==OrdemServicoInsumo.insumo_codigo",
        lazy="joined"
    )

    # GDM-111 - Ajuste de Propriedades para Insumos aparecerem no Protheus
    insumo_plano_manutencao: Mapped[str] = mapped_column("TL_PLANO", db_sql.VARCHAR, default='000000')
    insumo_sequencia_retorno: Mapped[str] = mapped_column("TL_SEQRELA", db_sql.VARCHAR, default='0')
    insumo_tarefa: Mapped[str] = mapped_column("TL_TAREFA", db_sql.VARCHAR, default='0')
    insumo_quantidade_recomendada: Mapped[float] = mapped_column("TL_QUANREC", db_sql.Float, default=0.0)
    insumo_usa_calendario: Mapped[str] = mapped_column("TL_USACALE", db_sql.VARCHAR , default='N')
    insumo_destino: Mapped[str] = mapped_column("TL_DESTINO", db_sql.VARCHAR, default='S')
    insumo_almoxarifado: Mapped[str] = mapped_column("TL_LOCAL", db_sql.VARCHAR, default='40')
    insumo_local_aplicacao: Mapped[str] = mapped_column("TL_LOCAPLI", db_sql.VARCHAR, default='')
    insumo_numero_sc: Mapped[str] = mapped_column("TL_NUMSC", db_sql.VARCHAR, default='')
    insumo_item_sc: Mapped[str] = mapped_column("TL_ITEMSC", db_sql.VARCHAR, default='')
    insumo_observacoes: Mapped[str] = mapped_column("TL_OBSERVA", db_sql.VARBINARY, nullable=True, default=None)
    insumo_nota_fiscal: Mapped[str] = mapped_column("TL_NOTFIS", db_sql.VARCHAR, default='')
    insumo_serie: Mapped[str] = mapped_column("TL_SERIE", db_sql.VARCHAR, default='')
    insumo_fornecedor: Mapped[str] = mapped_column("TL_FORNEC", db_sql.VARCHAR, default='')
    insumo_loja: Mapped[str] = mapped_column("TL_LOJA", db_sql.VARCHAR, default='')

    # Importante: A Sol. Armazém é gerada ao apontar insumo na O.S. na MATA105. Fica na tabela "SCP010"
    insumo_numero_sa: Mapped[str] = mapped_column("TL_NUMSA", db_sql.VARCHAR, default='')
    insumo_item_sa: Mapped[str] = mapped_column("TL_ITEMSA", db_sql.VARCHAR, default='')

    # A Sequência da Tarefa precisa ser `auto increment`, ou seja, pegar a última sequência e incrementar 1.
    insumo_sequencia_tarefa: Mapped[str] = mapped_column("TL_SEQTARE", db_sql.VARCHAR, default='')

    insumo_codigo_aen: Mapped[str] = mapped_column("TL_CODAEN", db_sql.VARCHAR, default='')
