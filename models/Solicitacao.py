from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


@dataclass
class Solicitacao(db_sql.Model):
    __tablename__ = 'TQB010'  # Tabela de S.S. - Protheus.

    solicitacao_id: Mapped[str] = mapped_column("TQB_SOLICI", db_sql.String, primary_key=True)
    solicitacao_filial: Mapped[str] = mapped_column("TQB_FILIAL", db_sql.String, nullable=False)
    solicitacao_equipamento: Mapped[str] = mapped_column("TQB_CODBEM", db_sql.String, nullable=False)
    solicitacao_status: Mapped[str] = mapped_column("TQB_SOLUCA", db_sql.String, nullable=False)
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        ignore_fields = ["D_E_L_E_T_"]
        return {key: str(getattr(self, key)) for key in self.__annotations__ if key not in ignore_fields}
