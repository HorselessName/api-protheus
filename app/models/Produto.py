from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


class Produto(db_sql.Model):
    __tablename__ = 'SB1010'

    # Campos da tabela
    produto_codigo: Mapped[str] = mapped_column("B1_COD", db_sql.String, primary_key=True)
    produto_descricao: Mapped[str] = mapped_column("B1_DESC", db_sql.String)
    produto_unidade: Mapped[str] = mapped_column("B1_UM", db_sql.String)
    produto_tipo: Mapped[str] = mapped_column("B1_TIPO", db_sql.String)

    # Campo de controle de exclusão, sem nome personalizado pra evitar o erro "Invalid Field" no Marshmallow.
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)
