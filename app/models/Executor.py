from db_context import db_sql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List


class Executor(db_sql.Model):
    __tablename__ = "ST1010"

    executor_matricula: Mapped[str] = mapped_column("T1_CODFUNC", db_sql.String, primary_key=True)
    executor_filial: Mapped[str] = mapped_column("T1_FILIAL", db_sql.String, nullable=False)
    executor_nome: Mapped[str] = mapped_column("T1_NOME", db_sql.String, nullable=False)
    executor_email: Mapped[str] = mapped_column("T1_EMAIL", db_sql.String, nullable=False)
    executor_usuario: Mapped[str] = mapped_column("T1_CODUSU", db_sql.String, nullable=False)
    exeutor_ccusto: Mapped[str] = mapped_column("T1_CCUSTO", db_sql.String, nullable=False)
    executor_turno: Mapped[str] = mapped_column("T1_TURNO", db_sql.String, nullable=False)

    # Relacionamento 1..N. Um executor pode ter várias especialidades.
    # Backref: Referencia reversa. Permite acessar o Executor a partir da Especialidade.
    # Ex: EspecialidadesDoExecutor.executor.executor_nome
    executor_especialidades: Mapped[List["EspecialidadesDoExecutor"]] = relationship(
        "EspecialidadesDoExecutor",
        primaryjoin="Executor.executor_matricula==EspecialidadesDoExecutor.executante_codigo",
        backref="executor_relacionado",
        lazy='joined'
    )


class EspecialidadesDoExecutor(db_sql.Model):
    """
    Lista de Especialidades do Executor.
    Para mapear o NOME da Especialidade, o `especialidade_codigo` foi estruturado para tentar reproduzir a lógica
    SQL que faz:

    SELECT
        detalhes_especialidade.T0_XESPECI
    FROM
        ST0010 detalhes_especialidade
    WHERE
        detalhes_especialidade.T0_ESPECIA = especialidade_do_executor.T2_ESPECIA
    """
    __tablename__ = 'ST2010'  # Tabela do Protheus de Especialidades do Executor.

    executante_codigo: Mapped[str] = mapped_column('T2_CODFUNC',
                                                   ForeignKey('ST1010.T1_CODFUNC')
                                                   )

    # Chave para o Relacionamento com a Tabela de Detalhes da Especialidade.
    # Select DetalhesEspecialidade.T0_XESPECI
    # Where DetalhesEspecialidade.T0_ESPECIA == EspecialidadesDoExecutor.T2_ESPECIA

    especialidade_codigo: Mapped[str] = mapped_column('T2_ESPECIA',
                                                      ForeignKey('ST0010.T0_ESPECIA'),
                                                      primary_key=True)

    # Nome da Especialidade: Mapeada do Relacionamento com a Tabela de Especialidades.
    detalhes_especialidade: Mapped["DetalhesEspecialidade"] = relationship("DetalhesEspecialidade")


class DetalhesEspecialidade(db_sql.Model):
    __tablename__ = 'ST0010'  # Tabela do Protheus de Detalhes das Especialidades

    especialidade_codigo: Mapped[str] = mapped_column('T0_ESPECIA', db_sql.String, primary_key=True)
    especialidade_nome: Mapped[str] = mapped_column('T0_XESPECI', db_sql.String)
