from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql


@dataclass
class Usuario(db_sql.Model):
    __tablename__ = 'SYS_USR'  # Tabela de Usuários - Protheus.

    usuario_codigo: Mapped[str] = mapped_column("USR_ID", db_sql.String, primary_key=True)
    usuario_login: Mapped[str] = mapped_column("USR_CODIGO", db_sql.String, unique=True, nullable=False)
    usuario_nome: Mapped[str] = mapped_column("USR_NOME", db_sql.String, nullable=False)
    usuario_bloqueado: Mapped[str] = mapped_column("USR_MSBLQL", db_sql.String, nullable=False)
