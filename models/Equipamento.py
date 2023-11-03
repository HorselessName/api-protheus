from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


@dataclass
class Equipamento(db_sql.Model):
    __tablename__ = 'ST9010'  # Tabela de Bens - Protheus.

    equipamento_id: Mapped[str] = mapped_column("T9_CODBEM", db_sql.String, primary_key=True)
    equipamento_filial: Mapped[str] = mapped_column("T9_FILIAL", db_sql.String, primary_key=True)
    equipamento_setor: Mapped[str] = mapped_column("T9_CODFAMI", db_sql.String, primary_key=True)
    equipamento_nome: Mapped[str] = mapped_column("T9_NOME", db_sql.String, nullable=False)
    equipamento_ccusto: Mapped[str] = mapped_column("T9_CCUSTO", db_sql.String, nullable=False)
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)
    T9_STATUS: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        ignore_fields = ["D_E_L_E_T_", "T9_STATUS"]
        return {key: str(getattr(self, key)) for key in self.__annotations__ if key not in ignore_fields}
