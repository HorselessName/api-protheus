from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db_context import db_sql


# Referencias:
# https://terminaldeinformacao.com/wp-content/tabelas/tqb.php
# https://sempreju.com.br/tabelas_protheus/tabelas/tabela_tqb.html

@dataclass
class SolicitacaoDescricao(db_sql.Model):
    """
    Descrição de uma solicitação de serviço.
    É criada usando o código da solicitação de serviço (TQB_CODMSS) como chave primária e o nome da coluna.
    """
    __tablename__ = 'SYP010'

    # Desc. ID é o valor da coluna `TQB_CODMSS` da tabela `TQB010`. (Código de Descrição da Solicitação)
    descricao_id: Mapped[str] = mapped_column("YP_CHAVE",
                                              db_sql.String,
                                              ForeignKey('TQB010.TQB_CODMSS'),
                                              primary_key=True)

    descricao_texto: Mapped[str] = mapped_column("YP_TEXTO", db_sql.String, nullable=False)
    descricao_campo: Mapped[str] = mapped_column("YP_CAMPO", db_sql.String, nullable=False)

    # Relacionamento 1..1 no Padrão SQLAlchemy (Precisa ter dos dois lados, de acordo com a documentação).
    # Doc.: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-one
    # Note: ViewOnly para resolver "SAWarning" do Marshmallow de Overlapping Columns.
    solicitacao_descricao: Mapped[str] = relationship("Solicitacao", lazy="noload", viewonly=True)


@dataclass
class Solicitacao(db_sql.Model):
    """
    Esse modelo representa uma solicitação de serviço.
    Explicação dos campos principais:

    - TQB_DESCSS: Descrição da solicitação de serviço.
    1. Contém um código que é a chave primária da tabela SYP010 (YP_CHAVE).
    2. É vinculado essa chave primária com o campo YP_CHAVE, e também o campo YP_CAMPO vinculado com o campo TQB_CODMSS.
    3. Na Solicitacao é criado o TQB_CODMSS (YP_CHAVE) apenas.

    Join para trazer a descrição: LEFT JOIN SYP010 SYP ON TQB.TQB_CODMSS = SYP.YP_CHAVE

    """
    __tablename__ = 'TQB010'  # Tabela de S.S. - Protheus.

    solicitacao_id: Mapped[str] = mapped_column("TQB_SOLICI", db_sql.String, primary_key=True)
    solicitacao_filial: Mapped[str] = mapped_column("TQB_FILIAL", db_sql.String, nullable=False)
    solicitacao_equipamento: Mapped[str] = mapped_column("TQB_CODBEM", db_sql.String, nullable=False)
    solicitacao_status: Mapped[str] = mapped_column("TQB_SOLUCA", db_sql.String, nullable=False)
    solicitacao_prioridade: Mapped[str] = mapped_column("TQB_PRIORI", db_sql.String, nullable=False, default="1")
    solicitacao_origin: Mapped[str] = mapped_column("TQB_ORIGEM", db_sql.String, nullable=False)
    solicitacao_tipo: Mapped[str] = mapped_column("TQB_CDSERV", db_sql.String, nullable=False)
    solicitacao_databer: Mapped[str] = mapped_column("TQB_DTABER", db_sql.String, nullable=True)
    solicitacao_datafec: Mapped[str] = mapped_column("TQB_DTFECH", db_sql.String, nullable=True)
    solicitacao_horaber: Mapped[str] = mapped_column("TQB_HOABER", db_sql.String, nullable=True)
    solicitacao_horafec: Mapped[str] = mapped_column("TQB_HOFECH", db_sql.String, nullable=True)
    solicitacao_tempo: Mapped[str] = mapped_column("TQB_TEMPO", db_sql.String, nullable=True)

    D_E_L_E_T_: Mapped[str] = mapped_column(db_sql.String, nullable=True)

    # Relacionamento 1..1 com a tabela SYP010.
    solicitacao_descricao_id: Mapped[str] = mapped_column("TQB_CODMSS", db_sql.String)
    solicitacao_descricao: Mapped[SolicitacaoDescricao] = relationship(
        "SolicitacaoDescricao", lazy="joined")

    def to_dict(self):
        atributos_ignore = ['_sa_instance_state', 'D_E_L_E_T_', 'solicitacao_descricao_id']
        dict_solicitacao = {}

        for nome_propriedade, valor_propriedade in self.__dict__.items():
            if nome_propriedade in atributos_ignore:
                continue
            elif nome_propriedade == 'solicitacao_descricao':
                # Adiciona apenas o texto da descrição da solicitação
                if valor_propriedade is not None:
                    dict_solicitacao['solicitacao_descricao'] = valor_propriedade.descricao_texto.strip()
            else:
                # Adiciona os outros atributos, aplicando strip se for string
                valor_formatado = valor_propriedade.strip() if isinstance(valor_propriedade, str) else valor_propriedade
                dict_solicitacao[nome_propriedade] = valor_formatado

        # Aplicar o valor padrão para a prioridade se o campo estiver vazio ou com espaço
        if 'solicitacao_prioridade' in dict_solicitacao and not dict_solicitacao['solicitacao_prioridade'].strip():
            dict_solicitacao['solicitacao_prioridade'] = "1"

        return dict_solicitacao

    def __repr__(self) -> str:
        atributos_ignore = ['_sa_instance_state', 'D_E_L_E_T_', 'solicitacao_descricao_id']
        representacao_solicitacao = f"<{self.__class__.__name__}("

        for nome_propriedade, valor_propriedade in self.__dict__.items():
            if nome_propriedade in atributos_ignore:
                continue
            elif nome_propriedade == 'solicitacao_descricao':
                # Adiciona apenas o texto da descrição da solicitação
                if valor_propriedade is not None:
                    texto_descricao = valor_propriedade.descricao_texto.strip()
                    representacao_solicitacao += f"solicitacao_descricao='{texto_descricao}', "
            else:
                # Adiciona os outros atributos, aplicando strip se for string
                valor_formatado = valor_propriedade.strip() if isinstance(valor_propriedade, str) else valor_propriedade
                representacao_solicitacao += f"{nome_propriedade}='{valor_formatado}', "

        representacao_solicitacao = representacao_solicitacao.rstrip(", ")  # Remove a última vírgula
        representacao_solicitacao += ")>"
        return representacao_solicitacao
