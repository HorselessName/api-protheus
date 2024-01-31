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

    # Valores Não Usados, mas mapeados para possíveis funcionalidades de agendamento.
    ordem_data_prevista: Mapped[str] = mapped_column('TJ_DTPPINI', db_sql.String)
    ordem_hora_prevista: Mapped[str] = mapped_column('TJ_HOPPINI', db_sql.String)

    # Valores Preenchidos quando a O.S. é gerada.
    ordem_data_abertura: Mapped[str] = mapped_column('TJ_DTMPINI', db_sql.String)
    ordem_hora_abertura: Mapped[str] = mapped_column('TJ_HOMPINI', db_sql.String)

    # Valores Preenchidos quando o executor iniciar o atendimento.
    ordem_data_inicio_atendimento: Mapped[str] = mapped_column('TJ_DTMRINI', db_sql.String)
    ordem_hora_inicio_atendimento: Mapped[str] = mapped_column('TJ_HOMRINI', db_sql.String)

    # Valores Preenchidos quando o executor finalizar o atendimento.
    ordem_data_fim_atendimento: Mapped[str] = mapped_column('TJ_DTMRFIM', db_sql.String)
    ordem_hora_fim_atendimento: Mapped[str] = mapped_column('TJ_HOMRFIM', db_sql.String)

    ordem_ultima_alteracao: Mapped[str] = mapped_column('TJ_USUARIO', db_sql.String)
    ordem_codsetor: Mapped[str] = mapped_column('TJ_CENTRAB', db_sql.String)
    ordem_observacao: Mapped[str] = mapped_column('TJ_OBSERVA', db_sql.String)
    ordem_codsolicitacao: Mapped[str] = mapped_column('TJ_SOLICI', db_sql.String)
    ordem_situacao: Mapped[str] = mapped_column('TJ_SITUACA', db_sql.String)

    @hybrid_property
    def ordem_prioridade(self):
        return self.solicitacao_vinculada.solicitacao_prioridade if self.solicitacao_vinculada else None

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

    insumo_ordem_id: Mapped[str] = mapped_column('TL_ORDEM', db_sql.String,
                                                 ForeignKey(OrdemServico.ordem_id), primary_key=True)

    @hybrid_property
    def executor_nome(self):
        if self.insumo_tipo == "M":
            return self.executor.executor_nome
        return None

    insumo_codigo: Mapped[str] = mapped_column('TL_CODIGO', db_sql.String,
                                               ForeignKey(Executor.executor_matricula), primary_key=True)
    insumo_tipo: Mapped[str] = mapped_column('TL_TIPOREG', db_sql.String)

    ordem_vinculada: Mapped["OrdemServico"] = relationship(back_populates="ordem_insumos")
    executor: Mapped["Executor"] = relationship(
        "Executor",
        primaryjoin="Executor.executor_matricula==OrdemServicoInsumo.insumo_codigo",
        lazy="joined"
    )
