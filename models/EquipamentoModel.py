from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


class Equipamento(db_sql.Model):
    __tablename__ = 'ST9010'  # Tabela de Bens - Protheus.

    equipamento_id: Mapped[int] = mapped_column("T9_CODBEM", db_sql.Integer, primary_key=True)
    equipamento_filial: Mapped[str] = mapped_column("T9_FILIAL", db_sql.String, nullable=False)
    equipamento_setor: Mapped[str] = mapped_column("T9_CODFAMI", db_sql.String, nullable=False)
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

