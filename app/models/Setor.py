from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


@dataclass
class Setor(db_sql.Model):
    __tablename__ = 'ST6010'  # Tabela de Famílias - Protheus.

    setor_filial: Mapped[str] = mapped_column("T6_FILIAL", db_sql.String, primary_key=True)
    setor_codigo: Mapped[str] = mapped_column("T6_CODFAMI", db_sql.String, primary_key=True)
    setor_nome: Mapped[str] = mapped_column("T6_NOME", db_sql.String, nullable=False)
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        ignore_fields = ["D_E_L_E_T_"]
        return {key: str(getattr(self, key)) for key in self.__annotations__ if key not in ignore_fields}
