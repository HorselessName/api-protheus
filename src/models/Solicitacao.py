from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from db_context import db_sql

# Referencias:
# https://terminaldeinformacao.com/wp-content/tabelas/tqb.php
# https://sempreju.com.br/tabelas_protheus/tabelas/tabela_tqb.html


@dataclass
class Solicitacao(db_sql.Model):
    __tablename__ = 'TQB010'  # Tabela de S.S. - Protheus.

    solicitacao_id: Mapped[str] = mapped_column("TQB_SOLICI", db_sql.String, primary_key=True)
    solicitacao_filial: Mapped[str] = mapped_column("TQB_FILIAL", db_sql.String, nullable=False)
    solicitacao_equipamento: Mapped[str] = mapped_column("TQB_CODBEM", db_sql.String, nullable=False)
    solicitacao_status: Mapped[str] = mapped_column("TQB_SOLUCA", db_sql.String, nullable=False)
    solicitacao_prioridade: Mapped[str] = mapped_column("TQB_PRIORI", db_sql.String, nullable=False, default="1")
    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    def to_dict(self):
        # Ignorar a coluna D_E_L_E_T_ ao criar o dicionário
        data = {key: str(getattr(self, key)) for key in self.__annotations__ if key not in ["D_E_L_E_T_"]}

        # Aplicar o valor padrão para a prioridade se o campo estiver vazio ou com espaço
        if not data.get("solicitacao_prioridade").strip():
            data["solicitacao_prioridade"] = "1"

        return data
