from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


class Filial(db_sql.Model):
    __tablename__ = 'SYS_COMPANY'  # Tabela de Filiais - Protheus.

    filial_grupo: Mapped[str] = mapped_column("M0_CODIGO", db_sql.String, primary_key=True)
    filial_codigo: Mapped[str] = mapped_column("M0_CODFIL", db_sql.String, primary_key=True)
    filial_nome: Mapped[str] = mapped_column("M0_FILIAL", db_sql.String, nullable=False)
    filial_familia: Mapped[str] = mapped_column("M0_NOME", db_sql.String, nullable=False)
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        ignore_fields = ["D_E_L_E_T_"]
        return {key: str(getattr(self, key)) for key in self.__annotations__ if key not in ignore_fields}
