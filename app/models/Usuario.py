from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db_context import db_sql


@dataclass
class Usuario(db_sql.Model):
    __tablename__ = 'SYS_USR'  # Tabela de Usuários - Protheus.

    usuario_codigo: Mapped[str] = mapped_column("USR_ID", db_sql.String, primary_key=True)
    usuario_login: Mapped[str] = mapped_column("USR_CODIGO", db_sql.String, unique=True, nullable=False)
    usuario_nome: Mapped[str] = mapped_column("USR_NOME", db_sql.String, nullable=False)
    usuario_bloqueado: Mapped[str] = mapped_column("USR_MSBLQL", db_sql.String, nullable=False)

    # Relacionamento N..1 com o Usuario: Um Usuario pode ter muitas filiais.
    # Backref: Cria uma referência na classe UsuarioFilial para deixar acessar o Usuario pela UsuarioFilial.
    # Exemplo: uma_filial = sessao.query(UsuarioFilial).first()

    filiais: Mapped[list["UsuarioFilial"]] = relationship("UsuarioFilial", backref="usuario", lazy='joined')


class UsuarioFilial(db_sql.Model):
    __tablename__ = 'SYS_USR_FILIAL'

    usuario_filial: Mapped[str] = mapped_column("USR_FILIAL", db_sql.String, primary_key=True, nullable=False)
    usuario_filial_grupo: Mapped[str] = mapped_column("USR_GRPEMP", db_sql.String, nullable=False)
    usuario_acesso: Mapped[str] = mapped_column("USR_ACESSO", db_sql.String, nullable=False)

    # Relacionamento para determinar a condição de `join` entre as tabelas relacionadas.
    usuario_codigo: Mapped[str] = mapped_column("USR_ID", db_sql.String, db_sql.ForeignKey(Usuario.usuario_codigo))
