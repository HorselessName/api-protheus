from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


class Filial(db_sql.Model):
    __tablename__ = 'SYS_COMPANY'  # Tabela de Filiais - Protheus.

    filial_grupo: Mapped[int] = mapped_column("M0_CODIGO", db_sql.Integer, primary_key=True)
    filial_codigo: Mapped[str] = mapped_column("M0_CODFIL", db_sql.String, primary_key=True)
    filial_nome: Mapped[str] = mapped_column("M0_FILIAL", db_sql.String, nullable=False)
    filial_familia: Mapped[str] = mapped_column("M0_NOME", db_sql.String, nullable=False)
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        return {
            "filial_grupo": self.filial_grupo,
            "filial_codigo": self.filial_codigo,
            "filial_nome": self.filial_nome,
            "filial_familia": self.filial_familia
        }


class Equipamento(db_sql.Model):
    __tablename__ = 'ST9010'  # Tabela de Bens - Protheus.

    equipamento_id: Mapped[int] = mapped_column("T9_CODBEM", db_sql.Integer, primary_key=True)
    equipamento_filial: Mapped[str] = mapped_column("T9_FILIAL", db_sql.String, primary_key=True)
    equipamento_setor: Mapped[str] = mapped_column("T9_CODFAMI", db_sql.String, primary_key=True)
    equipamento_nome: Mapped[str] = mapped_column("T9_NOME", db_sql.String, nullable=False)
    equipamento_ccusto: Mapped[str] = mapped_column("T9_CCUSTO", db_sql.String, nullable=False)
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)
    T9_STATUS: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        return {
            "equipamento_id": self.equipamento_id,
            "equipamento_filial": self.equipamento_filial,
            "equipamento_setor": self.equipamento_setor,
            "equipamento_nome": self.equipamento_nome,
            "equipamento_ccusto": self.equipamento_ccusto,
        }


class Solicitacao(db_sql.Model):
    __tablename__ = 'TQB010'  # Tabela de S.S. - Protheus.

    solicitacao_id: Mapped[int] = mapped_column("TQB_SOLICI", db_sql.Integer, primary_key=True)
    solicitacao_filial: Mapped[str] = mapped_column("TQB_FILIAL", db_sql.String, nullable=False)
    solicitacao_equipamento: Mapped[str] = mapped_column("TQB_CODBEM", db_sql.String, nullable=False)
    solicitacao_status: Mapped[str] = mapped_column("TQB_SOLUCA", db_sql.String, nullable=False)
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        return {
            "solicitacao_id": self.solicitacao_id,
            "solicitacao_filial": self.solicitacao_filial,
            "solicitacao_equipamento": self.solicitacao_equipamento,
            "solicitacao_status": self.solicitacao_status
        }
